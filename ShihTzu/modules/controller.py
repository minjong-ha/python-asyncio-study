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
async def dbus_publish(controllers):
    try:
        bus = MessageBus(bus_type=BusType.SESSION)
        await bus.connect()

        for controller in controllers:
            bus.export(controller.DBUS_PATH, controller)
            await bus.request_name(controller.DBUS_NAME)
            _logger.info(f"{controller.DBUS_PATH} - {controller.DBUS_INTERFACE} dbus_publish()")
            #await bus.wait_for_disconnect()

    except Exception as e:
        _logger.error(e)
        sys.exit(1)

class CageController(dbus_next.service.ServiceInterface):
    def __init__(self, _loop):
        self.DBUS_NAME = "com.puppy.Puppy"
        self.DBUS_PATH = "/com/puppy/Puppy"
        self.DBUS_INTERFACE = "com.puppy.Puppy.Cage"
        self.loop = _loop

        _logger.info(f"DBUS_NAME: {self.DBUS_NAME}")
        _logger.info(f"DBUS_PATH: {self.DBUS_PATH}")
        _logger.info(f"DBUS_INTERFACE: {self.DBUS_INTERFACE}")

        super().__init__(self.DBUS_INTERFACE)

    # TODO (minjong, 221220): Add signals for PuppyControllers

    @dbus_next.service.method("RequestFeedAll")
    def request_feed_all(self) -> "b":
        return self.feed_all()
        
    @dbus_next.service.method("RequestWalkAll")
    def request_walk_all(self) -> "b":
        return self.walk_all()

    @dbus_next.service.method("StopAll")
    def request_stop_all(self) -> "b":
        try:
            self.loop.stop()
            return True
        except Exception as e:
            return False

    @dbus_next.service.signal("FeedAll")
    def feed_all(self) -> "b":
        return True

    @dbus_next.service.signal("WalkAll")
    def walk_all(self) -> "b":
        return True


class PuppyController(dbus_next.service.ServiceInterface):
    #DBUS_NAME = "com.puppy.Puppy"
    #DBUS_PATH = "/com/puppy/Puppy/"
    #DBUS_INTERFACE = "com.puppy.Puppy."

    def __init__(self, _puppy):
        self.pet = _puppy
        self.DBUS_NAME = "com.puppy.Puppy"
        self.DBUS_PATH = "/com/puppy/Puppy"
        self.DBUS_INTERFACE = "com.puppy.Puppy." + str(self.pet.name)
        self.interface = None

        _logger.info(f"DBUS_NAME: {self.DBUS_NAME}")
        _logger.info(f"DBUS_PATH: {self.DBUS_PATH}")
        _logger.info(f"DBUS_INTERFACE: {self.DBUS_INTERFACE}")

        super().__init__(self.DBUS_INTERFACE)

    async def _on_feed_all(self, description):
        _pre = self.pet.hunger
        self.pet.hunger += 10
        _logger.info(f"{self.pet.name} hunger: {_pre} -> {self.pet.hunger} {description}")

    async def _on_walk_all(self, description):
        _pre = self.pet.state
        self.pet.state += 10
        _logger.info(f"{self.pet.name} state: {_pre} -> {self.pet.state} {description}")

    async def initialize(self):
        self.interface = await self._get_dbus_interface()
        self.interface.on_feed_all(self._on_feed_all)
        self.interface.on_walk_all(self._on_walk_all)

    async def _get_dbus_interface(self):
        bus = await MessageBus(bus_type=BusType.SESSION).connect()

        with open("dbus/com.puppy.Puppy.xml", "r") as f:
            introspection = f.read()

        proxy_object = bus.get_proxy_object("com.puppy.Puppy", "/com/puppy/Puppy", introspection)

        interface = proxy_object.get_interface("com.puppy.Puppy.Cage")

        return interface

    # dst: destination for walk
    # time: how long it walks
    # range: how far it goes
    @dbus_next.service.method("WalkOutside")
    async def walk_outside(self, dst: "s", time: "n", range: "n") -> "n":

        try:
            assert time > 0
            assert range > 0
            assert dst is not None

        except AssertionError as e:
            _logger.error(e)
            return 0

        self.pet.state += (range / time)
        _logger.info(f"{self.pet.name}({self.pet.age})'s state : {self.pet.state} ")

        return self.pet.state
        
    # _amount: amount of food
    @dbus_next.service.method("Feed")
    async def feed(self, _amount: "n") -> "n":
        self.pet.hunger += _amount
        _logger.info(f"{self.pet.name}({self.pet.age})'s hunger: {self.pet.hunger}")

        return self.pet.hunger

    @dbus_next.service.dbus_property(
        access=dbus_next.PropertyAccess.READ, name="State"
    )
    async def get_state(self) -> "n":
        return self.pet.state

    @dbus_next.service.dbus_property(
        access=dbus_next.PropertyAccess.READ, name="Hunger"
    )
    async def get_hunger(self) -> "n":
        return self.pet.hunger