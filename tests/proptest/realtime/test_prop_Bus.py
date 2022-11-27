from dataclasses import dataclass
from typing import Any, Optional, Tuple

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
class SampleBus(TestSample):
    bus: supriya.realtime.Bus
    calculation_rate: CalculationRate
    bus_group_or_index: Optional[int] = None
    set_value: float = 0.0
    bus_index_min: int = 0
    bus_index_max: int = 16383


@get_CTGr(max_size=64)
def st_bus(
    draw: st.DrawFn,
    calculation_rates: Tuple[Any, ...] = (
        (CalculationRate.AUDIO, CalculationRate.CONTROL)
    ),
    user_id: bool = False,
) -> SampleBus:

    if user_id:
        bus_group_or_index = draw(
            st.integers(
                min_value=SampleBus.bus_index_min, max_value=SampleBus.bus_index_max
            )
        )
    else:
        bus_group_or_index = None
    calculation_rate = draw(st.sampled_from(calculation_rates))
    bus = supriya.realtime.Bus(
        bus_group_or_index=bus_group_or_index, calculation_rate=calculation_rate
    )
    sample = SampleBus(bus, calculation_rate)

    sample.set_value = draw(st.floats(width=32, allow_infinity=False, allow_nan=False))
    sample.bus_group_or_index = bus_group_or_index

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_bus(calculation_rates=(CalculationRate.CONTROL,)))
def test_getset(server: Server, strategy: CTGr[SampleBus]) -> None:

    control, test = strategy

    assert all(_.bus.allocate(server) for _ in control + test)
    assert all(_.bus.is_allocated for _ in control + test)
    control_vals = tuple(_.bus.get() for _ in control)

    for sample in test:
        sample.bus.set(sample.set_value)
        assert sample.bus.get() == sample.set_value
        assert sample.bus.value == sample.set_value

    assert control_vals == tuple(_.bus.get() for _ in control)
    assert all(_.bus.free() for _ in control + test)
    assert not any(_.bus.is_allocated for _ in control + test)
