from typing import Any, Callable, Optional, ParamSpec

import hypothesis
import hypothesis.strategies as st

F = Callable[..., Any]
P = ParamSpec("P")

hp_global_settings = hypothesis.settings()


def get_control_test_groups(
    min_size: int = 1, max_size: Optional[int] = None
) -> Callable[[F], F]:
    def _wrapper(func: F) -> F:
        def _st_func(*args: P.args, **kwargs: P.kwargs) -> st.SearchStrategy[Any]:
            strategy = func(*args, **kwargs)
            return st.tuples(
                st.lists(strategy, min_size=min_size, max_size=max_size),
                st.lists(strategy, min_size=min_size, max_size=max_size),
            )

        return _st_func

    return _wrapper
