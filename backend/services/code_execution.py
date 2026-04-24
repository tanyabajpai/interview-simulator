import subprocess
import tempfile
import os
import textwrap

def run_code(code: str):
    try:
        # 🔥 Wrap user code to actually CALL solution()
        wrapped_code = f"""
{code}

if __name__ == "__main__":
    try:
        print(solution("hello"))  # default test input
    except Exception as e:
        print("Error:", e)
"""

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp:
            temp.write(textwrap.dedent(wrapped_code))
            temp_path = temp.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        os.remove(temp_path)

        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    except Exception as e:
        return {
            "error": str(e)
        }