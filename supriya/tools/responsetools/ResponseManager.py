# -*- encoding: utf-8 -*-
import itertools
import sys
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ResponseManager(SupriyaObject):
    r'''Handles OSC responses from scsynth.

    ::

        >>> from supriya import osctools
        >>> from supriya import responsetools
        >>> manager = responsetools.ResponseManager()

    ::

        >>> message = osctools.OscMessage(
        ...     '/status.reply', 1, 0, 0, 2, 4,
        ...     0.040679048746824265, 0.15118031203746796,
        ...     44100.0, 44100.00077873274,
        ...     )
        >>> manager(message)
        StatusResponse(
            ugen_count=0,
            synth_count=0,
            group_count=2,
            synthdef_count=4,
            average_cpu_usage=0.040679048746824265,
            peak_cpu_usage=0.15118031203746796,
            target_sample_rate=44100.0,
            actual_sample_rate=44100.00077873274
            )

    ::

        >>> message = osctools.OscMessage('/b_info', 1100, 512, 1, 44100.0)
        >>> manager(message)[0]
        BufferInfoResponse(
            buffer_id=1100,
            frame_count=512,
            channel_count=1,
            sample_rate=44100.0
            )

    ::

        >>> message = osctools.OscMessage('/n_set', 1023, '/one', -1, '/two', 0)
        >>> manager(message)
        NodeSetResponse(
            node_id=1023,
            items=(
                NodeSetItem(
                    control_index_or_name='/one',
                    control_value=-1
                    ),
                NodeSetItem(
                    control_index_or_name='/two',
                    control_value=0
                    ),
                )
            )

    ::

        >>> message = osctools.OscMessage('/b_setn', 1, 0, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        >>> manager(message)
        BufferSetContiguousResponse(
            items=(
                BufferSetContiguousItem(
                    starting_sample_index=0,
                    sample_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                    ),
                ),
            buffer_id=1
            )

    ::

        >>> message = osctools.OscMessage('/g_queryTree.reply', 0, 0, 1, 1, 2, 1001, 0, 1000, 1, 1002, 0)
        >>> manager(message)
        QueryTreeGroup(
            node_id=0,
            children=(
                QueryTreeGroup(
                    node_id=1,
                    children=(
                        QueryTreeGroup(
                            node_id=1001,
                            children=()
                            ),
                        QueryTreeGroup(
                            node_id=1000,
                            children=(
                                QueryTreeGroup(
                                    node_id=1002,
                                    children=()
                                    ),
                                )
                            ),
                        )
                    ),
                )
            )

    ::

        >>> print(manager(message))
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 group

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_response_handlers'
        )

    ### INITIALIZER ###

    def __init__(self):
        self._response_handlers = {
            '/b_info': self._handle_b_info,
            '/b_set': self._handle_b_set,
            '/b_setn': self._handle_b_setn,
            '/c_set': self._handle_c_set,
            '/c_setn': self._handle_c_setn,
            '/d_removed': self._handle_d_removed,
            '/done': self._handle_done,
            '/fail': self._handle_fail,
            '/g_queryTree.reply': self._handle_g_query_tree_reply,
            '/n_end': self._handle_n_info,
            '/n_go': self._handle_n_info,
            '/n_info': self._handle_n_info,
            '/n_move': self._handle_n_info,
            '/n_off': self._handle_n_info,
            '/n_on': self._handle_n_info,
            '/n_set': self._handle_n_set,
            '/n_setn': self._handle_n_setn,
            '/status.reply': self._handle_status_reply,
            '/synced': self._handle_synced,
            '/tr': self._handle_tr,
            }

    ### SPECIAL METHODS ###

    def __call__(self, message):
        address, contents = message.address, message.contents
        if address in self._response_handlers:
            handler = self._response_handlers[address]
            response = handler(address, contents)
        else:
            raise ValueError(message)
        return response

    ### PRIVATE METHODS ###

    def _group_items(self, items, length):
        iterators = [iter(items)] * length
        if sys.version_info[0] == 2:
            iterator = itertools.izip(*iterators)
        else:
            iterator = zip(*iterators)
        return iterator

    def _handle_b_info(self, command, contents):
        from supriya.tools import responsetools
        responses = []
        for group in self._group_items(contents, 4):
            response = responsetools.BufferInfoResponse(*group)
            responses.append(response)
        responses = tuple(responses)
        return responses

    def _handle_b_set(self, command, contents):
        from supriya.tools import responsetools
        buffer_id, remainder = contents[0], contents[1:]
        items = []
        for group in self._group_items(remainder, 2):
            item = responsetools.BufferSetItem(*group)
            items.append(item)
        items = tuple(items)
        response = responsetools.BufferSetResponse(
            buffer_id=buffer_id,
            items=items,
            )
        return response

    def _handle_b_setn(self, command, contents):
        from supriya.tools import responsetools
        buffer_id, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            starting_sample_index = remainder[0]
            sample_count = remainder[1]
            sample_values = tuple(remainder[2:2 + sample_count])
            item = responsetools.BufferSetContiguousItem(
                starting_sample_index=starting_sample_index,
                sample_values=sample_values,
                )
            items.append(item)
            remainder = remainder[2 + sample_count:]
        items = tuple(items)
        response = responsetools.BufferSetContiguousResponse(
            buffer_id=buffer_id,
            items=items,
            )
        return response

    def _handle_c_set(self, command, contents):
        from supriya.tools import responsetools
        items = []
        for group in self._group_items(contents, 2):
            item = responsetools.ControlBusSetItem(*group)
            items.append(item)
        response = responsetools.ControlBusSetResponse(
            items=tuple(items),
            )
        return response

    def _handle_c_setn(self, command, contents):
        from supriya.tools import responsetools
        items = []
        while contents:
            starting_bus_index = contents[0]
            bus_count = contents[1]
            bus_values = tuple(contents[2:2 + bus_count])
            item = responsetools.ControlBusSetContiguousItem(
                starting_bus_index=starting_bus_index,
                bus_values=bus_values,
                )
            items.append(item)
            contents = contents[2 + bus_count:]
        items = tuple(items)
        response = responsetools.CSetnResponse(
            items=items,
            )
        return response

    def _handle_d_removed(self, command, contents):
        from supriya.tools import responsetools
        synthdef_name = contents[0]
        response = responsetools.SynthDefRemovedResponse(
            synthdef_name=synthdef_name,
            )
        return response

    def _handle_done(self, command, contents):
        from supriya.tools import responsetools
        arguments = contents
        response = responsetools.DoneResponse(action=tuple(arguments))
        return response

    def _handle_fail(self, command, contents):
        from supriya.tools import responsetools
        failed_command = contents[0]
        failed_reason = contents[1:]
        if failed_reason:
            failed_reason = tuple(failed_reason)
        response = responsetools.FailResponse(
            failed_command=failed_command,
            failed_reason=failed_reason,
            )
        return response

    def _handle_g_query_tree_reply(self, command, contents):
        def recurse(contents, control_flag):
            node_id = contents.pop(0)
            child_count = contents.pop(0)
            if child_count == -1:
                controls = []
                synthdef_name = contents.pop(0)
                if control_flag:
                    control_count = contents.pop(0)
                    for i in range(control_count):
                        control_name_or_index = contents.pop(0)
                        control_value = contents.pop(0)
                        control = responsetools.QueryTreeControl(
                            control_name_or_index=control_name_or_index,
                            control_value=control_value,
                            )
                        controls.append(control)
                controls = tuple(controls)
                result = responsetools.QueryTreeSynth(
                    node_id=node_id,
                    synthdef_name=synthdef_name,
                    controls=controls,
                    )
            else:
                children = []
                for i in range(child_count):
                    children.append(recurse(contents, control_flag))
                children = tuple(children)
                result = responsetools.QueryTreeGroup(
                    node_id=node_id,
                    children=children,
                    )
            return result
        from supriya.tools import responsetools
        contents = list(contents)
        control_flag = bool(contents.pop(0))
        response = recurse(contents, control_flag)
        return response

    def _handle_n_info(self, command, contents):
        from supriya.tools import responsetools
        arguments = (command,) + contents
        response = responsetools.NodeInfoResponse(*arguments)
        return response

    def _handle_n_set(self, command, contents):
        from supriya.tools import responsetools
        node_id, remainder = contents[0], contents[1:]
        items = []
        for group in self._group_items(remainder, 2):
            item = responsetools.NodeSetItem(*group)
            items.append(item)
        response = responsetools.NodeSetResponse(
            node_id=node_id,
            items=tuple(items),
            )
        return response

    def _handle_n_setn(self, command, contents):
        from supriya.tools import responsetools
        node_id, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            control_index_or_name = remainder[0]
            control_count = remainder[1]
            control_values = tuple(remainder[2:2 + control_count])
            item = responsetools.NodeSetContiguousItem(
                control_index_or_name=control_index_or_name,
                control_values=control_values,
                )
            items.append(item)
            remainder = remainder[2 + control_count:]
        items = tuple(items)
        response = responsetools.NodeSetContiguousResponse(
            node_id=node_id,
            items=items,
            )
        return response

    def _handle_status_reply(self, command, contents):
        from supriya.tools import responsetools
        arguments = contents[1:]
        response = responsetools.StatusResponse(*arguments)
        return response

    def _handle_synced(self, command, contents):
        from supriya.tools import responsetools
        arguments = contents
        response = responsetools.SyncedResponse(*arguments)
        return response

    def _handle_tr(self, command, contents):
        from supriya.tools import responsetools
        arguments = contents
        response = responsetools.TriggerResponse(*arguments)
        return response
