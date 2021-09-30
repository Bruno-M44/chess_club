from models.player import Player
from controller.controller_creation import ControllerCreationPlayer
from view.clear_terminal import ClearTerminal
from tinydb import TinyDB


class ViewPlayerByTournament:
    def __init__(self, tournament):
        self.tournament = tournament

    def view_players_by_alphabetical_order(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici la liste des joueurs du tournoi " + self.name +
              " classés par ordre "
              "alphabétique (Nom, Prénom, date de naissance, sexe, "
              "classement) :")
        print()
        alphabetical_order_players = sorted(self.players,
                                            key=lambda players:
                                            (players.last_name,
                                             players.first_name))
        for player in alphabetical_order_players:
            print(player.__dict__["last_name"], player.__dict__["first_name"],
                  player.__dict__["birthday"],
                  player.__dict__["gender"], player.__dict__["ranking"],
                  sep=", ")
        input()
        return ViewReport.view_report_menu()

    def view_players_by_ranking(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici la liste des joueurs du tournoi " + self.name +
              " classés par classement "
              "(Nom, Prénom, date de naissance, sexe, classement) :")
        print()
        ranking_players = sorted(self.players,
                                 key=lambda players: int(players.ranking))
        for player in ranking_players:
            print(player.__dict__["last_name"], player.__dict__["first_name"],
                  player.__dict__["birthday"],
                  player.__dict__["gender"], player.__dict__["ranking"],
                  sep=", ")
        input()
        return ViewReport.view_report_menu()

    def view_players_by_score(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici la liste des joueurs du tournoi " + self.name +
              " classés par score "
              "(Nom, Prénom, date de naissance, sexe, classement, score) :")
        print(ViewPlayerByTournament.score_player(self, self.players[0]))
        scores_players = sorted(self.players,
                                key=lambda players: -ViewPlayerByTournament.
                                score_player(self, players))
        for player in scores_players:
            print(player.__dict__["last_name"], player.__dict__["first_name"],
                  player.__dict__["birthday"],
                  player.__dict__["gender"], player.__dict__["ranking"],
                  ViewPlayerByTournament.score_player(self, player),
                  sep=", ")
        input()
        return ViewReport.view_report_menu()

    def score_player(self, player):
        score = 0
        for tour in self.tours:
            for match in tour.matches:
                if match.player_1.__dict__ == player.__dict__:
                    score += match.score_1
                elif match.player_2.__dict__ == player.__dict__:
                    score += match.score_2
        return score

    def view_add_players(self):
        from view.view_tournament import ViewTournament
        ClearTerminal.clear_terminal()
        print("Voici la liste des joueurs disponibles :")
        list_players_available = ViewPlayerByTournament.players_available(self)
        for iPlayer in range(len(list_players_available)):
            print(iPlayer + 1, "- ",
                  list_players_available[iPlayer]["last_name"],
                  list_players_available[iPlayer]["first_name"])

        print("Sélectionner le joueur que vous voulez ajouter :")
        while True:
            try:
                entry = int(input())
                if 0 < entry <= len(list_players_available):
                    for iPlayer in range(len(list_players_available)):
                        if entry == iPlayer + 1:
                            if not ViewPlayerByTournament.players_available(
                                    self):
                                ClearTerminal.clear_terminal()
                                print("Il n'y a plus de joueur disponible. "
                                      "Veuillez en créer un autre via le "
                                      "menu joueur")
                                return ViewTournament.view_tournament_menu()
                            else:
                                self.players.\
                                    append(Player(list_players_available[
                                                                    iPlayer]))
                                self.save_table()
                                ClearTerminal.clear_terminal()
                                print("Joueur ajouté au tournoi")
                                input()
                                ClearTerminal.clear_terminal()
                                if ViewPlayerByTournament.players_available(
                                        self):
                                    print(len(self.players),
                                          " joueurs ajoutés")

                                    if len(self.players) == 8 and \
                                            self.number_of_tours == 4:
                                        "Tous les joueurs ont été ajoutés."
                                        input()
                                        return ViewTournament.\
                                            view_tournament_menu()

                                    print("pour un tournoi par défaut, "
                                          "veuillez renseigner 8 joueurs.")
                                    print("Ajouter un autre joueur : "
                                          "'r' pour retourner en arrière")
                                    entry = input()
                                    if entry == "r":
                                        return ViewTournament.\
                                            view_tournament_menu()
                                    else:
                                        return ViewPlayerByTournament. \
                                            view_add_players(self)
                                else:
                                    return ViewTournament.\
                                        view_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer")

    def players_available(self):
        players_available = []
        for player in TinyDB("tables.json").table("players").all():
            available = True
            for player_unavailable in self.players:
                if (player_unavailable.__dict__["last_name"]
                        == player["last_name"] and
                        player_unavailable.__dict__["first_name"]
                        == player["first_name"]):
                    available = False
            if available:
                players_available.append(player)
        return players_available


class ViewPlayer:
    @classmethod
    def view_player_menu(cls):
        ClearTerminal.clear_terminal()
        i_correct_input = False
        while not i_correct_input:
            print("1- Consultation joueurs et modification classement")
            print("2- Création nouveau joueur")
            print("3- Retour au menu précédent")
            print("Saisir 1, 2 ou 3 puis entrée pour faire votre choix :")
            try:
                entry = int(input())
                if entry == 1:
                    ViewPlayer.view_consultation_player_menu()
                    i_correct_input = True
                elif entry == 2:
                    ViewPlayer.view_creation_player()
                    i_correct_input = True
                elif entry == 3:
                    i_correct_input = True
                    from view.view_main_menu import ViewMain
                    ViewMain.view_main_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")

    @classmethod
    def view_consultation_player_menu(cls):
        ClearTerminal.clear_terminal()
        if TinyDB("tables.json").table("players").all():
            for iPlayer in range(len(
                    TinyDB("tables.json").table("players").all())):
                print(iPlayer + 1, "- ",
                      TinyDB("tables.json").table("players").all()[iPlayer][
                          "last_name"],
                      TinyDB("tables.json").table("players").all()[iPlayer][
                          "first_name"])
            print("Sélectionner le joueur sur lequel vous voulez agir :")
            while True:
                try:
                    entry = int(input())
                    for iPlayer in range(
                            len(TinyDB("tables.json").table("players").all())):
                        if entry == iPlayer + 1:
                            return ViewPlayerByPlayer.view_consultation_player(
                                Player(TinyDB("tables.json").
                                       table("players").all()[iPlayer]))
                    print("Saisie incorrecte, veuillez recommencer :")
                except ValueError:
                    print("Saisie incorrecte, veuillez recommencer :")
        else:
            print("Créer d'abord un joueur.")
            return ViewPlayer.view_player_menu()

    @classmethod
    def view_creation_player(cls):
        ClearTerminal.clear_terminal()
        player_created = {}
        print("Saisir le nom du joueur :")
        save_input = {"last_name": input()}
        print("Saisir le prénom du joueur :")
        save_input["first_name"] = input()
        while not ControllerCreationPlayer.controller_name(save_input):
            print("Saisir le nom du joueur :")
            save_input = {"last_name": input()}
            print("Saisir le prénom du joueur :")
            save_input["first_name"] = input()
        player_created["last_name"] = save_input["last_name"]
        player_created["first_name"] = save_input["first_name"]

        ClearTerminal.clear_terminal()
        print("Saisir la date de naissance (format JJ/MM/SSAA) :")
        save_input = input()
        while not ControllerCreationPlayer.controller_birthday(save_input):
            save_input = input()
        player_created["birthday"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir le sexe (M ou F) :")
        save_input = input()
        while not ControllerCreationPlayer.controller_gender(save_input):
            save_input = input()
        player_created["gender"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir le classement :")
        save_input = input()
        while not ControllerCreationPlayer.controller_ranking(save_input):
            save_input = input()
        player_created["ranking"] = save_input

        ClearTerminal.clear_terminal()
        Player(player_created).save_table()
        print("Joueur créé")
        input()
        return ViewPlayer.view_player_menu()

    @classmethod
    def view_players_by_alphabetical_order(cls):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici la liste des joueurs par ordre alphabétique (Nom, "
              "Prénom, date de naissance, sexe et classement) :")
        print()
        alphabetical_order_players = sorted(TinyDB("tables.json").
                                            table("players").all(),
                                            key=lambda x: (
                                                x["last_name"],
                                                x["first_name"]))
        for player in alphabetical_order_players:
            print(player["last_name"], player["first_name"],
                  player["birthday"], player["gender"],
                  player["ranking"], sep=", ")
        input()
        return ViewReport.view_report_menu()

    @classmethod
    def view_players_by_ranking(cls):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici la liste des joueurs par classement (Nom, "
              "Prénom, date de naissance, sexe et classement) :")
        print()
        ranking_players = sorted(TinyDB("tables.json").
                                 table("players").all(),
                                 key=lambda x: (int(x["ranking"])))
        for player in ranking_players:
            print(player["last_name"], player["first_name"],
                  player["birthday"], player["gender"],
                  player["ranking"], sep=", ")
        input()
        return ViewReport.view_report_menu()


class ViewPlayerByPlayer:
    def __init__(self, player):
        self.player = player

    def view_consultation_player(self):
        ClearTerminal.clear_terminal()
        print("Détails du joueur sélectionné :")
        print()
        print("Nom : ", self.last_name)
        print("Prénom : ", self.first_name)
        print("Date d'anniversaire : ", self.birthday)
        print("Sexe : ", self.gender)
        print("Classement : ", self.ranking)
        print()
        print("Sélectionner l'action désirée :")
        print("1- Modification classement joueur")
        print("2- Retour au menu précédent")
        while True:
            try:
                entry = int(input())
                if entry == 1:
                    return ViewPlayerByPlayer.view_modification_ranking(self)
                elif entry == 2:
                    return ViewPlayer.view_player_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")

    def view_modification_ranking(self):
        ClearTerminal.clear_terminal()
        print("Entrer le nouveau classement du joueur :")
        while True:
            try:
                entry = int(input())
                if entry > 0:
                    self.modification_ranking(entry)
                    self.save_table()
                    return ViewPlayerByPlayer.view_consultation_player(self)
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")
