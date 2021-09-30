from models.tournament import Tournament
from tinydb import TinyDB
from controller.controller_creation import ControllerCreationTournament
from view.view_player import ViewPlayerByTournament
from view.view_match import ViewTour
from view.clear_terminal import ClearTerminal


class ViewTournament:
    @classmethod
    def view_tournament_menu(cls):
        ClearTerminal.clear_terminal()
        while True:
            print("1- Création nouveau tournoi (à noter qu'il faut d'abord "
                  "créer un joueur avant de pouvoir l'ajouter au tournoi)")
            print("2- Modification tournoi (ajout joueur, génération tour, "
                  "entrer résultats)")
            print("3- Retour au menu précédent")
            print("Saisir 1, 2 ou 3 puis entrée pour faire votre choix :")
            try:
                entry = int(input())
                if entry == 1:
                    return ViewTournament.view_creation_tournament()
                elif entry == 2:
                    return ViewTournamentByTournament. \
                        view_modification_tournament(
                            ViewTournament.view_consultation_tournament_menu())
                elif entry == 3:
                    from view.view_main_menu import ViewMain
                    return ViewMain.view_main_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")

    @classmethod
    def view_creation_tournament(cls):
        ClearTerminal.clear_terminal()
        tournament_created = {}
        print("Saisir le nom du tournoi :")
        save_input = input()
        while not ControllerCreationTournament.controller_name(save_input):
            save_input = input()
        tournament_created["name"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir le lieu du tournoi :")
        save_input = input()
        while not ControllerCreationTournament.controller_place(save_input):
            save_input = input()
        tournament_created["place"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir la date de début du tournoi (format JJ/MM/SSAA) :")
        save_input = input()
        while not ControllerCreationTournament.controller_start_date(
                save_input):
            save_input = input()
        tournament_created["start_date"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir la date de fin du tournoi (format JJ/MM/SSAA) "
              "- facultatif :")
        save_input = input()
        while not ControllerCreationTournament.controller_end_date(save_input):
            save_input = input()
        tournament_created["end_date"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir le nombre de tour du tournoi - facultatif (4 par "
              "défaut) :")
        save_input = input()
        while not ControllerCreationTournament.controller_number_of_tours(
                save_input):
            save_input = input()
        tournament_created["number_of_tours"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir le contrôle du temps du tournoi. Saisir 'bullet', "
              "'blitz' ou 'coup rapide' :")
        save_input = input()
        while not ControllerCreationTournament.controller_time_control(
                save_input):
            save_input = input()
        tournament_created["time_control"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir la description du tournoi :")
        tournament_created["description"] = input()

        tournament_created["tours"] = []
        tournament_created["players"] = []

        Tournament(tournament_created).save_table()

        ClearTerminal.clear_terminal()
        print("Tournoi créé")
        input()
        return ViewTournament.view_tournament_menu()

    @classmethod
    def view_consultation_tournament_menu(cls):
        ClearTerminal.clear_terminal()
        for iTournament in range(len(TinyDB("tables.json").table(
                "tournaments").all())):
            print(iTournament + 1, "- ",
                  TinyDB("tables.json").table("tournaments").all()[
                      iTournament]["name"])
        print(
            "Sélectionner le tournoi sur lequel vous voulez agir (entrée "
            "sans saisie pour retour au menu précédent) :")
        while True:
            entry = input()
            try:
                entry = int(entry)
                for iTournament in range(
                        len(TinyDB("tables.json").table("tournaments").all())):
                    if entry == iTournament + 1:
                        return Tournament(TinyDB("tables.json").
                                          table("tournaments").
                                          all()[iTournament])
                print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                if entry == "":
                    return ViewTournament.view_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")


class ViewTournamentByTournament:
    def __init__(self, tournament):
        self.tournament = tournament

    def view_consultation_tournament(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Détails du tournoi sélectionné :")
        print()
        print("Nom : ", self.name)
        print("Lieu : ", self.place)
        print("Date de début : ", self.start_date)
        print("Date de fin : ", self.end_date)
        print("Nombre de tours : ", self.number_of_tours)
        print("Contrôle du temps : ", self.time_control)
        print("Description : ", self.description)
        input()
        return ViewReport.view_report_menu()

    def view_modification_tournament(self):
        ClearTerminal.clear_terminal()
        print("Sélectionner l'action désirée :")
        if len(self.players) < 4 or (len(self.players) < 8 and
                                     self.number_of_tours == 4) and \
                ViewPlayerByTournament.players_available(self):
            print("1- Ajout joueurs")
            print("2- Retour au menu précédent")
        elif not self.tours and ViewPlayerByTournament. \
                players_available(self) and (len(self.players) != 8 or
                                             self.number_of_tours != 4):
            print("1- Ajout joueurs")
            print("2- Générer un tour")
            print("3- Retour au menu précédent")
        elif not self.tours:
            print("1- Générer un tour")
            print("2- Retour au menu précédent")
        elif self.tours[-1].matches and \
                self.tours[-1].matches[0].score_1 == 0 and \
                self.tours[-1].matches[0].score_2 == 0:
            print("1- Rentrer les résultats du dernier tour généré")
            print("2- Retour au menu précédent")
        elif len(self.tours) < self.number_of_tours:
            print("1- Générer un tour")
            print("2- Retour au menu précédent")
        else:
            print("Le tournoi n'est pas modificable en l'état.")
            print("1- Retour au menu précédent")

        while True:
            try:
                entry = int(input())
                if len(self.players) < 4 and \
                        ViewPlayerByTournament.players_available(self):
                    if entry == 1:
                        return ViewPlayerByTournament.view_add_players(self)
                    elif entry == 2:
                        return ViewTournament.view_tournament_menu()
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
                        return ViewTournament.view_tournament_menu()
                elif not self.tours and ViewPlayerByTournament. \
                        players_available(self) and (len(self.players) != 8
                                                     or self.number_of_tours
                                                     != 4):
                    if entry == 1:
                        return ViewPlayerByTournament.view_add_players(self)
                    elif entry == 2:
                        return ViewTour.view_generate_a_tour(self)
                    elif entry == 3:
                        return ViewTournament.view_tournament_menu()
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
                        return ViewTournament.view_tournament_menu()
                elif not self.tours:
                    if entry == 1:
                        return ViewTour.view_generate_a_tour(self)
                    elif entry == 2:
                        return ViewTournament.view_tournament_menu()
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
                        return ViewTournament.view_tournament_menu()
                elif self.tours[-1].matches and \
                        self.tours[-1].matches[0].score_1 == 0 and \
                        self.tours[-1].matches[0].score_2 == 0:
                    if entry == 1:
                        return ViewTour.view_results_entry(self)
                    elif entry == 2:
                        return ViewTournament.view_tournament_menu()
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
                        return ViewTournament.view_tournament_menu()
                elif len(self.tours) < self.number_of_tours:
                    if entry == 1:
                        return ViewTour.view_generate_a_tour(self)
                    elif entry == 2:
                        return ViewTournament.view_tournament_menu()
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
                        return ViewTournament.view_tournament_menu()
                else:
                    if entry == 1:
                        print("Le tournoi n'est plus modifiable")
                        return ViewTournament.view_tournament_menu()
                    else:
                        print("Saisie incorrecte, veuillez recommencer :")
                        return ViewTournament.view_tournament_menu()
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")
