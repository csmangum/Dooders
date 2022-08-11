from mesa import Agent


class RandomMovement(Agent):
    """
    Class implementing random walker methods in a generalized manner.
    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, self.moore, True)

        origin = self.pos
        destination = self.random.choice(possible_moves)

        self.model.grid.move_agent(self, destination)

        return origin, destination

        # move check
        # if len(next_moves) > 0:

        #     if self.behavior.fate(self.behavior.MakeMoveProbability):
        #         next_move = self.random.choices(
        #             next_moves, weights=self.behavior.MoveDirectionDistribution, k=1)[0]
        #         self.model.grid.move_agent(self, next_move)

        #     else:
        #         pass
