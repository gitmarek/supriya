import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import UGen


class Tap(UGen):
    """

    ::

        >>> tap = supriya.ugens.Tap.ar(
        ...     buffer_id=0,
        ...     channel_count=1,
        ...     delay_time=0.2,
        ...     )
        >>> tap
        Tap.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'buffer_id',
        'channel_count',
        'delay_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        channel_count=1,
        delay_time=0.2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            delay_time=delay_time,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        channel_count=1,
        delay_time=0.2,
        ):
        """
        Constructs an audio-rate Tap.

        ::

            >>> tap = supriya.ugens.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap
            Tap.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            channel_count=channel_count,
            delay_time=delay_time,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of Tap.

        ::

            >>> tap = supriya.ugens.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of Tap.

        ::

            >>> tap = supriya.ugens.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def delay_time(self):
        """
        Gets `delay_time` input of Tap.

        ::

            >>> tap = supriya.ugens.Tap.ar(
            ...     buffer_id=0,
            ...     channel_count=1,
            ...     delay_time=0.2,
            ...     )
            >>> tap.delay_time
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('delay_time')
        return self._inputs[index]
