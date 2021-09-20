from models.tournament import Tournament
from models.tour import Tour
from models.player import Player
from tinydb import TinyDB, Query
from datetime import datetime


class ControllerCreationTournament(Tournament):
    def controller_creation_tournament(self):
        if self == {}:
            return self

        errors = []

        if len(self["name"]) < 3:
            errors.append("Le nom du tournoi doit être renseigné.")

        if TinyDB("tables.json").table("tournament").\
                search(Query().name == self["name"]):
            errors.append("Le tournoi a déjà été créé.")

        if len(self["place"]) < 3:
            errors.append("Le lieu du tournoi doit être renseigné.")

        try:
            datetime.strptime(self["start_date"], "%d/%m/%Y")
        except ValueError:
            errors.append("La date de début du tournoi doit être une "
                          "date valide au format JJ/MM/SSAA.")

        try:
            datetime.strptime(self["end_date"], "%d/%m/%Y")
        except ValueError:
            if not self["end_date"] == "":
                errors.append("La date de fin du tournoi doit être une "
                              "date valide au format JJ/MM/SSAA.")

        try:
            int(self["number_of_tours"])
        except ValueError:
            if not self["number_of_tours"] == "":
                errors.append("Le nombre de tours du tournoi doit être "
                              "un nombre.")

        if self["time_control"] not in ['bullet', 'blitz', 'coup rapide']:
            errors.append("Le contrôle du temps est mal renseigné.")

        if not errors:
            errors = "OK"

        return errors


class ControllerCreationTour(Tour):
    def controller_creation_tour(self):
        if self == {}:
            return self

        errors = []

        if len(self["name"]) < 3:
            errors.append("Le nom du tour doit être renseigné.")

        try:
            datetime.strptime(self["start_date"], "%d/%m/%Y")
        except ValueError:
            errors.append("La date de début du tour doit être une date "
                          "valide au format JJ/MM/SSAA.")

        try:
            datetime.strptime(self["end_date"], "%d/%m/%Y")
        except ValueError:
            if self["end_date"] == "":
                self["end_date"] = self["start_date"]
            else:
                errors.append("La date de fin du tour doit être une date "
                              "valide au format JJ/MM/SSAA.")

        if not errors:
            errors = "OK"

        return errors


class ControllerCreationPlayer(Player):
    def controller_creation_player(self):
        if self == {}:
            return self
        errors = []

        if len(self["last_name"]) < 2:
            errors.append("Le nom du joueur doit être renseigné.")

        if len(self["first_name"]) < 2:
            errors.append("Le prénom du joueur doit être renseigné.")

        if TinyDB("tables.json").table("players").\
                search((Query().last_name == self["last_name"]) &
                       (Query().first_name == self["first_name"])):
            errors.append("Le joueur a déjà été créé.")

        try:
            datetime.strptime(self["birthday"], "%d/%m/%Y")
        except ValueError:
            errors.append("La date d'anniversaire doit être une date "
                          "valide au format JJ/MM/SSAA.")

        if self["gender"] not in ['M', 'F']:
            errors.append("Le sexe est mal renseigné")

        try:
            int(self["ranking"])
            if int(self["ranking"]) <= 0:
                errors.append("Le classement doit être un entier positif.")
        except ValueError:
            errors.append("Le classement doit être un entier positif.")

        if not errors:
            errors = "OK"

        return errors
