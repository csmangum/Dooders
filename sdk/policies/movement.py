""" 
The movement policy is responsible for "deciding" where a Dooder will move during it's step
Currently there are three policies:
1. Random: The Dooder will move to a random location
2. Rule-based: The Dooder will move to a location based on a set of rules
3. Neural Network: The Dooder will move to a location based on a neural network output
"""

from random import choice
from typing import TYPE_CHECKING

from nets.model import base_model
from sdk.base.base_policy import BasePolicy
from sdk.core.policies import Policies
from sdk.models.energy import Energy

if TYPE_CHECKING:
    from sdk.models.dooder import Dooder


@Policies.register()
class RandomMove(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood
    A neighborhood is all surrounding positions, including the current position

    Args:
        dooder: The Dooder object to move

    Returns:
        A random location in the Dooder's neighborhood
    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood
        random_cell = choice(neighborhood.coordinates)

        return random_cell


@Policies.register()
class RuleBased(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood that has energy.
    A neighborhood is all surrounding positions, including the current position

    Args:
        dooder: The Dooder object to move

    Returns:
        A random location in the Dooder's neighborhood that has energy
    """
    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood
        energy = neighborhood.fetch('Energy')

        if energy:
            energy_positions = [e.position for e in energy]
            random_cell = choice(energy_positions)

        else:
            random_cell = dooder.position

        return random_cell


@Policies.register()
class NeuralNetwork(BasePolicy):
    """
    Given a Dooder object, returns a selected location based on neural network output

    Args:
        dooder: The Dooder object to move

    Returns:
        A location based on neural network output
    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood
        has_energy = neighborhood.contains('Energy')

        if hasattr(dooder, 'move_action'):
            model = dooder.move_action

        else:
            model = base_model()
            dooder.move_action = model

        output = model.forward(has_energy, training=True)
