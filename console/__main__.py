import sys

from .main import main

if __name__ == "__main__":
    rc = 1
    try:
        rc = main()
    except Exception as e:
        print(f"Error: {rc}")
    sys.exit(rc)
