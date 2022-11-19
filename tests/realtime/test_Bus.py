import struct

import hypothesis as hp
import hypothesis.strategies as st
import pytest

import supriya.realtime
import supriya.synthdefs
from tests.confhp import st_f32_fin, suppress_hp_server_fixture_chk


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


def test_allocate_01(server):

    control_bus = supriya.realtime.Bus(calculation_rate=supriya.CalculationRate.CONTROL)

    assert control_bus.bus_group is None
    assert control_bus.bus_id is None
    assert control_bus.calculation_rate == supriya.CalculationRate.CONTROL
    assert control_bus.server is None
    assert not control_bus.is_allocated

    control_bus.allocate(server)

    assert control_bus.bus_group is None
    assert control_bus.bus_id == 0
    assert control_bus.calculation_rate == supriya.CalculationRate.CONTROL
    assert control_bus.server is server
    assert control_bus.is_allocated
    assert control_bus.map_symbol == "c0"

    control_bus.free()

    assert control_bus.bus_group is None
    assert control_bus.bus_id is None
    assert control_bus.calculation_rate == supriya.CalculationRate.CONTROL
    assert control_bus.server is None
    assert not control_bus.is_allocated


def test_allocate_02(server):

    audio_bus = supriya.realtime.Bus(calculation_rate=supriya.CalculationRate.AUDIO)

    assert audio_bus.bus_group is None
    assert audio_bus.bus_id is None
    assert audio_bus.calculation_rate == supriya.CalculationRate.AUDIO
    assert audio_bus.server is None
    assert not audio_bus.is_allocated

    audio_bus.allocate(server)

    assert audio_bus.bus_group is None
    assert audio_bus.bus_id == 16
    assert audio_bus.calculation_rate == supriya.CalculationRate.AUDIO
    assert audio_bus.server is server
    assert audio_bus.is_allocated
    assert audio_bus.map_symbol == "a16"

    audio_bus.free()

    assert audio_bus.bus_group is None
    assert audio_bus.bus_id is None
    assert audio_bus.calculation_rate == supriya.CalculationRate.AUDIO
    assert audio_bus.server is None
    assert not audio_bus.is_allocated


def test_allocate_03(server):

    bus = supriya.realtime.Bus(
        bus_group_or_index=23, calculation_rate=supriya.CalculationRate.CONTROL
    )

    assert bus.bus_id == 23
    assert bus.bus_group is None
    assert not bus.is_allocated
    assert bus.server is None

    bus.allocate(server)
    server.sync()

    assert bus.bus_id == 23
    assert bus.bus_group is None
    assert bus.is_allocated
    assert bus.server is server

    bus.free()
    server.sync()

    assert bus.bus_id is None
    assert bus.bus_group is None
    assert not bus.is_allocated
    assert bus.server is None


def test_allocate_04(server):

    bus_a = supriya.realtime.Bus(calculation_rate=supriya.CalculationRate.CONTROL)
    bus_b = supriya.realtime.Bus(calculation_rate=supriya.CalculationRate.CONTROL)
    bus_c = supriya.realtime.Bus(calculation_rate=supriya.CalculationRate.CONTROL)
    bus_d = supriya.realtime.Bus(calculation_rate=supriya.CalculationRate.CONTROL)

    assert bus_a.bus_id is None
    assert bus_b.bus_id is None
    assert bus_c.bus_id is None
    assert bus_d.bus_id is None
    assert bus_a.server is None
    assert bus_b.server is None
    assert bus_c.server is None
    assert bus_d.server is None

    bus_a.allocate(server)
    bus_b.allocate(server)
    bus_c.allocate(server)
    server.sync()

    assert bus_a.bus_id == 0
    assert bus_b.bus_id == 1
    assert bus_c.bus_id == 2
    assert bus_d.bus_id is None
    assert bus_a.server is server
    assert bus_b.server is server
    assert bus_c.server is server
    assert bus_d.server is None

    bus_c.free()
    bus_a.free()
    bus_d.allocate(server)
    server.sync()

    assert bus_a.bus_id is None
    assert bus_b.bus_id == 1
    assert bus_c.bus_id is None
    assert bus_d.bus_id == 0
    assert bus_a.server is None
    assert bus_b.server is server
    assert bus_c.server is None
    assert bus_d.server is server


@hp.given(set_val=st_f32_fin)
@suppress_hp_server_fixture_chk
def test_set(server, set_val):

    control_bus = server.add_bus()
    assert control_bus.is_allocated

    result = control_bus.get()
    assert result == 0.0
    assert control_bus.value == result

    control_bus.set(set_val)
    result = control_bus.get()
    assert result == set_val
    assert control_bus.value == result


@hp.given(set_val=st.floats())
@suppress_hp_server_fixture_chk
def test_set_double(server, set_val):

    control_bus = server.add_bus()
    assert control_bus.is_allocated

    restricted_value = struct.unpack("!f", struct.pack("!f", set_val))[0]
    control_bus.set(restricted_value)
    result = control_bus.get()
    assert result == restricted_value
