import sys
import os
import asyncio

import dbus_next.service
import dbus_next.aio
from dbus_next.service import Variant
from dbus_next.aio import MessageBus
from dbus_next import BusType

from ..utils import logger

_logger = logger.get_logger(os.path.basename(__file__))


# You must assign interfaces at one time 
# During the bus connected
async def dbus_publish(puppy_controllers):
    try:
        bus = MessageBus(bus_type=BusType.SESSION)
        await bus.connect()

        for puppy_controller in puppy_controllers:
            bus.export(puppy_controller.DBUS_PATH, puppy_controller)
            await bus.request_name(puppy_controller.DBUS_NAME)
            _logger.info(f"{puppy_controller.pet.name} dbus_publish()")
            #await bus.wait_for_disconnect()

    except Exception as e:
        _logger.error(e)
        sys.exit(1)


class PuppyController(dbus_next.service.ServiceInterface):
    #DBUS_NAME = "com.puppy.Puppy"
    #DBUS_PATH = "/com/puppy/Puppy/"
    #DBUS_INTERFACE = "com.puppy.Puppy."

    def __init__(self, _puppy):
        self.pet = _puppy
        self.DBUS_NAME = "com.puppy.Puppy"
        self.DBUS_PATH = "/com/puppy/Puppy"
        self.DBUS_INTERFACE = "com.puppy.Puppy." + str(self.pet.name)

        _logger.info(f"DBUS_NAME: {self.DBUS_NAME}")
        _logger.info(f"DBUS_PATH: {self.DBUS_PATH}")
        _logger.info(f"DBUS_INTERFACE: {self.DBUS_INTERFACE}")

        super().__init__(self.DBUS_INTERFACE)


    # dst: destination for walk
    # time: how long it walks
    # range: how far it goes
    @dbus_next.service.method("WalkOutside")
    async def walk_outside(self, dst: "s", time: "n", range: "n") -> "n":
        self.pet.state += (dst * (range / time))

        return self.pet.state
        
    # _amount: amount of food
    @dbus_next.service.method("Feed")
    async def feed(self, _amount: "n") -> "n":
        self.pet.hunger -= _amount
        _logger.info(f"{self.pet.name}({self.pet.age})'s hunger: {self.pet.hunger}")

        return self.pet.hunger
