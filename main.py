from tinydb import TinyDB, Query
import copy
import sys
import os
from datetime import datetime


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
        self.tours = dict_init["tours"]
        self.tours = []
        for tour in dict_init["tours"]:
            self.tours.append(Tour(tour))
        self.players = []
        for player in dict_init["players"]:
            self.players.append(Player(player))
        self.time_control = dict_init["time_control"]
        self.description = dict_init["description"]

    def add_player(self, *players):
        for i in players:
            self.players.append(i)
        self.save_table()

    def players_ranking(self):
        ranked_players = sorted(self.players, key=lambda players: (-players.score, players.ranking))
        for i in ranked_players:
            print(i.__dict__)

    def save_table(self):
        serialized_tournament = self.serialization()
        TinyDB("tables.json").table("tournaments").upsert(serialized_tournament, Query().name == self.name)

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

        return serialized_tournament
        '''
        serialized_tournament = copy.deepcopy(self.__dict__)  # to change made to a copy of object do not
        # reflect in the original object.

        for iPlayer in range(len(serialized_tournament['players'])):
            serialized_tournament['players'][iPlayer] = serialized_tournament['players'][iPlayer].__dict__

        for iTour in range(len(serialized_tournament['tours'])):
            serialized_tournament['tours'][iTour] = serialized_tournament['tours'][iTour].__dict__
            serialized_tournament['tours'][iTour]['tournament'] = serialized_tournament['name']
            for iMatch in range(len(serialized_tournament['tours'][iTour]['matches'])):
                serialized_tournament['tours'][iTour]['matches'][iMatch] = \
                    serialized_tournament['tours'][iTour]['matches'][iMatch].__dict__
                serialized_tournament['tours'][iTour]['matches'][iMatch]['player_1'] = \
                    serialized_tournament['tours'][iTour]['matches'][iMatch]['player_1'].__dict__
                serialized_tournament['tours'][iTour]['matches'][iMatch]['player_2'] = \
                    serialized_tournament['tours'][iTour]['matches'][iMatch]['player_2'].__dict__
                serialized_tournament['tours'][iTour]['matches'][iMatch]['tour'] = \
                    serialized_tournament['tours'][iTour]['name']
        return serialized_tournament
        '''

    @classmethod
    def load_table(cls):
        tournaments = []
        for tournament in TinyDB("tables.json").all():
            tournaments.append(Tournament(name=tournament['name'], place=tournament['place'],
                                          start_date=tournament['start_date'], end_date=tournament['end_date'],
                                          number_of_tours=tournament['number_of_tours'],
                                          time_control=tournament['time_control'],
                                          description=tournament['description']))
        return tournaments


class Player:
    def __init__(self, dict_init):
        self.last_name = dict_init["last_name"]
        self.first_name = dict_init["first_name"]
        self.birthday = dict_init["birthday"]
        self.gender = dict_init["gender"]
        self.ranking = dict_init["ranking"]

    #        self.score = 0
    #        self.players_met = []

    def serialization(self):
        serialized_player = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "ranking": self.ranking,
        }
        return serialized_player

    def save_table(self):
        TinyDB("players.json").upsert(self.__dict__, (Query().last_name == self.last_name) &
                                      (Query().first_name == self.first_name))


class Tour:
    def __init__(self, name, start_date, end_date, tournament):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = []
        self.tournament = tournament
        self.tournament.tours.append(self)
        self.tournament.save_table()

    def generate_a_tour(self):
        if not self.tournament.tours[0].matches:
            players_sorted = sorted(self.tournament.players, key=lambda players: players.ranking)
            for i in range(int(len(players_sorted) / 2)):
                self.matches.append(Match(players_sorted[i], 0,
                                          players_sorted[int(len(players_sorted) / 2 + i)], 0, self))
            self.tournament.save_table()
        else:
            players_sorted = sorted(self.tournament.players, key=lambda players: (-players.score, players.ranking))
            # sorted by score (decreasing with the sign -) and ranking
            players_assigned = []
            for i in range(len(players_sorted)):
                iAttribution = 0
                if not str(i) in players_assigned:
                    for j in range(i + 1, len(players_sorted)):
                        if not str(j) in players_assigned:
                            if not str(players_sorted[i].first_name + ' ' + players_sorted[i].last_name) in \
                                   players_sorted[j].players_met:
                                if iAttribution == 0:
                                    self.matches.append(Match(players_sorted[i], 0, players_sorted[j], 0, self))
                                    iAttribution = 1
                                    players_assigned.append(str(i))
                                    players_assigned.append(str(j))
                    if iAttribution == 0:
                        for j in range(i):
                            if not str(j) in players_assigned:
                                if not str(players_sorted[i].first_name + ' ' + players_sorted[i].last_name) in \
                                       players_sorted[j].players_met:
                                    if iAttribution == 0:
                                        self.matches.append(Match(players_sorted[i], 0, players_sorted[j], 0, self))
                                        iAttribution = 1
                                        players_assigned.append(str(i))
                                        players_assigned.append(str(j))
            self.tournament.save_table()

    def results(self):
        for match in self.matches:
            print("Player 1 :", match.__dict__['player_1'].__dict__)
            print("Player 2 :", match.__dict__['player_2'].__dict__)
            print("Vainqueur ? (1, 2 ou N pour nul)")
            result = str(input())
            while result != "1" and result != "2" and result != "N":
                print("Vous devez saisir 1, 2 ou N. Recommencer.")
                result = str(input())
            if result == "1":
                match.score_1 = 1
                match.player_1.score += 1
            elif result == "2":
                match.score_2 = 1
                match.player_2.score += 1
            else:
                match.score_1 = match.score_2 = 0.5
                match.player_1.score += 0.5
                match.player_2.score += 0.5
            match.player_1.players_met.append(match.player_2.first_name + ' ' + match.player_2.last_name)
            match.player_2.players_met.append(match.player_1.first_name + ' ' + match.player_1.last_name)
        self.tournament.save_table()


class Match:
    def __init__(self, player_1, score_1, player_2, score_2, tour):
        self.player_1 = player_1
        self.score_1 = score_1
        self.player_2 = player_2
        self.score_2 = score_2
        self.tour = tour


def main():
    view_main_menu()


def view_main_menu():
    while True:
        print("1- Tournois (consultation, modification, création)")
        print("2- Joueurs (consultation, modification, création)")
        print("3- Quitter le programme")
        print("Saisir 1, 2 ou 3 puis entrée pour faire votre choix :")
        try:
            entry = int(input())
            if entry == 1:
                return view_tournament_menu()
            elif entry == 2:
                return view_player_menu()
            elif entry == 3:
                return "fin programme"
            else:
                print("Saisie incorrecte, veuillez recommencer :")
        except:
            print("Saisie incorrecte, veuillez recommencer :")


def view_tournament_menu():
    while True:
        print("1- Consultation tournois")
        print("2- Création nouveau tournoi")
        print("3- Retour au menu précédent")
        print("Saisir 1, 2 ou 3 puis entrée pour faire votre choix :")
        try:
            entry = int(input())
            if entry == 1:
               return view_consultation_tournament()
            elif entry == 2:
                return view_creation_tournament()
            elif entry == 3:
                return view_main_menu()
            else:
                print("Saisie incorrecte, veuillez recommencer :")
                print("toto 1")
        except:
            print("Saisie incorrecte, veuillez recommencer :")
            print("toto 2")


def view_creation_tournament():
    i_tournament_created = False
    tournament_created = {}
    while controller_creation_tournament(tournament_created) != "OK" and not i_tournament_created:
        print("Saisir le nom du tournoi :")
        tournament_created["name"] = input()
        print("Saisir le lieu du tournoi :")
        tournament_created["place"] = input()
        print("Saisir la date de début du tournoi (format JJ/MM/SSAA) :")
        tournament_created["start_date"] = input()
        print("Saisir la date de fin du tournoi (format JJ/MM/SSAA) - facultatif :")
        tournament_created["end_date"] = input()
        print("Saisir le nombre de tour du tournoi - facultatif (4 par défaut) :")
        tournament_created["number_of_tours"] = int(input())
        print("Saisir le contrôle du temps du tournoi. Saisir 'bullet', 'blitz' ou 'coup rapide'")
        tournament_created["time_control"] = input()
        print("Saisir la description du tournoi - facultatif :")
        tournament_created["description"] = input()
        tournament_created["players"] = []
        tournament_created["tours"] = []
        if controller_creation_tournament(tournament_created) == "OK":
            Tournament(tournament_created).save_table()
            print("Tournoi créé")
            i_tournament_created = True
            view_tournament_menu()
        else:
            for i in range(len(controller_creation_tournament(tournament_created))):
                print(controller_creation_tournament(tournament_created)[i])


def controller_creation_tournament(tournament):
    if len(tournament) <= 9:
        return "KO"

    errors = []

    if len(tournament["name"]) < 3:
        errors.append("Le nom du tournoi doit être renseigné.")

    if TinyDB("tables.json").table("tournaments").search(Query().name == tournament["name"]):
        errors.append("Le tournoi a déjà été créé.")

    if len(tournament["place"]) < 3:
        errors.append("Le lieu du tournoi doit être renseigné.")

    try:
        datetime.strptime(tournament["start_date"], "%d/%m/%Y")
    except:
        errors.append("La date de début du tournoi doit être une date valide au format JJ/MM/SSAA.")

    try:
        datetime.strptime(tournament["end_date"], "%d/%m/%Y")
    except:
        if not tournament["end_date"] == "":
            errors.append("La date de fin du tournoi doit être une date valide au format JJ/MM/SSAA.")

    try:
        int(tournament["number_of_tours"])
        print("toto 3")
    except:
        if not tournament["number_of_tours"] == "":
            errors.append("Le nombre de tours du tournoi doit être un nombre.")

    if tournament["time_control"] not in ['bullet', 'blitz', 'coup rapide']:
        errors.append("Le contrôle du temps est mal renseigné.")

    if not errors:
        errors = "OK"

    return errors


def view_consultation_tournament():
    for iTournament in range(len(TinyDB("tables.json").table("tournaments").all())):
        print(iTournament + 1, "- ", TinyDB("tables.json").table("tournaments").all()[iTournament]["name"])
    print("Sélectionner le tournoi sur le quel vous voulez agir :")
    try:
        entry = int(input())
        i_menu_displayed = False
        while not i_menu_displayed:
            for iTournament in range(len(TinyDB("tables.json").table("tournaments").all())):
                if entry == iTournament + 1:
                    print(TinyDB("tables.json").table("tournaments").all()[iTournament])
                    tournament = Tournament(TinyDB("tables.json").table("tournaments").all()[iTournament])
                    print("Détails du tournoi sélectionné :")
                    print()
                    print("Nom : ", tournament.name)
                    print("Lieu : ", tournament.place)
                    print("Date de début : ", tournament.start_date)
                    print("Date de fin : ", tournament.end_date)
                    print("Nombre de tours : ", tournament.number_of_tours)
                    print("Contrôle du temps : ", tournament.time_control)
                    print("Description : ", tournament.description)
                    print()
                    print("Sélectionner l'action désirée :")
                    print("1- Liste de tous les joueurs par ordre alphabétique")
                    print("2- Liste de tous les joueurs par classement")
                    print("3- Ajout joueurs")
                    print("4- Liste de tous les tours d'un tournoi")
                    print("5- Liste de tous les matchs d'un tournoi")
                    print("6- Modification informations tournoi")
                    print("7- Retour au menu précédent")
                    # ajout génération tour et saisie résultats
                    i_menu_displayed = True
                    try:
                        entry = int(input())
                        if entry == 1:
                            print("1")
                        elif entry == 2:
                            print("2")
                        elif entry == 3:
                            view_add_players(tournament)
                    except:
                        print("Saisie incorrecte, veuillez recommencer :")

            if not i_menu_displayed:
                print("Saisie incorrecte, veuillez recommencer :")
    except:
        print("Saisie incorrecte, veuillez recommencer :")


def view_add_players(tournament):
    print("Voici la liste des joueurs disponibles :")
    print_number = 0
    players_available = []
    for player in TinyDB("tables.json").table("players").all():
        print(TinyDB("tables.json").table("players").search((Query().last_name == player["last_name"]) &
                                                            (Query().first_name == player["first_name"])))
        if TinyDB("tables.json").table("players").search((Query().last_name == player["last_name"]) &
                                                         (Query().first_name == player["first_name"])):
            print_number += 1
            players_available.append(player)
            print(print_number, "- ", player["last_name"], player["first_name"])
    print("Sélectionner le joueur que vous voulez ajouter :")
    try:
        entry = int(input())
        i_menu_displayed = False
        while not i_menu_displayed:
            for iPlayer in range(len(players_available)):
                if entry == iPlayer + 1:
                    player = Player(TinyDB("tables.json").table("players").all()[iPlayer])
                    print(tournament.players)
                    print(player)
                    tournament.players.append(player)
                    print(tournament.players)
                    tournament.save_table()
                    print("Joueur ajouté au tournoi")
                    print("Voulez-vous ajouter un autre joueur ? (O ou N)")
                    entry = input()
                    if entry == "O":
                        view_add_players(tournament)
                        i_menu_displayed = True
                    elif entry == "N":
                        view_consultation_tournament()
                        i_menu_displayed = True
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
            if not i_menu_displayed:
                print("Saisie incorrecte, veuillez recommencer :")
    except:
        print("Saisie incorrecte, veuillez recommencer :")


def view_player_menu():
    i_correct_input = False
    while not i_correct_input:
        print("1- Consultation joueurs")
        print("2- Création nouveau joueur")
        print("3- Retour au menu précédent")
        print("Saisir 1 ou 2 puis entrée pour faire votre choix :")
        try:
            entry = int(input())
            if entry == 1:
                view_consultation_player()
                i_correct_input = True
            elif entry == 2:
                view_creation_player()
                i_correct_input = True
            elif entry == 3:
                i_correct_input = True
                view_main_menu()
            else:
                print("Saisie incorrecte, veuillez recommencer :")
        except:
            print("Saisie incorrecte, veuillez recommencer :")


def view_consultation_player():
    for iPlayer in range(len(TinyDB("tables.json").table("players").all())):
        print(iPlayer + 1, "- ", TinyDB("tables.json").table("players").all()[iPlayer]["last_name"],
              TinyDB("tables.json").table("players").all()[iPlayer]["first_name"])
    print("Sélectionner le joueur sur le quel vous voulez agir :")
    try:
        entry = int(input())
        i_menu_displayed = False
        while not i_menu_displayed:
            for iPlayer in range(len(TinyDB("tables.json").table("players").all())):
                if entry == iPlayer + 1:
                    print("Détails du joueur sélectionné :")
                    print()
                    print("Nom : ", TinyDB("tables.json").table("players").all()[iPlayer]["last_name"])
                    print("Prénom : ", TinyDB("tables.json").table("players").all()[iPlayer]["first_name"])
                    print("Date d'anniversaire : ",
                          TinyDB("tables.json").table("players").all()[iPlayer]["birthday"])
                    print("Sexe : ", TinyDB("tables.json").table("players").all()[iPlayer]["gender"])
                    print("Classement : ", TinyDB("tables.json").table("players").all()[iPlayer]["ranking"])
                    print()
                    print("Sélectionner l'action désirée :")
                    print("1- Modification informations joueur")
                    print("2- Retour au menu précédent")
                    try:
                        entry = int(input())
                        if entry == 1:
                            print("modifications, à compléter")
                            i_menu_displayed = True
                        elif entry == 2:
                            view_player_menu()
                            i_menu_displayed = True
                        else:
                            print("Saisie incorrecte, veuillez recommencer :")
                    except:
                        print("Saisie incorrecte, veuillez recommencer :")
            if not i_menu_displayed:
                print("Saisie incorrecte, veuillez recommencer :")
    except:
        print("Saisie incorrecte, veuillez recommencer :")


def view_creation_player():
    input_list = []
    i_player_created = False
    while controller_creation_player(input_list) != "OK" and not i_player_created:
        input_list = []
        print("Saisir le nom du joueur :")
        input_list.append(input())
        print("Saisir le prénom du joueur :")
        input_list.append(input())
        print("Saisir la date de naissance (format JJ/MM/SSAA) :")
        input_list.append(input())
        print("Saisir le sexe (M ou F) :")
        input_list.append(input())
        print("Saisir le classement :")
        input_list.append(input())
        if controller_creation_player(input_list) == "OK":
            Player_instance = Player(input_list[0], input_list[1], input_list[2], input_list[3], input_list[4])
            TinyDB("tables.json").table("players").insert(Player_instance.serialization())
            print("Joueur créé")
            i_player_created = True
            view_player_menu()
        else:
            for i in controller_creation_player(input_list):
                print(i)


def controller_creation_player(input_list_args):
    if len(input_list_args) != 5:
        return "KO"
    errors = []

    if len(input_list_args[0]) < 3:
        errors.append("Le nom du joueur doit être renseigné.")

    if len(input_list_args[1]) < 3:
        errors.append("Le prénom du joueur doit être renseigné.")

    if TinyDB("tables.json").table("players").search((Query().last_name == input_list_args[0]) &
                                                     (Query().first_name == input_list_args[1])):
        errors.append("Le joueur a déjà été créé.")

    try:
        datetime.strptime(input_list_args[2], "%d/%m/%Y")
    except:
        errors.append("La date d'anniversaire doit être une date valide au format JJ/MM/SSAA.")

    if input_list_args[3] not in ['M', 'F']:
        errors.append("Le sexe est mal renseigné")

    try:
        int(input_list_args[4])
        if int(input_list_args[4]) <= 0:
            errors.append("Le classement doit être un entier positif.")
    except:
        errors.append("Le classement doit être un entier positif.")

    if not errors:
        errors = "OK"

    return errors


main()

'''
Tournament_1 = Tournament("Tournoi Bretagne", "Rennes", "01/05/2021", "", "", "bullet", "1er tournoi de la saison")
Tournament_2 = Tournament("Tournoi Lorraine", "Nancy", "10/06/2021", "20/06/2021", "", "bullet", "ras")

Player_1 = Player("Smith", "John", "02/05/1990", "M", 63)
Player_2 = Player("Durand", "Michel", "14/11/1948", "M", 567)
Player_3 = Player("Kasparov", "Garry", "13/04/1963", "M", 1)
Player_4 = Player("Carlsen", "Magnus", "02/02/1989", "M", 7)
Player_5 = Player("Menchik", "Vera", "01/03/1934", "F", 5)
Player_6 = Player("Yi", "Wei", "04/07/1981", "F", 22)
Player_7 = Player("Gaprindashvili", "Nona", "02/10/1942", "F", 8)
Player_8 = Player("Yifan", "Hou", "30/04/1994", "F", 78)

Tournament_1.add_player(Player_1, Player_2, Player_3, Player_4, Player_5, Player_6, Player_7, Player_8)

Tour_1 = Tour("Tour 1", "01/05/2021", "01/05/2021", Tournament_1)

Tournament_1.players_ranking()

Tour_1.generate_a_tour()

Tour_1.results()


Tour_2 = Tour("Tour 2", "02/05/2021", "02/05/2021", Tournament_1)

Tour_2.generate_a_tour()

Tour_2.results()

Tour_3 = Tour("Tour 3", "03/05/2021", "03/05/2021", Tournament_1)

Tour_3.generate_a_tour()

Tour_3.results()


Tour_4 = Tour("Tour 4", "04/05/2021", "04/05/2021", Tournament_1)

Tour_4.generate_a_tour()

Tour_4.results()



Tournament_1.players_ranking()

'''
'''
tournaments = []
for tournament in Tournament.load_table():
    tournaments.append(Tournament(name=tournament['name'], place=tournament['place'],
                                  start_date=tournament['start_date'], end_date=tournament['end_date'],
                                  number_of_tours=tournament['number_of_tours'],
                                  time_control=tournament['time_control'], description=tournament['description']))

print(tournaments[0].__dict__)

'''
