from dataclasses import dataclass
from typing import Optional

import hypothesis
import hypothesis.strategies as st
import pytest

import supriya.assets
import supriya.realtime
import supriya.synthdefs
from supriya import CalculationRate
from supriya.exceptions import BusAlreadyAllocated, BusNotAllocated, IncompatibleRate
from tests.proptest import get_control_test_groups, hp_global_settings


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    #persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


hp_settings = hypothesis.settings(
    hp_global_settings,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
)


@dataclass
class SampleGroup:
    group: supriya.realtime.Group
    name: Optional[str] = None
    parallel: bool = False


@get_control_test_groups(max_size=1024)
@st.composite
def st_group(draw) -> SampleGroup:

    name = draw(st.text())
    parallel = draw(st.booleans())
    group = supriya.realtime.Group(parallel=parallel)
    sample = SampleGroup(group, name=name, parallel=parallel)

    return sample


@hypothesis.settings(hp_settings, deadline=None)
@hypothesis.given(strategy=st_group())
def test_allocate_01(server, strategy):

    control, test = strategy

    for sample in control:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent 
        assert sample.group.parallel == sample.parallel

    for sample in test:
        sample.group.allocate(server)
    server.sync()
    for sample in test:
        assert sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server == server
        assert not sample.group.node_id_is_permanent 
        assert sample.group.parallel == sample.parallel
    for sample in test:
        sample.group.free()
    server.sync()
    assert not any(_.group.is_allocated for _ in test)


    for sample in control:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent 
        assert sample.group.parallel == sample.parallel

