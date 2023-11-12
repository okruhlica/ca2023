from random import shuffle


class RandomGuesser:
    NAME = "Random Guesser"

    def __init__(self, ask_fn, gamedef):
        self.ask_fn = ask_fn

        self.fleet = gamedef.fleet
        self.rows = gamedef.rows
        self.cols = gamedef.cols

        self.hits = 0
        self.needed = gamedef.hits_needed
        self.moves = []

        for y in range(self.rows):
            for x in range(self.cols):
                self.moves.append((y, x))
        shuffle(self.moves)

    def move(self):
        if not len(self.moves):
            return False

        y, x = self.moves.pop()
        response = self.ask_fn(y, x)
        if response.cell == 'X':
            self.hits += 1
        return True
