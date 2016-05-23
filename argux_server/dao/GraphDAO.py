"""Data Access Object class for handling Graphs."""

from argux_server.models import (
    HistoryGraph
)

import argux_server.auth

from .BaseDAO import BaseDAO


class GraphDAO(BaseDAO):

    """GraphDAO Class."""

    def create_graph(self, name):

        graph = HistoryGraph(
            name=name)

        self.db_session.add(graph)

        self.db_session.flush()

        return graph

    def get_graph(self, graph_id):
        graph = self.db_session.query(HistoryGraph)\
            .filter(HistoryGraph.id==graph_id).first()

        return graph
