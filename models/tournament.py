from tinydb import TinyDB, Query
from .tour import Tour
from .player import Player


class Tournament:
    def __init__(self, dict_init):
        self.name = dict_init["name"]
        self.place = dict_init["place"]
        self.start_date = dict_init["start_date"]
        self.end_date = dict_init["end_date"]
        if dict_init["number_of_tours"] == "":
            self.number_of_tours = 4
        else:
            self.number_of_tours = dict_init["number_of_tours"]
        self.tours = []
        for tour in dict_init["tours"]:
            self.tours.append(Tour(tour))
        self.players = []
        for player in dict_init["players"]:
            self.players.append(Player(player))
        self.time_control = dict_init["time_control"]
        self.description = dict_init["description"]

    def save_table(self):
        serialized_tournament = self.serialization()
        TinyDB("tables.json").table("tournaments").\
            upsert(serialized_tournament, Query().name == self.name)

    def serialization(self):
        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_tours": self.number_of_tours,
            "time_control": self.time_control,
            "description": self.description
        }
        serialized_players = []
        for player in self.players:
            serialized_players.append(player.serialization())
        serialized_tournament["players"] = serialized_players
        serialized_tours = []
        for tour in self.tours:
            serialized_tours.append(tour.serialization())
        serialized_tournament["tours"] = serialized_tours

        return serialized_tournament
