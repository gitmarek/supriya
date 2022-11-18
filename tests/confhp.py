import hypothesis as hp
import hypothesis.strategies as st

from supriya.providers import MAX_SECONDS, MIN_SECONDS

suppress_hp_server_fixture_chk = hp.settings(
    suppress_health_check=[hp.HealthCheck.function_scoped_fixture]
)

# ### Hypothesis strategies ### #

st_f32_fin = st.floats(width=32, allow_infinity=False, allow_nan=False)

st_seconds = st.one_of(
    st.none(),
    st.floats(
        min_value=MIN_SECONDS,
        max_value=MAX_SECONDS,
        allow_infinity=False,
        allow_nan=False,
    ),
)
