import os
import asyncio
import random

from ..controller import *
from ...utils import logger

_logger = logger.get_logger(os.path.basename(__file__))

DEFAULT_HUNGER_INTERVAL = 10
RANDOM_INTERVAL = 30
MAX_STATE = 100
MAX_HUNGER = 100

class ShihTzu:
    def __init__(self, _name, _age):
        self.name = _name
        self.age = _age
        self.species = "Shih-Tzu"
        self.state = MAX_STATE
        self.hunger = MAX_HUNGER

        self.controller = PuppyController(self)

        self.exit_code = None

    async def _bark(self):
        _logger.info(f"{self.name}({self.age}) Bark! - state: {self.state}  hunger: {self.hunger}")

    async def _default_state_decrease(self, interval):
        while True:
            await asyncio.sleep(interval)
            self.state -= 1
            #_logger.info(f"{self.name}({self.age})'s state: {self.state}")

            if (random.randrange(100) < (100 - self.state)):
                await self._bark()


    async def _default_hunger_decrease(self, interval):
        while True:
            await asyncio.sleep(interval)
            self.hunger -= 1
            #_logger.info(f"{self.name}({self.age})'s hunger: {self.hunger}")

            if (random.randrange(100) < (100 - self.state)):
                await self._bark()


    # TODO (minjong, 221220): Add get_properties via dbus-interface
    # TODO (minjong, 221220): Make state and hunger observable. If it becomes 0, puppy will die...
    # TODO (minjong, 221220): Add on_signal_cb for Oneshot DBUS Interface

    async def prepare(self, _name: str, _age: int):

        asyncio.create_task(self._default_hunger_decrease(DEFAULT_HUNGER_INTERVAL))
        asyncio.create_task(self._default_state_decrease(DEFAULT_HUNGER_INTERVAL))

        _logger.info(f"{self.name}({self.age}) prepare()")

        return True

    async def run(self):
        _logger.info(f"{self.species} {self.name}({self.age}) start to run()")
        await self.prepare(self.name, self.age)

