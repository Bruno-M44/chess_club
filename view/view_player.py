from models.tournament import Tournament
from models.player import Player
from controller.controller_creation import ControllerCreationPlayer
from tinydb import TinyDB


class ViewPlayerByTournament(Tournament):
    def view_players_by_alphabetical_order(self):
        from view.view_tournament import ViewTournamentByTournament
        print("Voici la liste des joueurs du tournoi classés par ordre "
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
        print("Appuyer sur entrée pour revenir au menu précédent")
        input()
        return ViewTournamentByTournament.view_consultation_tournament(self)

    def view_players_by_ranking(self):
        from view.view_tournament import ViewTournamentByTournament
        print("Voici la liste des joueurs du tournoi classés par classement "
              "(Nom, Prénom, date de naissance, sexe, classement) :")
        print()
        ranking_players = sorted(self.players,
                                 key=lambda players: int(players.ranking))
        for player in ranking_players:
            print(player.__dict__["last_name"], player.__dict__["first_name"],
                  player.__dict__["birthday"],
                  player.__dict__["gender"], player.__dict__["ranking"],
                  sep=", ")
        print("Appuyer sur entrée pour revenir au menu précédent")
        input()
        return ViewTournamentByTournament.view_consultation_tournament(self)

    def view_add_players(self):
        from view.view_tournament import ViewTournamentByTournament, \
            ViewTournament
        print("Voici la liste des joueurs disponibles :")
        print_number = 0
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
                players_available.append(Player(player))
                print_number += 1
                print(print_number, "- ", player["last_name"],
                      player["first_name"])
        if not players_available:
            print("Vous ne pouvez pas ajouter de joueur à ce tournoi. "
                  "Veuillez créer un autre joueur.")
            return ViewTournament.view_consultation_tournament_menu()

        print("Sélectionner le joueur que vous voulez ajouter :")
        try:
            entry = int(input())
            while True:
                for iPlayer in range(len(players_available)):
                    if entry == iPlayer + 1:
                        self.players.append(players_available[iPlayer])
                        self.save_table()
                        print("Joueur ajouté au tournoi")
                        print("Voulez-vous ajouter un autre joueur ? O ou "
                              "autre touche)")
                        entry = input()
                        if entry == "O":
                            return ViewPlayerByTournament. \
                                view_add_players(self)
                        else:
                            return ViewTournamentByTournament. \
                                view_consultation_tournament(self)
                print("Saisie incorrecte, veuillez recommencer :")
        except ValueError:
            print("Saisie incorrecte, veuillez recommencer :")


class ViewPlayer:
    @classmethod
    def view_player_menu(cls):
        i_correct_input = False
        while not i_correct_input:
            print("1- Consultation joueurs")
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
        i_player_created = False
        player_created = {}
        while ControllerCreationPlayer.controller_creation_player(
                player_created) != "OK" and not i_player_created:
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
            if ControllerCreationPlayer.controller_creation_player(
                    player_created) == "OK":
                Player(player_created).save_table()
                print("Joueur créé")
                i_player_created = True
                ViewPlayer.view_player_menu()
            else:
                for i in ControllerCreationPlayer.controller_creation_player(
                        player_created):
                    print(i)


class ViewPlayerByPlayer(Player):
    def view_consultation_player(self):
        print("Détails du joueur sélectionné :")
        print()
        print("Nom : ", self.last_name)
        print("Prénom : ", self.first_name)
        print("Date d'anniversaire : ", self.birthday)
        print("Sexe : ", self.gender)
        print("Classement : ", self.ranking)
        print()
        print("Sélectionner l'action désirée :")
        print("1- Retour au menu précédent")
        while True:
            try:
                entry = int(input())
                if entry == 1:
                    return ViewPlayer.view_player_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")
