""" 
Simulation
----------

The simulation class is the main class of the simulation. It is responsible for
initializing the simulation, running the simulation, and displaying the results.
"""

import traceback
from datetime import datetime
from statistics import mean

from sdk.base.reality import Reality
from sdk.core import Condition


class Simulation(Reality):
    """
    The simulation class is the main class of the simulation. It is responsible for
    initializing the simulation, running the simulation, and displaying the results.

    Parameters
    ----------
    settings: dict
        The settings for the simulation.

    Attributes
    ----------
    running: bool
        Whether the simulation is running or not.
    cycles: int
        The number of cycles that have passed.

    Methods
    -------
    setup()
        Setup the simulation.
    step()
        Advance the simulation by one cycle.
    cycle()
        Advance the simulation by one cycle.
    run_simulation()
        Run the simulation for a specified number of steps.
    post_simulation()
        Post cycle processes. Like sending data to a postgres db
    reset()
        Reset the simulation object, using the current parameters.
    stop()
        Stop the simulation.
    get_results()
        Get the step results of the simulation.
    generate_id()
        Generate a new id for an object.
    random_dooder()
        Get a random dooder from the simulation.
    stop_conditions()
        Check if the simulation should stop.
    log(granularity, message, scope)
        Log a message to the logger.
    simulation_summary()
        Get a summary of the simulation.
    """

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self.running = False
        self.cycles: int = 0

    def setup(self) -> None:
        """
        Setup the simulation.
        1. Spawn the dooders
        2. Spawn the energy
        3. Set simulation running to true
        4. Collect initial state
        """
        self.resources.allocate_resources()
        self.arena.generate_seed_population()

        self.running = True

        self.information.collect(self)

    def step(self) -> None:
        """
        Advance the simulation by one cycle.

        1. Advance every agent by a step
        2. Collect data at the end of the cycle
        3. Place new energy
        4. Collect stats
        5. Increment cycle counter   
        """
        # advance every agent by a step
        self.time.step()

        # collect data at the end of the cycle
        self.information.collect(self)

        # place new energy
        self.resources.step()

        # collect stats
        self.arena.step()

        self.cycles += 1

    def cycle(self) -> None:
        """ 
        Advance the simulation by one cycle.
        """
        if self.stop_conditions():
            self.step()

    def run_simulation(self) -> None:
        """
        Run the simulation for a specified number of steps.

        1. Setup the simulation
        2. Run the simulation until the stop conditions are met
        3. Collect the results
        """
        self.starting_time = datetime.now()
        try:
            self.setup()

            while self.stop_conditions():
                self.step()
        except Exception as e:
            print(traceback.format_exc())
            print('Simulation failed')

        self.ending_time = datetime.now()

    def reset(self) -> None:
        """
        Reset the simulation object, using the current parameters.

        This is useful for resetting the simulation after a parameter change.
        """
        self.__init__(self.simulation_id, self.params)

    def stop(self) -> None:
        """
        Stop the simulation.
        """
        self.running = False

    def get_results(self) -> dict:
        """
        Get the step results of the simulation.

        Returns
        -------
        dict
            A dictionary of the results of the simulation.
        """
        return self.information.get_result_dict(self)

    def generate_id(self) -> int:
        """
        Generate a new id for an object.

        Returns
        -------
        int
            A new id for an object.
        """
        return self.seed.uuid()

    def random_dooder(self):
        """
        Get a random dooder from the simulation.

        Returns
        -------
        Dooder
            A random dooder from the simulation.
        """
        return self.arena.get_dooder()

    def stop_conditions(self) -> bool:
        """
        Check if the simulation should stop.

        Returns
        -------
        bool
            Whether the simulation should stop or not.
        """
        result, reason = Condition.check('stop', self)

        if result:
            self.stop()
            self.log(
                1, f"Simulation stopped because of {reason}", 'Simulation')

            return False

        else:
            return True

    def log(self, granularity: int, message: str, scope: str) -> None:
        """ 
        Log a message to the logger.

        Parameters
        ----------
        granularity: int
            The granularity of the message.
        message: str
            The message to log.
        scope: str
            The scope of the message.
        """
        cycle_number = self.time.time

        log_dict = {
            'Scope': scope,
            'CycleNumber': cycle_number,
            'Granularity': granularity,
            'Message': message
        }

        final_message = str(log_dict).strip('{}')

        self.information.log(final_message, granularity)

    def simulation_summary(self) -> dict:
        """ 
        Get a summary of the simulation.

        Returns
        -------
        dict
            A dictionary of the summary of the simulation.
        """
        return {'SimulationID': self.simulation_id,
                'Timestamp': datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                'CycleCount': self.cycles,
                'TotalEnergy': sum(self.information.data['resources']['allocated_energy']),
                'ConsumedEnergy': sum(self.information.data['resources']['consumed_energy']),
                'StartingDooderCount': self.information.data['arena']['created_dooder_count'][0],
                'EndingDooderCount': len(self.arena.active_dooders),
                'ElapsedSeconds': int((self.ending_time - self.starting_time).total_seconds()),
                'AverageAge': int(mean([d.age for d in self.arena.graveyard.values()])),
                }

    @property
    def cycle_number(self) -> int:
        """ 
        Get the current cycle number.

        Returns
        -------
        int
            The current cycle number.
        """
        return self.cycles

    @property
    def state(self) -> dict:
        """ 
        Get the current state of the simulation.

        Returns
        -------
        dict
            The current state of the simulation.
        """
        return {
            'simulation_id': self.simulation_id,
            'settings': self.settings,
            'running': self.running,
            'starting_time': str(self.starting_time),
            'ending_time': str(self.ending_time),
            'arena': self.arena.state
        }
