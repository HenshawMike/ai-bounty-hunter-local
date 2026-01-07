import subprocess
import json
import os
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)
semgrep_config = config.get("semgrep_config")
code_path = config.get("code_path")

def run_semgrep_scan(code_path: str = code_path,
                    semgrep_config: str = semgrep_config):
    try:
        result = subprocess.run(
            ["semgrep", "scan",  "--config",semgrep_config,  "--json","--quiet","--timeout","0", code_path],
            capture_output=True,
            text = True,
            timeout=60,
            )
        if result.returncode == 0:
            data= json.loads(result.stdout)
            return data.get("results", [])
        else:
            print(f"Semgrep warning/error (non-fatal) - Return code: {result.returncode}")
            print("Stderr:", result.stderr.strip())
            print("Stdout:", result.stdout.strip()) #
            return []
    except subprocess.TimeoutExpired:
        print("Semgrep scan timed out", code_path)
        return []
    except json.JSONDecodeError:
        print("Semgrep scan failed to decode JSON", result.stdout)
        return []
    except Exception as e:
        print("Semgrep unexpected failure:", str(e))
        return []
            