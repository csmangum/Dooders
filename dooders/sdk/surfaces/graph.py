"""
Space: Graph
------------
"""

from functools import singledispatchmethod
import networkx as nx
from typing import Any, Dict, Iterator, List, Optional, Union, NamedTuple
import matplotlib.pyplot as plt

from dooders.sdk.modules.space import Space

import random


class Coordinate(NamedTuple):
    X: int
    Y: int


# def heuristic(a, b):
#     """Manhattan distance on a grid."""
#     print(f'a: {a}, b: {b}')
#     (x1, y1) = a
#     (x2, y2) = b
#     return abs(x1 - x2) + abs(y1 - y2)


class Graph:
    """
    A graph is a collection of nodes (vertices) along with identified pairs of
    nodes (called edges, links, etc).

    Parameters
    ----------
    settings: dict, {torus: bool, width: int, height: int}
        A dictionary of settings for the grid.
        The following settings are available:
        torus: bool, default: True
            A boolean indicating if the grid is a torus.
            Torus grids wrap around the edges.
        width: int, default: 10
            The width of the grid.
        height: int, default: 10
            The height of the grid.

    Attributes
    ----------
    torus: bool
        See settings.
    width: int
        See settings.
    height: int
        See settings.
    _graph: nx.Graph
        The graph object.
    _object_index: Dict[str, Coordinate]
        A dictionary mapping object names to coordinates.

    Methods
    -------
    _build()
        Creates a grid graph.
    coordinate_to_node_label(x, y)
        Converts a coordinate to a node label.
    add(object, coordinate)
        Adds an object to the graph and updates the object index.
    remove(object)
        Removes an object from the graph and updates the object index.
    coordinates()
        Return an iterator over all coordinates in the grid.
    spaces()
        Return an iterator over all spaces in the grid.
    contents(type=None)
        Return an iterator over all contents in the grid.
    contents(position)
        Return an iterator over all contents in a Space on the grid.
    out_of_bounds(position)
        Returns True if the position is out of bounds.
    nearby_spaces(position)
        Return an iterator over all nearby spaces in the grid.
    get_neighbors(node_label)
        Returns the neighbors of a node.
    __iter__()
        Return an iterator over all spaces in the grid.
    __getitem__(value: int)
        Return the space at the given index.
    __getitem__(value: Coordinate)
        Return the space at the given coordinate.
    __getitem__(value: list)
        Return the spaces at the given indices.
    __getitem__(value: str)
        Return the space at the given object id.
    state()
        Return the state of the graph.
    """

    _graph: nx.Graph
    _object_index: Dict[str, Coordinate]

    def __init__(self, settings: dict = {}) -> None:
        self.torus = settings.get("torus", False)
        self.height = settings.get("height", 5)
        self.width = settings.get("width", 5)
        self._graph = self._build()
        self._object_index = {}

        for setting in settings:
            if setting not in ["torus", "height", "width"]:
                setattr(self, setting, settings[setting])

        if hasattr(self, "map"):
            for space in self.spaces():
                x, y = space.coordinates
                tile_type = self.map[y][x]
                space.tile_type = tile_type

    def _build(self) -> nx.Graph:
        """
        Creates a grid graph.

        Returns
        -------
        G: nx.Graph
            A grid graph based on the settings (torus, width, height)
        """
        G = nx.grid_2d_graph(self.width, self.height)

        for node in G.nodes():
            G.nodes[node]["space"] = Space(*node)

        if self.torus:
            for x in range(self.height):
                G.add_edge((x, 0), (x, self.width - 1))
            for y in range(self.width):
                G.add_edge((0, y), (self.height - 1, y))

        return G

    def view(self):
        """
        Creates a view of the grid.

        Returns
        -------
        view: nx.Graph
            A view of the grid.
        """
        plt.figure(figsize=(15, 15))
        pos = {
            (x, y): (x, self.height - 1 - y)
            for x in range(self.width)
            for y in range(self.height)
        }
        nx.draw(
            self._graph,
            pos,
            with_labels=True,
            node_size=500,
            font_size=5,
            font_color="white",
            node_color="green",
        )
        plt.show()

    def heuristic(self, a, b):
        """Manhattan distance on a grid."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def add(self, object: object, coordinate: Coordinate) -> None:
        """
        Adds an object to the graph and updates the object index.

        Parameters
        ----------
        object: object
            The object to add.
        coordinate: Coordinate
            The coordinate to add the object to.
        """
        node = self._graph.nodes[coordinate]
        node["space"].add(object)
        self._object_index[object.id] = coordinate
        object.position = coordinate

    def path_finding(self, start: Coordinate, end: Coordinate) -> List[Coordinate]:
        """
        Finds a path between two coordinates.

        Parameters
        ----------
        start: Coordinate
            The starting coordinate.
        end: Coordinate
            The ending coordinate.

        Returns
        -------
        path: List[Coordinate]
            The path between the two coordinates.
        """
        path = nx.astar_path(self._graph, start, end, self.heuristic)
        return path[1:]

    def random(self):
        """
        Returns a random space.

        Returns
        -------
        space: Space
            A random space.
        """
        random_space = random.choice(list(self.spaces()))
        return random_space.coordinates

    @singledispatchmethod
    def remove(self, type: Union[object, str]) -> None:
        raise NotImplementedError(
            "You must pass either an object or an object id to remove."
        )

    @remove.register
    def _(self, object: object) -> None:
        """
        Removes an object from the graph and updates the object index.

        Parameters
        ----------
        object: object
            The object to remove.
        """
        node = self._graph.nodes[object.position]
        node["space"].remove(object)
        self._object_index.pop(object.id)

    @remove.register
    def _(self, object_id: str) -> None:
        """
        Removes an object from the graph and updates the object index.

        Parameters
        ----------
        object_id: str
            The object id to remove.
        """
        coordinate = self._object_index[object_id]
        node = self._graph.nodes[coordinate]
        node.space.remove(object_id)
        self._object_index.pop(object_id)

    def coordinates(self) -> Iterator[Coordinate]:
        """
        Return an iterator over all coordinates in the grid.

        Returns
        -------
        Iterator[Coordinate]
            An iterator over all coordinates in the grid.
            Example: [(0, 0), (0, 1), (0, 2), (0, 3)]

        Example
        -------
        for coordinate in grid.coordinates():
            print(coordinate)
        >>> (0, 0)
        >>> (0, 1)
        >>> (0, 2)
        """
        for node in self._graph.nodes:
            yield self._graph.nodes[node]["space"].coordinates

    def spaces(self) -> Iterator[Space]:
        """
        Return an iterator over all spaces in the grid.

        Returns
        -------
        Iterator[Space]
            An iterator over all spaces in the grid.
            Example: [Space(0, 0), Space(0, 1), Space(0, 2), Space(0, 3)]

        Example
        -------
        for space in grid.spaces():
            print(space)
        >>> Space(0, 0)
        >>> Space(0, 1)
        >>> Space(0, 2)
        """
        for node in self._graph.nodes:
            yield self._graph.nodes[node]["space"]

    @singledispatchmethod
    def contents(self, object_type: Union[str, None] = None):
        """
        Return an iterator over all contents in the grid.

        With no arguments, it will return all contents.
        Include an object type to return only that type of object.

        Parameters
        ----------
        type: Any, optional
            The type of contents to return. Defaults to all.
            object types include 'Dooder', 'Energy', etc.

        Returns
        -------
        Iterator[Any], [<Dooder>, <Energy>, <Dooder>, <Energy>]
            An iterator over all contents in the grid.

        Example
        -------
        for object in grid.contents():
            print(object)
        >>> <Dooder>
        >>> <Energy>
        >>> <Dooder>
        """
        if object_type is None:
            # Logic for no arguments
            for space in self.spaces():
                for object in space.contents:
                    yield object
        else:
            # Logic for when object_type is specified
            for space in self.spaces():
                for object in space.contents:
                    if object.__class__.__name__ == object_type:
                        yield object

    @contents.register
    def _(self, position: tuple):
        """
        Return an iterator over all contents in a Space on the grid.

        Parameters
        ----------
        position: Coordinate, (int, int)
            The position to get the contents from.

        Returns
        -------
        Iterator[Any], [<Dooder>, <Energy>, <Dooder>, <Energy>]
            An iterator over all contents in a Space on the grid.

        Example
        -------
        for object in grid.contents((0, 0)):
            print(object)
        >>> <Dooder>
        >>> <Energy>
        >>> <Dooder>
        """
        for object in self._graph.nodes[position]["space"].contents:
            yield object

    # @property
    # def contents(self):
    #     contents = []
    #     for space in self.spaces():
    #         for object in space.contents:
    #             contents.append(object)

    #     return contents

    def out_of_bounds(self, position: Coordinate) -> bool:
        """
        Returns True if the position is out of bounds.

        Parameters
        ----------
        position: Coordinate, (int, int)
            The position to check.

        Returns
        -------
        out_of_bounds: bool
            True if the position is out of bounds.
        """
        x, y = position
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def nearby_spaces(self, position: Coordinate) -> Iterator[Space]:
        """
        Return an iterator over all nearby spaces in the grid.

        Parameters
        ----------
        position: Coordinate, (int, int)
            The position to get the contents from.

        Returns
        -------
        Iterator[Space], [<Space>, <Space>, <Space>, <Space>]
            An iterator over all nearby spaces in the grid.

        Example
        -------
        for space in grid.nearby_spaces((0, 0)):
            print(space)
        >>> <Space>
        >>> <Space>
        >>> <Space>
        """
        for neighbor in self._graph.neighbors(position):
            yield self._graph.nodes[neighbor]["space"]

    def nearby_spaces(self, coordinate: "Coordinate") -> List[Space]:
        """
        Returns the neighbor spaces of a node.

        Parameters
        ----------
        node_label: int
            The node label.

        Returns
        -------
        neighbor_spaces: List[Space]
            A list of neighbor spaces.
        """
        neighbor_nodes = list(self._graph.neighbors(coordinate))
        neighbor_spaces = [
            self._graph.nodes[coordinate]["space"] for coordinate in neighbor_nodes
        ]
        return neighbor_spaces

    def get_neighbors(self, node_label: int) -> List[int]:
        """
        Returns the neighbors of a node.

        Parameters
        ----------
        node_label: int
            The node label.

        Returns
        -------
        neighbor_nodes: List[int]
            A list of neighbor nodes.
        """
        neighbor_nodes = list(self._graph.neighbors(node_label))
        return neighbor_nodes

    def __iter__(self) -> Iterator[Space]:
        """
        Return an iterator over all spaces in the grid.

        Returns
        -------
        Iterator[Space]
            An iterator over all spaces in the grid.
            Example: [Space(0, 0), Space(0, 1), Space(0, 2), Space(0, 3)]

        Example
        -------
        for space in grid:
            print(space)
        >>> Space(0, 0)
        >>> Space(0, 1)
        >>> Space(0, 2)
        """
        return self.spaces()

    @singledispatchmethod
    def __getitem__(self, value) -> Any:
        raise NotImplementedError(f"Type {type(value)} is unsupported")

    @__getitem__.register
    def _(self, value: int) -> Space:
        """
        Return the space at the given index.

        Parameters
        ----------
        value: int
            The index of the space.

        Returns
        -------
        space: Space
            The space at the given index.
        """
        return self._graph.nodes[value]["space"]

    @__getitem__.register
    def _(self, value: Coordinate) -> Space:
        """
        Return the space at the given coordinate.

        Parameters
        ----------
        value: Coordinate, (int, int)
            The coordinate of the space.

        Returns
        -------
        space: Space
            The space at the given coordinate.
        """
        return self._graph.nodes[value]["space"]

    @__getitem__.register
    def _(self, value: list) -> List[Space]:
        """
        Return the spaces at the given indices.

        Parameters
        ----------
        value: List[int]
            The indices of the spaces.

        Returns
        -------
        spaces: List[Space]
            The spaces at the given indices.
        """
        return [self._graph.nodes[node_label]["space"] for node_label in value]

    @__getitem__.register
    def _(self, value: str) -> Space:
        """
        Return the space at the given object id.

        Parameters
        ----------
        value: str
            The object id of the space.

        Returns
        -------
        space: Space
            The space at the given object id.
        """
        coordinate = self._object_index[value]
        return self._graph.nodes[coordinate]["space"]

    def draw(self, **kwargs) -> None:
        """
        Draw the graph.

        Parameters
        ----------
        kwargs: dict
            A dictionary of keyword arguments to pass to nx.draw.
        """
        nx.draw(self._graph, **kwargs)

    def state(self) -> Dict:
        """
        Return the state of the graph.

        Returns
        -------
        state: Dict
            The state of the graph.
        """
        return {
            "width": self.width,
            "height": self.height,
            "torus": self.torus,
            # 'spaces': {f'{space.x}-{space.y}': space.state for space in self.spaces()} # This takes up too much space
        }
