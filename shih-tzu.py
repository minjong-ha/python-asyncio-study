import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))

from ShihTzu import main

if __name__ == "__main__":

    app = main.ShihTzu()
    app.run()
    sys.exit(app.exit_code)

    




