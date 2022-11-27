from dataclasses import dataclass
from typing import Tuple

import hypothesis
import hypothesis.strategies as st
import pytest

import supriya.assets
import supriya.realtime
import supriya.synthdefs
from supriya import CalculationRate
from supriya.realtime import Server

from tests.proptest.utils import CTGr, TestSample, get_CTGr, hp_global_settings


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
    deadline=1999,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
)


@dataclass
class SampleBusGroup(TestSample):
    bus_group: supriya.realtime.BusGroup
    calculation_rate: CalculationRate
    bus_count: int
    set_values: Tuple[float] = (0.0,)


@get_CTGr(max_size=64)
def st_bus_group(
    draw: st.DrawFn,
    max_bus_count=16,
    calculation_rates=((CalculationRate.AUDIO, CalculationRate.CONTROL)),
) -> SampleBusGroup:

    bus_count = draw(st.integers(min_value=1, max_value=max_bus_count))
    calculation_rate = draw(st.sampled_from(calculation_rates))
    bus_group = supriya.realtime.BusGroup(
        bus_count=bus_count, calculation_rate=calculation_rate
    )

    sample = SampleBusGroup(bus_group, calculation_rate, bus_count)
    sample.set_values = tuple(
        draw(st.floats(width=32, allow_infinity=False, allow_nan=False))
        for _ in range(bus_count)
    )

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus_group(calculation_rates=("control",)))
def test_getset(server: Server, strategy: CTGr[SampleBusGroup]) -> None:

    control, test = strategy

    assert all(_.bus_group.allocate(server) for _ in control + test)
    assert all(_.bus_group.is_allocated for _ in control + test)
    control_vals = tuple(_.bus_group.get() for _ in control)

    for sample in test:
        sample.bus_group.set(*sample.set_values)
        results = sample.bus_group.get()
        assert results == sample.set_values

    assert control_vals == tuple(_.bus_group.get() for _ in control)
    assert all(_.bus_group.free() for _ in control + test)
    assert not any(_.bus_group.is_allocated for _ in control + test)
