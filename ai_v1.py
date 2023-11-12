from random import shuffle


class RandomGuesser:
    NAME = "Random Guesser"
    def __init__(self, ask_fn):
        self.hits = 0
        self.ask_fn = ask_fn
        self.moves = []
        for y in range(12):
            for x in range(12):
                self.moves.append((y, x))
        shuffle(self.moves)

    def move(self):
        if not len(self.moves):
            return False

        y, x = self.moves.pop()
        result = self.ask_fn(y, x)
        if result:
            self.hits += 1
        return True
