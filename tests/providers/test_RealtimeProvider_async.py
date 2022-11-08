import asyncio
import random
import time

import pytest
import pytest_asyncio

import supriya
from supriya.osc import OscBundle, OscMessage

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


# @pytest.fixture(scope="module")
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# TODO: make this fixture persistent
@pytest_asyncio.fixture()
async def async_server(event_loop):
    server = supriya.AsyncServer()
    await server.boot(port=supriya.osc.utils.find_free_port())
    provider = supriya.Provider.from_context(server)
    async with provider.at():
        synth_p = provider.add_synth()
        synth_p.free()
    yield server
    await server.quit()


# Make sure messages are sent in the right order
async def test_RealtimeProvider_async_set_node_01(async_server):
    provider = supriya.Provider.from_context(async_server)
    assert provider is not None
    cur_time = time.time()
    with async_server.osc_protocol.capture() as transcript:
        async with provider.at(cur_time + 1):
            async with provider.at(cur_time):
                synth_p = provider.add_synth(frequency=440)
            provider.free_node(synth_p)
        async with provider.at(cur_time + 0.75):
            provider.set_node(synth_p, frequency=1760)
        async with provider.at(cur_time + 0.5):
            provider.set_node(synth_p, frequency=880, amplitude=0.2)

    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscBundle(
                contents=(OscMessage("/s_new", "default", synth_p.identifier, 0, 1),),
                timestamp=cur_time + provider.latency,
            ),
        ),
        (
            "S",
            OscBundle(
                contents=(OscMessage("/n_set", synth_p.identifier, "gate", 0),),
                timestamp=cur_time + provider.latency + 1.0,
            ),
        ),
        (
            "S",
            OscBundle(
                contents=(OscMessage("/n_set", synth_p.identifier, "frequency", 1760),),
                timestamp=cur_time + provider.latency + 0.75,
            ),
        ),
        (
            "S",
            OscBundle(
                contents=(
                    OscMessage("/n_set", 1001, "amplitude", 0.2, "frequency", 880),
                ),
                timestamp=cur_time + provider.latency + 0.5,
            ),
        ),
    ]


# Make sure no message is lost under heavy load
async def test_RealtimeProvider_async_set_node_02(async_server):
    provider = supriya.Provider.from_context(async_server)
    assert provider is not None

    async def set_node(n: int, synth_p: supriya.providers.SynthProxy):
        for i in range(n):
            async with synth_p.provider.at(time.time()):
                synth_p["frequency"] = random.randint(20, 20000)
                await asyncio.sleep(random.random() * 0.001 + 0.0001)

    async with provider.at(time.time()):
        synth_p = provider.add_synth()
    await asyncio.sleep(provider.latency)
    with async_server.osc_protocol.capture() as transcript:
        aws = [set_node(128, synth_p) for _ in range(128)]
        await asyncio.gather(*aws)
    async with provider.at():
        provider.free_node(synth_p)
    # exclude /status msgs sent not in a bundle
    send_msgs = [
        _.message
        for _ in transcript
        if _.label == "S" and isinstance(_.message, OscBundle)
    ]
    assert len(send_msgs) == 128 * 128


# Make sure no message is lost under heavy load, quantised time
async def test_RealtimeProvider_async_set_node_03(async_server):
    provider = supriya.Provider.from_context(async_server)
    assert provider is not None

    async def set_node(n: int, synth_p: supriya.providers.SynthProxy):
        for i in range(n):
            cur_time = time.time()
            cur_time_rem = cur_time - (cur_time % 0.01) + 0.01
            async with synth_p.provider.at(cur_time_rem):
                synth_p["frequency"] = random.randint(20, 2000)
            await asyncio.sleep(random.random() * 0.001 + 0.0001)

    async with provider.at(time.time()):
        synth_p = provider.add_synth()
    await asyncio.sleep(provider.latency)
    with async_server.osc_protocol.capture() as transcript:
        aws = [set_node(123, synth_p) for _ in range(78)]
        await asyncio.gather(*aws)
    async with provider.at():
        provider.free_node(synth_p)
    # exclude /status msgs sent not in a bundle
    send_msgs = [
        _.message
        for _ in transcript
        if _.label == "S" and isinstance(_.message, OscBundle)
    ]
    assert len(send_msgs) == 123 * 78
    assert len(set([_.timestamp for _ in send_msgs])) < 123 * 78
