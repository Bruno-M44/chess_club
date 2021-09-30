from tinydb import TinyDB, Query
from datetime import datetime


class ControllerCreationTournament:
    def controller_name(self):
        if len(self) < 3:
            print("Le nom du tournoi doit être renseigné.")
            return False
        elif TinyDB("tables.json").table("tournaments").\
                search(Query().name == self):
            print("Le tournoi a déjà été créé.")
            return False
        else:
            return True

    def controller_place(self):
        if len(self) < 3:
            print("Le lieu du tournoi doit être renseigné.")
            return False
        else:
            return True

    def controller_start_date(self):
        try:
            datetime.strptime(self, "%d/%m/%Y")
            return True
        except ValueError:
            print("La date de début du tournoi doit être une date valide au "
                  "format JJ/MM/SSAA.")
            return False

    def controller_end_date(self):
        try:
            datetime.strptime(self, "%d/%m/%Y")
            return True
        except ValueError:
            if not self == "":
                print("La date de fin du tournoi doit être une date valide "
                      "au format JJ/MM/SSAA.")
                return False
            else:
                return True

    def controller_number_of_tours(self):
        try:
            int(self)
            if self <= 0:
                print("Le nombre de tours du tournoi ne peut pas être nul "
                      "ou négatif.")
                return False
            else:
                return True
        except ValueError:
            if not self == "":
                print("Le nombre de tours du tournoi doit être un nombre.")
                return False
            else:
                return True

    def controller_time_control(self):
        if self not in ['bullet', 'blitz', 'coup rapide']:
            print("Le contrôle du temps est mal renseigné.")
            return False
        else:
            return True


class ControllerCreationPlayer:
    def controller_name(self):
        if len(self["last_name"]) < 2:
            print("Le nom du joueur doit être renseigné.")
            return False
        elif len(self["first_name"]) < 2:
            print("Le prénom du joueur doit être renseigné.")
            return False
        elif TinyDB("tables.json").table("players").\
                search((Query().last_name == self["last_name"]) &
                       (Query().first_name == self["first_name"])):
            print("Le joueur a déjà été créé.")
            return False
        else:
            return True

    def controller_birthday(self):
        try:
            datetime.strptime(self, "%d/%m/%Y")
            return True
        except ValueError:
            print("La date d'anniversaire doit être une date valide au "
                  "format JJ/MM/SSAA.")
            return False

    def controller_gender(self):
        if self not in ['M', 'F']:
            print("Le sexe est mal renseigné.")
            return False
        else:
            return True

    def controller_ranking(self):
        try:
            int(self)
            if int(self) <= 0:
                print("Le classement doit être un entier positif.")
                return False
            else:
                return True
        except ValueError:
            print("Le classement doit être un entier positif.")
            return False
