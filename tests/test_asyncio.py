import sys
import pytest

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from ShihTzu.main import *

@pytest.mark.asyncio
async def test_async_func():
    ret = return_value_async()

    assert ret and True
    
