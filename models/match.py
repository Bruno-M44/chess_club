from .player import Player


class Match:
    def __init__(self, dict_init):
        self.player_1 = Player(dict_init["player_1"])
        self.score_1 = dict_init["score_1"]
        self.player_2 = Player(dict_init["player_2"])
        self.score_2 = dict_init["score_2"]

    def serialization(self):
        serialized_match = {
            "player_1": self.player_1.serialization(),
            "score_1": self.score_1,
            "player_2": self.player_2.serialization(),
            "score_2": self.score_2
        }
        return serialized_match
