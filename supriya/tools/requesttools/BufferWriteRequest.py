# -*- encoding: utf-8 -*-
from supriya.tools.requesttools.Request import Request


class BufferWriteRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        from supriya.tools import requesttools
        manager = requesttools.RequestManager
        message = manager.make_buffer_write_message()
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_WRITE