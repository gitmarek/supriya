import sys

import hypothesis as hp
import hypothesis.strategies as st
import pytest

import supriya
from supriya.providers import (
    NonrealtimeProvider,
    Provider,
    ProviderMoment,
    RealtimeProvider,
)
from supriya.scsynth import Options
from tests.confhp import st_seconds, suppress_hp_server_fixture_chk

supernova_skip_win = pytest.param(
    "supernova",
    marks=pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Supernova won't boot on Windows"
    ),
)


def test_Provider_from_context(session, server):
    realtime_provider = Provider.from_context(server)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server is server
    nonrealtime_provider = Provider.from_context(session)
    assert isinstance(nonrealtime_provider, NonrealtimeProvider)
    assert nonrealtime_provider.session is session
    with pytest.raises(ValueError):
        Provider.from_context(23)


@hp.given(seconds=st_seconds)
@suppress_hp_server_fixture_chk
def test_Provider_at_seconds_01(session, server, seconds):
    realtime_provider = Provider.from_context(server)
    moment = realtime_provider.at(seconds)
    assert isinstance(moment, ProviderMoment)
    assert moment.provider is realtime_provider
    assert moment.seconds == seconds
    nonrealtime_provider = Provider.from_context(session)
    moment = nonrealtime_provider.at(seconds)
    assert isinstance(moment, ProviderMoment)
    assert moment.provider is nonrealtime_provider
    assert moment.seconds == seconds


@hp.given(
    seconds=st.one_of(
        st.floats(
            max_value=0.0, exclude_max=True, allow_infinity=False, allow_nan=False
        ),
        st.floats(
            min_value=supriya.providers.MAX_SECONDS,
            exclude_min=True,
            allow_infinity=False,
            allow_nan=False,
        ),
    )
)
def test_Provider_at_seconds_02(seconds):
    server = supriya.Server()
    realtime_provider = Provider.from_context(server)
    with pytest.raises(ValueError):
        _ = realtime_provider.at(seconds)
    session = supriya.Session()
    nonrealtime_provider = Provider.from_context(session)
    with pytest.raises(ValueError):
        _ = nonrealtime_provider.at(seconds)


@pytest.mark.parametrize("executable", [None, supernova_skip_win])
def test_Provider_realtime(executable):
    options = Options(executable=executable)
    realtime_provider = Provider.realtime(options=options)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner


@pytest.mark.asyncio
@pytest.mark.parametrize("executable", [None, supernova_skip_win])
async def test_Provider_realtime_async(executable):
    options = Options(executable=executable)
    realtime_provider = await Provider.realtime_async(options=options)
    assert isinstance(realtime_provider, RealtimeProvider)
    assert realtime_provider.server.is_running
    assert realtime_provider.server.is_owner
    await realtime_provider.server.quit()
    assert not realtime_provider.server.is_running
    assert not realtime_provider.server.is_owner
