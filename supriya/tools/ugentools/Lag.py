# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Rate import Rate
from supriya.tools.ugentools.Filter import Filter


class Lag(Filter):
    r'''A lag unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.kr(bus=0)
        >>> ugentools.Lag.kr(
        ...     lag_time=0.5,
        ...     source=source,
        ...     )
        Lag.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'lag_time',
        )

    _valid_rates = (
        Rate.AUDIO,
        Rate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lag_time=0.1,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            rate=rate,
            source=source,
            lag_time=lag_time,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        lag_time=None,
        rate=None,
        source=None,
        ):
        if lag_time == 0:
            return source
        source_rate = Rate.from_input(source)
        if source_rate == Rate.SCALAR:
            return source
        ugen = cls(
            lag_time=lag_time,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        lag_time=0.1,
        source=None,
        ):
        r'''Creates an audio-rate lag.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.Lag.ar(
            ...     lag_time=0.5,
            ...     source=source,
            ...     )
            Lag.ar()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            lag_time=lag_time,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        lag_time=0.1,
        source=None,
        ):
        r'''Creates a control-rate lag.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.Lag.kr(
            ...     lag_time=0.5,
            ...     source=source,
            ...     )
            Lag.kr()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            lag_time=lag_time,
            rate=rate,
            source=source,
            )
        return ugen