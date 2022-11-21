import itertools
from dataclasses import dataclass
from typing import List, Optional, Tuple

import hypothesis
import hypothesis.strategies as st

import supriya.realtime

from tests.proptest import hp_global_settings


import supriya.realtime

hp_settings = hypothesis.settings(hp_global_settings)


@dataclass
class Sample:
    allocator: supriya.realtime.BlockAllocator
    heap_minimum: int = 0
    heap_maximum: int = 1048576
    heap_min_size: int = 1
    block_sizes: Tuple[int] = (1,)
    allocate_at_indices: Tuple[int] = (1,)
    free_at_indices: Tuple[int] = (1,)


@st.composite
def st_block_allocator(draw):

    heap_minimum = draw(
        st.integers(min_value=Sample.heap_minimum, max_value=Sample.heap_maximum - Sample.heap_min_size)
    )
    heap_maximum = draw(
        st.integers(min_value=heap_minimum + Sample.heap_min_size, max_value=Sample.heap_maximum)
    )
    allocator = supriya.realtime.BlockAllocator(
        heap_minimum=heap_minimum, heap_maximum=heap_maximum
    )

    sample = Sample(allocator, heap_minimum=heap_minimum, heap_maximum=heap_maximum)

    sample.block_sizes = tuple(
        draw(
            st.lists(
                st.integers(min_value=1, max_value=heap_maximum - heap_minimum),
                min_size=1,
            )
        )
    )
    st_indices = st.lists(
        st.integers(min_value=heap_minimum, max_value=heap_maximum), min_size=1, unique=True
    )
    sample.allocate_at_indices = tuple(draw(st_indices))
    sample.free_at_indices = tuple(draw(st_indices))

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(sample=st_block_allocator())
def test_allocate_01(sample):

    available_blocks = sample.heap_maximum - sample.heap_minimum
    allocated_blocks = 0
    for size in sample.block_sizes:
        result = sample.allocator.allocate(size)
        if allocated_blocks + size > available_blocks:
            assert result is None
            break
        else:
            assert result == sample.heap_minimum + allocated_blocks
        allocated_blocks += size

# #######
# WIP
#
# @hypothesis.settings(hp_settings, suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
# @hypothesis.given(sample=st_block_allocator())
# def test_allocate_02(sample):

#     available_blocks = {
#         _: True for _ in range(sample.heap_minimum, sample.heap_maximum)
#     }
#     for size, index in zip(sample.block_sizes, sample.allocate_at_indices):
#         hypothesis.assume(index + size < sample.heap_maximum)

#         # Without this assumption, allocate_at() would throw AssertionError
#         if not any(available_blocks[_] for _ in range(index, index+size)):
#             continue

#         result = sample.allocator.allocate_at(index, size)
#         if not all(available_blocks[_] for _ in range(index, index+size)):
#             assert result is None
#         else:
#             assert result == index
#             available_blocks.update({_: False for _ in range(index, index+size)})


