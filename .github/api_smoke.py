import json, os, secrets, socket, subprocess, sys, tempfile, time, urllib.error, urllib.request
s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
key = secrets.token_urlsafe(32)
work = tempfile.mkdtemp()
env = dict(os.environ, AGENT_BOM_DB=os.path.join(work, "api with space.db"), AGENT_BOM_STATE_DIR=work)
log = open("out/api.log", "w")
exe = "agent-bom.exe" if os.name == "nt" else "agent-bom"
p = subprocess.Popen([exe, "api", "--port", str(port), "--api-key", key], stdout=log, stderr=log, env=env)
base = f"http://127.0.0.1:{port}"
def call(path, data=None):
    r = urllib.request.Request(base + path, data=data, headers={"authorization": f"Bearer {key}", "content-type": "application/json"}, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(r, timeout=60) as x:
            return x.status, json.loads(x.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:200]
try:
    t = time.time()
    while time.time() - t < 120:
        try:
            if call("/health")[0] == 200: break
        except Exception: time.sleep(1)
    print("health after", round(time.time() - t, 1), "s")
    body = open("out/project.json", "rb").read()
    print("push", str(call("/v1/results/push", body))[:200])
    time.sleep(5)
    for path in ("/v1/jobs", "/v1/findings", "/v1/graph", "/v1/overview"):
        c, r = call(path)
        print(path, c, len(json.dumps(r)) if isinstance(r, dict) else r)
finally:
    p.terminate()
    try: print("stop rc", p.wait(30))
    except subprocess.TimeoutExpired: p.kill(); print("killed after timeout")
