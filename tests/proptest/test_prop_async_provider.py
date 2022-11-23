import hypothesis
import hypothesis.strategies as st
import pytest
import pytest_asyncio

import supriya
from supriya.osc import OscBundle, OscMessage
from tests.proptest import hp_global_settings


@pytest.fixture(autouse=True)
def shutdown_async_servers(shutdown_scsynth, event_loop):
    pass


@pytest_asyncio.fixture
async def async_server(persistent_async_server):
    serv = persistent_async_server
    # TODO: AsyncServ.reset()
    serv.send(["/g_freeAll", 0])
    await serv._setup_default_groups()
    yield serv


hp_settings = hypothesis.settings(
    hp_global_settings,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
)


st_seconds = st.floats(
    min_value=10.0, max_value=111111, width=32, allow_infinity=False, allow_nan=False
)


@hypothesis.settings(hp_settings)
@hypothesis.given(seconds=st_seconds)
@pytest.mark.asyncio
async def test_RealtimeProvider_async_set_node_01(async_server, seconds):

    provider = supriya.Provider.from_context(async_server)
    assert provider is not None
    with async_server.osc_protocol.capture() as transcript:
        async with provider.at(seconds + 1):
            async with provider.at(seconds):
                synth_p = provider.add_synth(frequency=440)
            provider.free_node(synth_p)

    assert [(_.label, _.message) for _ in transcript] == [
        (
            "S",
            OscBundle(
                contents=(OscMessage("/s_new", "default", synth_p.identifier, 0, 1),),
                timestamp=seconds + provider.latency,
            ),
        ),
        (
            "S",
            OscBundle(
                contents=(OscMessage("/n_set", synth_p.identifier, "gate", 0),),
                timestamp=seconds + provider.latency + 1.0,
            ),
        ),
    ]
