from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeVar

import hypothesis
import hypothesis.strategies as st

P = ParamSpec("P")
T = TypeVar("T")
CTGr = tuple[list[T], list[T]]

hp_global_settings = hypothesis.settings()


# Hypothesis strategies
st_f32_fin = st.floats(width=32, allow_infinity=False, allow_nan=False)


class TestSample:
    ...


def get_CTGr(
    min_size: int = 1, max_size: int | None = None
) -> Callable[
    [Callable[Concatenate[st.DrawFn, P], TestSample]],
    Callable[P, st.SearchStrategy[CTGr[TestSample]]],
]:
    def _wrapper(
        func: Callable[Concatenate[st.DrawFn, P], TestSample]
    ) -> Callable[P, st.SearchStrategy[CTGr[TestSample]]]:
        def __st_func(
            *args: P.args, **kwargs: P.kwargs
        ) -> st.SearchStrategy[CTGr[TestSample]]:
            strategy = st.composite(func)(*args, **kwargs)
            return st.tuples(
                st.lists(strategy, min_size=min_size, max_size=max_size),
                st.lists(strategy, min_size=min_size, max_size=max_size),
            )

        return __st_func

    return _wrapper
