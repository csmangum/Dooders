"""
Arena Model
-------------
Responsible for creation and management of Dooder objects in the simulation.   
"""

from typing import TYPE_CHECKING

import networkx as nx
from pydantic import BaseModel

from sdk.models import Dooder

if TYPE_CHECKING:
    from sdk.base.reality import BaseSimulation


class Attributes(BaseModel):
    dooders_created: int = 0
    dooders_died: int = 0


class Arena:
    """
    Class manages Dooder objects in the simulation.

    The class also keeps track of the total number of Dooders created and 
    terminated for each cycle. (The Information class will have historical 
    data for the above stats. The counts are reset after each cycle.) 

    Parameters
    ----------
    simulation : Simulation object
        The simulation object that contains the environment, agents, 
        and other models.

    Attributes
    ----------
    dooders_created : int
        The total number of Dooders created (for the current cycle).
    dooders_terminated: int
        The total number of Dooders terminated (for the current cycle).
    graph : networkx.Graph
        The graph object that contains the Dooder objects and relationships.
    active_dooders : dict
        Current active Dooders indexed by their unique id.
    graveyard : dict
        Current terminated Dooders indexed by their unique id.
    simulation: see ``Parameters`` section.
    seed : function
        The function that generates the seed population to start 
        the simulation.

    Methods
    -------
    step()
        Step the Arena forward. Currently, this will only reset attributes.
    reset()
        Reset main attributes after each cycle.
    generate_seed_population()
        Generate seed population based on the selected strategy.
    generate_dooder()
        Generate a new dooder and place it in the environment
    place_dooder()
        Place a dooder in the environment
    _generate_dooder()
        Generate a new dooder with a provided position
    """

    def __init__(self, simulation: 'BaseSimulation') -> None:
        self.graph = nx.Graph()
        self.active_dooders = {}
        self.graveyard = {}
        self.simulation = simulation

    def _setup(self) -> None:
        self.reset()  # set attributes

    def step(self) -> None:
        """
        Step the Arena forward. Currently, this will only reset attributes.
        """
        self.reset()

    def reset(self) -> None:
        """
        Reset main attributes after each cycle.
        """
        for attribute in Attributes():
            setattr(self, attribute[0], attribute[1])

    def generate_seed_population(self) -> None:
        """
        Generate seed population based on the selected strategy.
        """
        for position in self.SeedPlacement(self.SeedCount()):
            self.generate_dooder(position)

    def _generate_dooder(self, position: tuple) -> 'Dooder':
        """
        Generate a new dooder with a provided position

        Parameters
        ----------
        position : tuple 
            position to place dooder, (x, y)

        Returns
        -------
        Dooder: dooder object
            Newly generated Dooder object
        """
        dooder = Dooder(self.simulation.generate_id(),
                        position, self.simulation)
        return dooder

    def generate_dooder(self, position: tuple) -> None:
        """
        Generate a new dooder and place it in the environment

        Parameters
        ----------
        position : tuple
            position to place dooder, (x, y)
        """
        dooder = self._generate_dooder(position)
        self.place_dooder(dooder, position)
        dooder.log(granularity=1,
                   message=f"Created {dooder.id}", scope='Dooder')

    def place_dooder(self, dooder: 'Dooder', position: tuple) -> None:
        """
        Place dooder in environment

        The method will also add the dooder to the active_dooders dictionary
        and add the dooder to the graph for relationship tracking.

        Parameters
        ----------
        dooder : Dooder object 
        position : tuple
            position to place dooder, (x, y)
        """
        self.simulation.environment.place_object(dooder, position)
        self.simulation.time.add(dooder)

        self.active_dooders[dooder.id] = dooder

        #! TODO: Add more attributes to graph node
        self.graph.add_node(dooder.id)
        self.dooders_created += 1

    def terminate_dooder(self, dooder: 'Dooder') -> None:
        """
        Terminate dooder based on the unique id
        Removes from active_dooders, environment, and time

        Parameters
        ----------
        dooder_id : str
            dooder unique id, generated by the simulation
        """
        self.graveyard[dooder.id] = dooder
        self.active_dooders.pop(dooder.id)
        self.simulation.time.remove(dooder)
        self.simulation.environment.remove_object(dooder)
        self.dooders_died += 1

    def get_dooder(self, dooder_id: str = None) -> 'Dooder':
        """
        Get dooder based on the unique id, if no id is provided, a random dooder
        will be selected from the active dooders. If no active dooders are
        available, a random dooder will be selected from the graveyard.

        Parameters:
        ----------
        dooder_id : str
            dooder unique id, generated by the simulation

        Returns
        -------
        Dooder: dooder object
        """

        if dooder_id is None:
            if len(self.active_dooders) == 0:
                return self.simulation.random.choice(list(self.graveyard.values()))
            else:
                return self.simulation.random.choice(list(self.active_dooders.values()))
        else:

            return self.active_dooders[dooder_id]

    @property
    def active_dooder_count(self) -> int:
        """ 
        Returns the number of active dooders
        """
        return len(self.active_dooders)
    
    @property
    def state(self) -> dict:
        """
        Returns the state of the Arena
        """
        return {
            'active_dooders': {k:v.state for k,v in self.active_dooders.items()},
            # 'graveyard': {k:v.state for k,v in self.graveyard.items()},
            'settings': self.settings
        }
