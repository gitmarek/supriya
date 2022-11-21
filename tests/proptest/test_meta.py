from dataclasses import dataclass

import hypothesis
import hypothesis.strategies as st

from tests.proptest import get_control_test_groups, hp_global_settings

hp_settings = hypothesis.settings(hp_global_settings)


@dataclass
class Sample:

    val_bool: bool
    val_int: int
    val_float: float = 0.0
    val_text: str = ""


@get_control_test_groups()
@st.composite
def st_test_strategy_01(draw):

    sample = Sample(draw(st.booleans()), draw(st.integers()))

    sample.val_float = draw(st.floats(allow_infinity=False, allow_nan=False))
    sample.val_text = draw(st.text())

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_test_strategy_01())
def test_composite_strategy_01(strategy):

    assert isinstance(strategy, tuple)
    assert len(strategy) == 2
    control, test = strategy
    assert isinstance(control, list)
    assert isinstance(test, list)
    assert len(control) >= 1
    assert len(test) >= 1
    assert all(isinstance(_, Sample) for _ in control + test)
    assert all(isinstance(_.val_bool, bool) for _ in control + test)
    assert all(isinstance(_.val_int, int) for _ in control + test)
    assert all(isinstance(_.val_float, float) for _ in control + test)
    assert all(isinstance(_.val_text, str) for _ in control + test)
