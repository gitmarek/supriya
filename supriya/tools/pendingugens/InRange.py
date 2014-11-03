# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class InRange(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        hi=1,
        lo=0,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            hi=hi,
            lo=lo,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        hi=1,
        lo=0,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            hi=hi,
            lo=lo,
            source=source,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        hi=1,
        lo=0,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            hi=hi,
            lo=lo,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        hi=1,
        lo=0,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            hi=hi,
            lo=lo,
            source=source,
            )
        return ugen
