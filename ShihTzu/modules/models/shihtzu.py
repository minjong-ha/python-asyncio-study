import os
import asyncio
import random

from ..controller import *
from ...utils import logger

_logger = logger.get_logger(os.path.basename(__file__))

DEFAULT_HUNGER_INTERVAL = 10

class ShihTzu:
    def __init__(self, _name, _age):
        self.name = _name
        self.age = _age
        self.species = "Shih-Tzu"
        self.state = 0
        self.hunger = 0

        self.controller = PuppyController(self)

        self.exit_code = None

    async def random_bark(self):
        while True:
            _random = random.randint(1,10)
            await asyncio.sleep(_random)
            _logger.info(f"{self.name}:{self.age} Bark! for {_random} sec")

    async def _default_hunger_decrease(self, interval):
        while True:
            await asyncio.sleep(interval)
            self.hunger += 1
            _logger.info(f"{self.name}({self.age})'s hunger: {self.hunger}")

    async def prepare(self, _name: str, _age: int):
        # assign dbus-interface(user) for socket income

        asyncio.create_task(self.random_bark())
        asyncio.create_task(self._default_hunger_decrease(DEFAULT_HUNGER_INTERVAL))
        #asyncio.create_task(dbus_publish(self._interact_dbus_interface))

        _logger.info(f"{self.name}({self.age}) prepare()")

        # Never reached since random_bark()
        return True

    async def run(self):
        _logger.info(f"{self.species} {self.name}({self.age}) start to run()")
        await self.prepare(self.name, self.age)

