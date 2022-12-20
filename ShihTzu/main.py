import asyncio
import os

from ShihTzu.modules.controller import dbus_publish


from .utils import logger
from .modules import *
from .modules.models.shihtzu import ShihTzu

_logger = logger.get_logger(os.path.basename(__file__))

async def print_log_every_n_sec(_arg: str, _interval: int):
    while True:
        _logger.info(f"{_arg} for every {_interval} seconds")
        await asyncio.sleep(_interval)


async def return_value_async():
    return True


def _handle_exception(self, loop, context):
    _logger.error(f"Exception: {context}")

    exception = context.get("exception")
    if exception:
        _logger.error(f"Exception Info: {exception}")

    loop.stop()
    self.exit_code = os.EX_SOFTWARE

def run():
    loop = asyncio.get_event_loop() 
    loop.set_exception_handler(_handle_exception)

    # Create ShihTzu objects and make them run()
    poppi = ShihTzu("poppi", 12)
    toto = ShihTzu("toto", 10)

    loop.create_task(toto.run())
    loop.create_task(poppi.run())

    # Assign dbus-interface for ShihTzu objects
    controllers = list()
    controllers.append(toto.controller)
    controllers.append(poppi.controller)

    loop.create_task(dbus_publish(controllers))

    loop.run_forever()
