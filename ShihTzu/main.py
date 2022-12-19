import asyncio
import sys
import os

from ShihTzu.modules.dbus import Interact

from .utils import logger
from .modules import *

_logger = logger.get_logger(os.path.basename(__file__))

async def print_log_every_n_sec(_arg: str, _interval: int):
    while True:
        _logger.info(f"{_arg} for every {_interval} seconds")
        await asyncio.sleep(_interval)


async def return_value_async():
    return True


class ShihTzu:
    def __init__(self):
        self.name = None
        self.age = None
        self.status = None

        self.exit_code = None

    def _handle_exception(self, loop, context):
        _logger.error(f"Exception: {context}")

        exception = context.get("exception")
        if exception:
            _logger.error(f"Exception Info: {exception}")

        loop.stop()
        self.exit_code = os.EX_SOFTWARE

    async def prepare(self, _name: str, _age: int):
        self.name = _name
        self.age = _age
        self.status = None

        # assign dbus-interface(user) for socket income
        self._interact_dbus_interface = Interact()
        await self._interact_dbus_interface.dbus_publish()

        _logger.info("prepare() complete")

        return await return_value_async()

    def run(self):
        # Only a single event loop is allowed in the entire application.
        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self._handle_exception)
        self.loop.create_task(self.prepare("poppi", 5))

        # Before the self.loop.run_forever(), assign all tasks that application requires
        # If one of the task call loop.stop(), the event loop will be closed.
        self.loop.run_forever()


    
