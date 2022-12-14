import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))

from ShihTzu import main

asyncio.run(main.run())


