from dataclasses import dataclass
from typing import List, Optional

import hypothesis
import hypothesis.strategies as st
import pytest

import supriya.assets
import supriya.realtime
import supriya.synthdefs
from tests.proptest import get_control_test_groups, hp_global_settings


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


hp_settings = hypothesis.settings(
    hp_global_settings,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
    deadline=999,
)


@dataclass
class SampleGroup:
    group: supriya.realtime.Group
    allocate_pattern: List[bool]
    name: Optional[str] = None
    node_id_is_permanent: bool = False
    parallel: bool = False


@get_control_test_groups(min_size=1, max_size=64)
@st.composite
def st_group(draw) -> SampleGroup:

    name = draw(st.one_of(st.text(), st.none()))
    node_id_is_permanent = draw(st.booleans())
    parallel = draw(st.booleans())
    group = supriya.realtime.Group(name=name, parallel=parallel)
    allocate_pattern = draw(st.lists(st.booleans(), min_size=8, max_size=128))
    sample = SampleGroup(
        group,
        name=name,
        node_id_is_permanent=node_id_is_permanent,
        parallel=parallel,
        allocate_pattern=allocate_pattern,
    )

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_group())
def test_allocate_01(server, strategy):

    control, test = strategy

    for sample in control:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent
        assert sample.group.name == sample.name
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
        assert sample.group.name == sample.name

    for sample in control:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_group())
def test_allocate_02(server, strategy):

    control, test = strategy

    for sample in test + control:
        sample.group.allocate(server)
    server.sync()

    for sample in control:
        assert sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server == server
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name

    for sample in test:
        sample.group.free()
    server.sync()
    for sample in test:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent
        assert sample.group.name == sample.name
        assert sample.group.parallel == sample.parallel

    for sample in control:
        assert sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server == server
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_group())
def test_allocate_03(server, strategy):

    control, test = strategy

    for sample in test + control:
        sample.group.allocate(server)
    server.sync()

    for sample in control:
        assert sample.group.is_allocated

    for allocate_frame in zip(*(_.allocate_pattern for _ in test)):
        for i, should_allocate in enumerate(allocate_frame):
            sample = test[i]
            if should_allocate:
                sample.group.allocate(server)
                # Fun time! Uncomment this to listen to the test:
                # import random
                # synth_a = supriya.realtime.Synth(
                #    amplitude=0.01,
                #    frequency=random.uniform(80, 500),
                #    pan=random.random(),
                # )
                #  sample.group.append(synth_a)
            else:
                sample.group.free()
        server.sync()
        for i, should_allocate in enumerate(allocate_frame):
            assert test[i].group.is_allocated is should_allocate

    for sample in control:
        assert sample.group.is_allocated
