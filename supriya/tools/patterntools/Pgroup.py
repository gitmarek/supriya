# -*- encoding: utf-8 -*-
import uuid
from abjad import new
from supriya.tools.patterntools.EventPattern import EventPattern


class Pgroup(EventPattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pattern',
        '_release_time',
        )

    ### INITIALIZER ###

    def __init__(self, pattern, release_time=0.25):
        self._pattern = pattern
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state):
        from supriya.tools import patterntools
        expr = super(Pgroup, self)._coerce_iterator_output(expr)
        if (
            isinstance(expr, patterntools.NoteEvent) or
            not expr.get('is_stop')
            ):
            kwargs = {}
            if expr.get('target_node') is None:
                kwargs['target_node'] = state['group_uuid']
            expr = new(expr, **kwargs)
        return expr

    def _iterate(self, state=None):
        return iter(self.pattern)

    def _setup_state(self):
        return {
            'group_uuid': uuid.uuid4(),
            }

    def _setup_peripherals(self, initial_expr, state):
        from supriya.tools import patterntools
        start_group_event = patterntools.GroupEvent(
            add_action='ADD_TO_HEAD',
            uuid=state['group_uuid'],
            )
        stop_group_event = patterntools.GroupEvent(
            uuid=state['group_uuid'],
            is_stop=True,
            )
        peripheral_starts = [start_group_event]
        peripheral_stops = []
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(patterntools.NullEvent(delta=delta))
        peripheral_stops.append(stop_group_event)
        return peripheral_starts, peripheral_stops

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def release_time(self):
        return self._release_time
