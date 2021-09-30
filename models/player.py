from tinydb import TinyDB, Query


class Player:
    def __init__(self, dict_init):
        self.last_name = dict_init["last_name"]
        self.first_name = dict_init["first_name"]
        self.birthday = dict_init["birthday"]
        self.gender = dict_init["gender"]
        self.ranking = dict_init["ranking"]

    def serialization(self):
        serialized_player = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "ranking": self.ranking,
        }
        return serialized_player

    def modification_ranking(self, ranking):
        self.ranking = ranking

    def save_table(self):
        serialized_player = self.serialization()
        TinyDB("tables.json").table("players").\
            upsert(serialized_player, (Query().last_name == self.last_name) &
                                      (Query().first_name == self.first_name))
