# -*- encoding: utf-8 -*-
from supriya.tools.osctools.OscCallback import OscCallback


class BufferResponseCallback(OscCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        OscCallback.__init__(
            self,
            address_pattern='/b_(info|set|setn)',
            procedure=self.__call__,
            )
        assert isinstance(server, servertools.Server)
        self._server = server

    ### SPECIAL METHODS ###

    def __call__(self, message):
        from supriya.tools import responsetools
        responses = responsetools.ResponseManager.handle_message(message)
        if not isinstance(responses, tuple):
            responses = (responses,)
        for response in responses:
            buffer_id = response.buffer_id
            buffer_proxy = self._server._get_buffer_proxy(buffer_id)
            buffer_proxy.handle_response(response)