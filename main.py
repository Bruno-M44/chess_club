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
        self.tours = []
        for tour in dict_init["tours"]:
            self.tours.append(Tour(tour))
        self.players = []
        for player in dict_init["players"]:
            self.players.append(Player(player))
        self.time_control = dict_init["time_control"]
        self.description = dict_init["description"]

    def players_ranking(self):
        ranked_players = sorted(self.players, key=lambda players: (-players.score, players.ranking))
        for player in ranked_players:
            print(player.__dict__)

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
        serialized_tours = []
        for tour in self.tours:
            serialized_tours.append(tour.serialization())
        serialized_tournament["tours"] = serialized_tours

        return serialized_tournament

    def player_score(self, player):
        score = 0
        for tour in self.tours:
            for match in tour.matches:
                if match.player_1.__dict__ == player.__dict__:
                    score += match.score_1
                elif match.player_2.__dict__ == player.__dict__:
                    score += match.score_2
        return score

    def players_met(self, player):
        players_met = []
        for tour in self.tours:
            for match in tour.matches:
                if match.player_1.__dict__ == player.__dict__:
                    players_met.append(match.player_2.__dict__)
                elif match.player_2.__dict__ == player.__dict__:
                    players_met.append(match.player_1.__dict__)
        return players_met

    def player_played_this_tour(self, player):
        player_played = False
        for match in self.tours[-1].matches:
            if match.player_1.__dict__ == player.__dict__:
                player_played = True
            elif match.player_2.__dict__ == player.__dict__:
                player_played = True
        return player_played

    def generate_a_tour(self):
        if not self.tours[0].matches:
            players_sorted = sorted(self.players, key=lambda players: int(players.ranking))
            print(self.tours[0].matches)
            for iPlayer in range(int(len(players_sorted) / 2)):
                self.tours[0].matches.append(Match({"player_1": players_sorted[iPlayer].__dict__,
                                                    "score_1": 0,
                                                    "player_2":
                                                        players_sorted[int(len(players_sorted) / 2 + iPlayer)].__dict__,
                                                    "score_2": 0}))
        else:
            players_sorted = sorted(self.players, key=lambda player: (-self.player_score(player), int(player.ranking)))
            # sorted by score (decreasing with the sign -) and ranking
            for iPlayer in range(len(players_sorted)):
                if not self.player_played_this_tour(players_sorted[iPlayer]):
                    j = 1
                    while True:
                        try:
                            player_met = players_sorted[iPlayer + j].__dict__ in self.players_met(players_sorted[iPlayer])
                            if player_met:
                                j += 1
                            else:
                                self.tours[-1].matches.append(Match({"player_1": players_sorted[iPlayer].__dict__,
                                                                     "score_1": 0,
                                                                     "player_2": players_sorted[iPlayer + j].__dict__,
                                                                     "score_2": 0
                                                                     }))
                                break
                        except:
                            break

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
        serialized_player = self.serialization()
        TinyDB("tables.json").table("players").upsert(serialized_player, (Query().last_name == self.last_name) &
                                                      (Query().first_name == self.first_name))


class Tour:
    def __init__(self, dict_init):
        self.name = dict_init["name"]
        self.start_date = dict_init["start_date"]
        self.end_date = dict_init["end_date"]
        self.matches = []
        for match in dict_init["matches"]:
            self.matches.append(Match(match))
        # self.tournament = tournament
        # self.tournament.tours.append(self)

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
                return view_consultation_tournament_menu()
            elif entry == 2:
                return view_creation_tournament()
            elif entry == 3:
                return view_main_menu()
            else:
                print("Saisie incorrecte, veuillez recommencer :")
        except:
            print("Saisie incorrecte, veuillez recommencer :")


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
        tournament_created["number_of_tours"] = input()
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
    if tournament == {}:
        return tournament

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
    except:
        if not tournament["number_of_tours"] == "":
            errors.append("Le nombre de tours du tournoi doit être un nombre.")

    if tournament["time_control"] not in ['bullet', 'blitz', 'coup rapide']:
        errors.append("Le contrôle du temps est mal renseigné.")

    if not errors:
        errors = "OK"

    return errors


def view_consultation_tournament_menu():
    for iTournament in range(len(TinyDB("tables.json").table("tournaments").all())):
        print(iTournament + 1, "- ", TinyDB("tables.json").table("tournaments").all()[iTournament]["name"])
    print("Sélectionner le tournoi sur le quel vous voulez agir :")
    while True:
        try:
            entry = int(input())
            for iTournament in range(len(TinyDB("tables.json").table("tournaments").all())):
                if entry == iTournament + 1:
                    return view_consultation_tournament(Tournament(TinyDB("tables.json").
                                                                   table("tournaments").all()[iTournament]))
            print("Saisie incorrecte, veuillez recommencer :")
        except:
            print("Saisie incorrecte, veuillez recommencer :")


def view_consultation_tournament(tournament):
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
    if not tournament.tours:
        print("3- Ajout joueurs")
        print("4- Générer un tour")
        print("5- Liste de tous les matchs d'un tournoi")
        print("6- Modification informations tournoi")
        print("7- Retour au menu précédent")
    elif tournament.tours[-1].matches[0].score_1 == 0 and tournament.tours[-1].matches[0].score_2 == 0:
        print("3- Rentrer les résultats du dernier tour généré")
        print("4- Liste de tous les matchs d'un tournoi")
        print("5- Modification informations tournoi")
        print("6- Retour au menu précédent")
    elif len(tournament.tours) < tournament.number_of_tours:
        print("3- Générer un tour")
        print("4- Liste de tous les matchs d'un tournoi")
        print("5- Modification informations tournoi")
        print("6- Retour au menu précédent")
    else:
        print("3- Liste de tous les matchs d'un tournoi")
        print("4- Modification informations tournoi")
        print("5- Retour au menu précédent")

    try:
        entry = int(input())
        if not tournament.tours:
            if entry == 1:
                return view_players_by_alphabetical_order(tournament)
            elif entry == 2:
                return view_players_by_ranking(tournament)
            elif entry == 3:
                return view_add_players(tournament)
            elif entry == 4:
                return view_generate_a_tour(tournament)
        elif tournament.tours[-1].matches[0].score_1 == 0 and tournament.tours[-1].matches[0].score_2 == 0:
            if entry == 1:
                return view_players_by_alphabetical_order(tournament)
            elif entry == 2:
                return view_players_by_ranking(tournament)
            elif entry == 3:
                return view_results_entry(tournament)
        elif len(tournament.tours) < tournament.number_of_tours:
            if entry == 1:
                return view_players_by_alphabetical_order(tournament)
            elif entry == 2:
                return view_players_by_ranking(tournament)
            elif entry == 3:
                return view_generate_a_tour(tournament)
        else:
            if entry == 1:
                return view_players_by_alphabetical_order(tournament)
            elif entry == 2:
                return view_players_by_ranking(tournament)
    except:
        print("Saisie incorrecte, veuillez recommencer :")


def view_players_by_alphabetical_order(tournament):
    print("Voici la liste des joueurs du tournoi classés par ordre alphabétique (Nom, Prénom, "
          "date de naissance, sexe, classement) :")
    print()
    alphabetical_order_players = sorted(tournament.players, key=lambda players: (players.last_name, players.first_name))
    for player in alphabetical_order_players:
        print(player.__dict__["last_name"], player.__dict__["first_name"], player.__dict__["birthday"],
              player.__dict__["gender"], player.__dict__["ranking"], sep=", ")
    print("Appuyer sur entrée pour revenir au menu précédent")
    input()
    return view_consultation_tournament(tournament)


def view_players_by_ranking(tournament):
    print("Voici la liste des joueurs du tournoi classés par classement (Nom, Prénom, "
          "date de naissance, sexe, classement) :")
    print()
    ranking_players = sorted(tournament.players, key=lambda players: int(players.ranking))
    for player in ranking_players:
        print(player.__dict__["last_name"], player.__dict__["first_name"], player.__dict__["birthday"],
              player.__dict__["gender"], player.__dict__["ranking"], sep=", ")
    print("Appuyer sur entrée pour revenir au menu précédent")
    input()
    return view_consultation_tournament(tournament)


def view_add_players(tournament):
    print("Voici la liste des joueurs disponibles :")
    print_number = 0
    players_available = []
    for player in TinyDB("tables.json").table("players").all():
        available = True
        for player_unavailable in tournament.players:
            if (player_unavailable.__dict__["last_name"] == player["last_name"] and
                    player_unavailable.__dict__["first_name"] == player["first_name"]):
                available = False
        if available:
            players_available.append(Player(player))
            print_number += 1
            print(print_number, "- ", player["last_name"], player["first_name"])
    if not players_available:
        print("Vous ne pouvez pas ajouter de joueur à ce tournoi. Veuillez créer un autre joueur.")
        return view_consultation_tournament_menu()

    print("Sélectionner le joueur que vous voulez ajouter :")
    try:
        entry = int(input())
        while True:
            for iPlayer in range(len(players_available)):
                if entry == iPlayer + 1:
                    tournament.players.append(players_available[iPlayer])
                    tournament.save_table()
                    print("Joueur ajouté au tournoi")
                    print("Voulez-vous ajouter un autre joueur ? (O ou N)")
                    entry = input()
                    if entry == "O":
                        return view_add_players(tournament)
                    elif entry == "N":
                        return view_consultation_tournament(tournament)
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
            print("Saisie incorrecte, veuillez recommencer :")
    except:
        print("Saisie incorrecte, veuillez recommencer :")


def view_generate_a_tour(tournament):
    tour_created = {}
    while controller_creation_tour(tour_created) != "OK":
        print("Saisir le nom du tour :")
        tour_created["name"] = input()
        print("Saisir la date de début du tour (format JJ/MM/SSAA) :")
        tour_created["start_date"] = input()
        print("Saisir la date de fin du tour (format JJ/MM/SSAA) - si non renseigné, le tour sera par "
              "défaut sur 1 journée :")
        tour_created["end_date"] = input()
        tour_created["matches"] = []
        if controller_creation_tour(tour_created) == "OK":
            tournament.tours.append(Tour(tour_created))
            tournament.generate_a_tour()
            tournament.save_table()
            print("Le tour a été généré")
            return view_consultation_tournament(tournament)
        else:
            for i in range(len(controller_creation_tour(tour_created))):
                print(controller_creation_tour(tour_created)[i])


def view_results_entry(tournament):
    for match in tournament.tours[-1].matches:
        print("Joueur 1 :", match.player_1.last_name, " ", match.player_1.first_name)
        print("rencontre")
        print("Joueur 2 :", match.player_2.last_name, " ", match.player_2.first_name)
        print("Vainqueur ? (1, 2 ou N pour nul)")
        result = str(input())
        while result != "1" and result != "2" and result != "N":
            print("Vous devez saisir 1, 2 ou N. Recommencer.")
            result = str(input())
        if result == "1":
            match.score_1 = 1
        elif result == "2":
            match.score_2 = 1
        else:
            match.score_1 = match.score_2 = 0.5
    tournament.save_table()
    print("Les résultats ont été sauvegardés")
    return view_consultation_tournament(tournament)


def controller_creation_tour(tour):
    if tour == {}:
        return tour

    errors = []

    if len(tour["name"]) < 3:
        errors.append("Le nom du tour doit être renseigné.")

    try:
        datetime.strptime(tour["start_date"], "%d/%m/%Y")
    except:
        errors.append("La date de début du tour doit être une date valide au format JJ/MM/SSAA.")

    try:
        datetime.strptime(tour["end_date"], "%d/%m/%Y")
    except:
        if tour["end_date"] == "":
            tour["end_date"] = tour["start_date"]
        else:
            errors.append("La date de fin du tour doit être une date valide au format JJ/MM/SSAA.")

    if not errors:
        errors = "OK"

    return errors


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
                view_consultation_player_menu()
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


def view_consultation_player_menu():
    for iPlayer in range(len(TinyDB("tables.json").table("players").all())):
        print(iPlayer + 1, "- ", TinyDB("tables.json").table("players").all()[iPlayer]["last_name"],
              TinyDB("tables.json").table("players").all()[iPlayer]["first_name"])
    print("Sélectionner le joueur sur lequel vous voulez agir :")
    while True:
        try:
            entry = int(input())
            for iPlayer in range(len(TinyDB("tables.json").table("players").all())):
                if entry == iPlayer + 1:
                    return view_consultation_player(Player(TinyDB("tables.json").table("players").all()[iPlayer]))
            print("Saisie incorrecte, veuillez recommencer :")
        except:
            print("Saisie incorrecte, veuillez recommencer :")


def view_consultation_player(player):
    print("Détails du joueur sélectionné :")
    print()
    print("Nom : ", player.last_name)
    print("Prénom : ", player.first_name)
    print("Date d'anniversaire : ", player.birthday)
    print("Sexe : ", player.gender)
    print("Classement : ", player.ranking)
    print()
    print("Sélectionner l'action désirée :")
    print("1- Modification informations joueur")
    print("2- Retour au menu précédent")
    while True:
        try:
            entry = int(input())
            if entry == 1:
                return "modifications, à compléter"
            elif entry == 2:
                return view_player_menu()
            else:
                print("Saisie incorrecte, veuillez recommencer :")
        except:
            print("Saisie incorrecte, veuillez recommencer :")


def view_creation_player():
    i_player_created = False
    player_created = {}
    while controller_creation_player(player_created) != "OK" and not i_player_created:
        print("Saisir le nom du joueur :")
        player_created["last_name"] = input()
        print("Saisir le prénom du joueur :")
        player_created["first_name"] = input()
        print("Saisir la date de naissance (format JJ/MM/SSAA) :")
        player_created["birthday"] = input()
        print("Saisir le sexe (M ou F) :")
        player_created["gender"] = input()
        print("Saisir le classement :")
        player_created["ranking"] = input()
        if controller_creation_player(player_created) == "OK":
            Player(player_created).save_table()
            print("Joueur créé")
            i_player_created = True
            view_player_menu()
        else:
            for i in controller_creation_player(player_created):
                print(i)


def controller_creation_player(player):
    if player == {}:
        return player
    errors = []

    if len(player["last_name"]) < 2:
        errors.append("Le nom du joueur doit être renseigné.")

    if len(player["first_name"]) < 2:
        errors.append("Le prénom du joueur doit être renseigné.")

    if TinyDB("tables.json").table("players").search((Query().last_name == player["last_name"]) &
                                                     (Query().first_name == player["first_name"])):
        errors.append("Le joueur a déjà été créé.")

    try:
        datetime.strptime(player["birthday"], "%d/%m/%Y")
    except:
        errors.append("La date d'anniversaire doit être une date valide au format JJ/MM/SSAA.")

    if player["gender"] not in ['M', 'F']:
        errors.append("Le sexe est mal renseigné")

    try:
        int(player["ranking"])
        if int(player["ranking"]) <= 0:
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
