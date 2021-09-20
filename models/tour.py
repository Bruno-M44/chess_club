from .match import Match


class Tour:
    def __init__(self, dict_init):
        self.name = dict_init["name"]
        self.start_date = dict_init["start_date"]
        self.end_date = dict_init["end_date"]
        self.matches = []
        for match in dict_init["matches"]:
            self.matches.append(Match(match))

    def serialization(self):
        serialized_tour = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        serialized_matches = []
        for match in self.matches:
            serialized_matches.append(match.serialization())
        serialized_tour["matches"] = serialized_matches

        return serialized_tour
