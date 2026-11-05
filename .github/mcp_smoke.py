import json, os, subprocess, time
exe = "agent-bom.exe" if os.name == "nt" else "agent-bom"
p = subprocess.Popen([exe, "mcp", "server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open("out/mcp.err", "w"), text=True, encoding="utf-8")
def send(o): p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()
t = time.time()
send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}})
print("init", p.stdout.readline()[:120], round(time.time() - t, 1), "s")
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
print("tools", [x["name"] for x in json.loads(p.stdout.readline())["result"]["tools"]])
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check", "arguments": {"package": "lodash", "ecosystem": "npm", "version": "4.17.20"}}})
print("check", p.stdout.readline()[:200])
p.terminate()
