import asyncio
import os

from ShihTzu.modules.controller import CageController, dbus_publish


from .utils import logger
from .modules import *
from .modules.models.shihtzu import ShihTzu

_logger = logger.get_logger(os.path.basename(__file__))

def _handle_exception(self, loop, context):
    _logger.error(f"Exception: {context}")

    exception = context.get("exception")
    if exception:
        _logger.error(f"Exception Info: {exception}")

    loop.stop()
    self.exit_code = os.EX_SOFTWARE

def run():
    loop = asyncio.get_event_loop() 
    #loop.set_exception_handler(_handle_exception)

    # Create cage controller rule them all
    cage_controller = CageController(loop)

    # Create ShihTzu objects and make them run()
    puppies = list()

    poppi = ShihTzu("poppi", 12)
    toto = ShihTzu("toto", 10)
    tori = ShihTzu("tori", 3)

    puppies.append(poppi)
    puppies.append(toto)
    puppies.append(tori)

    # Assign dbus-interface for ShihTzu objects and cage
    controllers = list()
    controllers.append(cage_controller)
    for puppy in puppies:
        controllers.append(puppy.controller)

    loop.create_task(dbus_publish(controllers))

    for puppy in puppies:
        loop.create_task(puppy.run())
        loop.create_task(puppy.controller.initialize())

    loop.run_forever()
