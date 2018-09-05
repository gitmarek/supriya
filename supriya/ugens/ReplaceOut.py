import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class ReplaceOut(UGen):
    """
    An overwriting bus output unit generator.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> supriya.ugens.ReplaceOut.ar(
        ...     bus=0,
        ...     source=source,
        ...     )
        ReplaceOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    _default_channel_count = 0

    _is_output = True

    _ordered_input_names = collections.OrderedDict([
        ('bus', 0),
        ('source', None),
    ])

    _unexpanded_input_names = (
        'source',
    )

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )
