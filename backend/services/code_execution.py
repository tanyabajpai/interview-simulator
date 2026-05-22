import subprocess
import tempfile
import os
import textwrap


def run_code(code: str):
    try:
        wrapped_code = f"""{code}

if __name__ == "__main__":
    try:
        result = solution()
        if result is not None:
            print(result)
    except TypeError as e:
        print("Error:", e)
        print("Tip: your solution() should accept the input as a parameter, e.g. def solution(s):")
    except Exception as e:
        print("Error:", e)
"""

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp:
            temp.write(textwrap.dedent(wrapped_code))
            temp_path = temp.name

        result = subprocess.run(
            ["python3", temp_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        os.remove(temp_path)

        output = result.stdout.strip()
        stderr = result.stderr.strip()

        return {
            "stdout": output if output else stderr,
            "stderr": stderr
        }

    except subprocess.TimeoutExpired:
        return {"stdout": "Time Limit Exceeded (5s)", "stderr": ""}
    except Exception as e:
        return {"stdout": "", "stderr": str(e)}