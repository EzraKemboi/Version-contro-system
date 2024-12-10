"""
This tells Python to invoke the main() function from the cli.py file
 when python -m myscm is executed.
"""
from .cli import main

if __name__ == "__main__":
    main()
