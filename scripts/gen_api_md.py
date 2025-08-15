import json
from pathlib import Path
from src.main import app


output_file = Path("../docs/api_auto/api_auto.md")
output_file.parent.mkdir(parents=True, exist_ok=True)

openapi_json = app.openapi()

with open(output_file.with_suffix(".json"), "w", encoding="utf-8") as f:
    json.dump(openapi_json, f, indent=2)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# API Documentation\n\n")
    for path, methods in openapi_json["paths"].items():
        f.write(f"## `{path}`\n\n")
        for method, info in methods.items():
            f.write(f"### {method.upper()}\n")
            if info.get("summary"):
                f.write(f"{info['summary']}\n\n")
            if info.get("description"):
                f.write(f"{info['description']}\n\n")
            if "parameters" in info:
                f.write("**Parameters:**\n\n")
                for p in info["parameters"]:
                    f.write(f"- `{p['name']}` ({p.get('in','')}) - {p.get('description','')}\n")
                f.write("\n")
            if "requestBody" in info:
                f.write("**Request Body:**\n\n")
                f.write(json.dumps(info["requestBody"], indent=2))
                f.write("\n\n")
            if "responses" in info:
                f.write("**Responses:**\n\n")
                for status, resp in info["responses"].items():
                    f.write(f"- {status}: {resp.get('description','')}\n")
                f.write("\n")
