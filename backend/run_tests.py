import os
import sys

# Ensure PYTHONPATH includes the /app directory
sys.path.insert(0, '/app')

import subprocess

# Run pytest with the tests directory
result = subprocess.run(['pytest', 'tests'], capture_output=True, text=True)

# Print pytest output
print(result.stdout)
print(result.stderr)

# Return the exit code of pytest so it can be captured by CI/CD or shell
sys.exit(result.returncode)
