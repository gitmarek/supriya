import asyncio

import pytest
import pytest_asyncio

import supriya

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# TODO: make this fixture persistent
@pytest_asyncio.fixture()
async def async_server():
    server = supriya.AsyncServer()
    await server.boot(port=supriya.osc.utils.find_free_port())
    yield server
    await server.quit()


async def test_RealtimeProvider_async_init(async_server):
    provider = supriya.Provider.from_context(async_server)
    assert provider is not None
    async with provider.at():
        provider.add_synth(frequency=440)
    await asyncio.sleep(1)
