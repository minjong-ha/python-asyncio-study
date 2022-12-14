import asyncio
import sys
import os

from .utils import logger
_logger = logger.get_logger(os.path.basename(__file__))

async def print_log_every_n_sec(_arg: str, _interval: int):
    while True:
        _logger.info(f"{_arg} for every {_interval} seconds")
        await asyncio.sleep(_interval)


async def return_value_async():
    return True


async def run():
    _logger.info(f"Shih-Tzu run()")

    task_1 = asyncio.create_task(print_log_every_n_sec("task_1", 1))
    task_2 = asyncio.create_task(print_log_every_n_sec("task_2", 2))
    task_3 = asyncio.create_task(print_log_every_n_sec("task_3", 3))

    await task_1
    await task_2
    await task_3
    
