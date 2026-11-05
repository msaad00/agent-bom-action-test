import json, os, platform, pathlib
home = pathlib.Path.home()
sys_ = platform.system()
cfg = {"mcpServers": {"gh": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github@2025.4.8"], "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GH_PLACEHOLDER}"}}}}
if sys_ == "Windows":
    appdata = pathlib.Path(os.environ["APPDATA"])
    claude = appdata / "Claude/claude_desktop_config.json"
    vscode = appdata / "Code/User/mcp.json"
elif sys_ == "Darwin":
    claude = home / "Library/Application Support/Claude/claude_desktop_config.json"
    vscode = home / "Library/Application Support/Code/User/mcp.json"
else:
    claude = home / ".config/Claude/claude_desktop_config.json"
    vscode = home / ".config/Code/User/mcp.json"
paths = {claude: cfg, home / ".cursor/mcp.json": cfg, home / ".codeium/windsurf/mcp_config.json": cfg, vscode: {"servers": cfg["mcpServers"]}, home / ".gemini/settings.json": cfg}
for p, c in paths.items():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(c))
    print("wrote", p)
cont = home / ".continue/config.yaml"
cont.parent.mkdir(parents=True, exist_ok=True)
cont.write_text("name: t\nversion: 1.0.0\nschema: v1\nmcpServers:\n  - name: gh\n    command: npx\n    args: ['-y', '@modelcontextprotocol/server-github@2025.4.8']\n")
print("wrote", cont)
print("expected_clients", 6)
