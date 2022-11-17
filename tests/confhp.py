import hypothesis as hp
import hypothesis.strategies as st

suppress_hp_server_fixture_chk = hp.settings(
    suppress_health_check=[hp.HealthCheck.function_scoped_fixture]
)

# ### Hypothesis strategies ### #

st_f32_fin = st.floats(width=32, allow_infinity=False, allow_nan=False)

st_seconds = st.one_of(
    st.just(None),
    st.floats(min_value=0.0, max_value=2**30, allow_infinity=False, allow_nan=False),
)
