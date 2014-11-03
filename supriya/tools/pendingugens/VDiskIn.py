# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class VDiskIn(MultiOutUGen):

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
        bufnum=None,
        channel_count=None,
        loop=0,
        rate=1,
        send_id=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            loop=loop,
            rate=rate,
            send_id=send_id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=None,
        channel_count=None,
        loop=0,
        rate=1,
        send_id=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            loop=loop,
            rate=rate,
            send_id=send_id,
            )
        return ugen
