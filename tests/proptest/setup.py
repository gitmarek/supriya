from typing import Callable, TypeVar

import hypothesis
import hypothesis.strategies as st

T = TypeVar("T", covariant=True)
CTGr = tuple[list[T], list[T]]

hp_global_settings = hypothesis.settings()


class TestSample:
    ...


def get_CTGr(
    min_size: int = 1, max_size: int | None = None
) -> Callable[
    [Callable[..., st.SearchStrategy[TestSample]]],
    Callable[..., st.SearchStrategy[CTGr[TestSample]]],
]:
    def _wrapper(
        func: Callable[..., st.SearchStrategy[TestSample]]
    ) -> Callable[..., st.SearchStrategy[CTGr[TestSample]]]:
        def _st_func(*args, **kwargs) -> st.SearchStrategy[CTGr[TestSample]]:
            strategy: st.SearchStrategy[TestSample] = func(*args, **kwargs)
            return st.tuples(
                st.lists(strategy, min_size=min_size, max_size=max_size),
                st.lists(strategy, min_size=min_size, max_size=max_size),
            )

        return _st_func

    return _wrapper
