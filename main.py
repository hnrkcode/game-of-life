# /// script
# dependencies = [
#  "pygame-ce",
# ]
#
# [tool.ty.environment]
# root = ["."]
# ///

import asyncio

from gameoflife import app

asyncio.run(app.run())
