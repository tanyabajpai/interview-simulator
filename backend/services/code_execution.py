import subprocess
import tempfile
import os

def run_code(code: str):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(code.encode())
            temp_path = temp.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        os.remove(temp_path)

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "error": str(e)
        }