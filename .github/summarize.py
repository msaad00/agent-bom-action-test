import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
agents = d.get("agents") or []
print("agents", [(a.get("name"), a.get("agent_type"), a.get("config_path"), len(a.get("mcp_servers") or [])) for a in agents])
print("summary", {k: v for k, v in (d.get("summary") or {}).items() if k in ("total_vulnerabilities", "total_packages", "total_agents", "total_servers")}, "grade", d.get("posture_grade"), "outcome", (d.get("scan_run") or {}).get("outcome"))
print("possibly_affected", len(d.get("possibly_affected") or []))
print("issues", [str(i)[:160] for i in ((d.get("scan_run") or {}).get("issues") or [])][:8])
