# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Pluck(UGen):

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
        coef=0.5,
        decaytime=1,
        delaytime=0.2,
        maxdelaytime=0.2,
        source=0,
        trigger=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            coef=coef,
            decaytime=decaytime,
            delaytime=delaytime,
            maxdelaytime=maxdelaytime,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coef=0.5,
        decaytime=1,
        delaytime=0.2,
        maxdelaytime=0.2,
        source=0,
        trigger=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coef=coef,
            decaytime=decaytime,
            delaytime=delaytime,
            maxdelaytime=maxdelaytime,
            source=source,
            trigger=trigger,
            )
        return ugen
