# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferFillRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_index_count_value_triples',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        index_count_value_triples=None,
        ):
        self._buffer_id = buffer_id
        triples = []
        for index, count, value in index_count_value_triples:
            triple = (int(index), int(count), float(value))
            triples.append(triple)
        triples = tuple(triples)
        self._index_count_value_triples = triples

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        for index, count, value in self.index_count_value_triples:
            contents.append(int(index))
            contents.append(int(count))
            contents.append(float(value))
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_value_triples(self):
        return self._index_count_value_triples

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_FILL