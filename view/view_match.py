from models.tournament import Tournament, Tour
from controller.controller_creation import ControllerCreationTour
from controller.controller_generate_a_tour import ControllerGenerateATour
from view.clear_terminal import ClearTerminal


class ViewTour:
    def __init__(self, tournament):
        self.tournament = tournament

    def view_generate_a_tour(self):
        from view.view_tournament import ViewTournament
        ClearTerminal.clear_terminal()
        tour_created = {}
        print("Saisir le nom du tour :")
        save_input = input()
        while not ControllerCreationTour.controller_name(save_input):
            save_input = input()
        tour_created["name"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir la date de début du tour (format JJ/MM/SSAA) :")
        save_input = input()
        while not ControllerCreationTour.controller_start_date(save_input):
            save_input = input()
        tour_created["start_date"] = save_input

        ClearTerminal.clear_terminal()
        print("Saisir la date de fin du tour (format JJ/MM/SSAA) - si non "
              "renseigné, le tour sera par défaut sur 1 journée :")
        save_input = input()
        while not ControllerCreationTour.controller_end_date(save_input):
            save_input = input()
        tour_created["end_date"] = save_input

        tour_created["matches"] = []

        self.tours.append(Tour(tour_created))
        ControllerGenerateATour.generate_a_tour(self)
        Tournament.save_table(self)
        ClearTerminal.clear_terminal()
        print("Le tour a été généré")
        input()
        return ViewTournament.view_tournament_menu()

    def view_results_entry(self):
        from view.view_tournament import ViewTournament
        ClearTerminal.clear_terminal()
        for match in self.tours[-1].matches:
            print("Joueur 1 :", match.player_1.last_name, " ",
                  match.player_1.first_name)
            print("rencontre")
            print("Joueur 2 :", match.player_2.last_name, " ",
                  match.player_2.first_name)
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
            ClearTerminal.clear_terminal()
        self.save_table()
        print("Les résultats ont été sauvegardés")
        input()
        return ViewTournament.view_tournament_menu()

    def view_tours(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici les différents tours du tournoi (nom, date de début, "
              "date de fin) :")
        for tour in self.tours:
            print(tour.name, tour.start_date, tour.end_date, sep=" ; ")
        input()
        return ViewReport.view_report_menu()

    def view_tour_menu(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        for iTour in range(len(self.tours)):
            print(iTour + 1, "- ", self.tours[iTour].__dict__["name"])
        print(
            "Sélectionner le tour du tournoi " + self.name + " sur lequel "
            "vous voulez agir (entrée sans saisie pour retour au menu "
            "précédent) :")
        while True:
            entry = input()
            try:
                entry = int(entry)
                for iTour in range(len(self.tours)):
                    if entry == iTour + 1:
                        return self.tours[iTour]
            except ValueError:
                if entry == "":
                    return ViewReport.view_report_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")


class ViewMatch:
    def __init__(self, tour):
        self.tour = tour

    def view_matches(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici les différents matchs du tour " + self.name + " :")
        for match in self.matches:
            if match.score_1 == 0 and match.score_2 == 0:
                print(match.player_1.last_name, match.player_1.first_name,
                      "- classement :", match.player_1.ranking)
                print("rencontre")
                print(match.player_2.last_name, match.player_2.first_name,
                      "- classement :", match.player_2.ranking)
                print()
            elif match.score_1 == 0.5:
                print(match.player_1.last_name, match.player_1.first_name,
                      "- classement :", match.player_1.ranking)
                print("a fait match nul avec")
                print(match.player_2.last_name, match.player_2.first_name,
                      "- classement :", match.player_2.ranking)
                print()
            elif match.score_1 == 1:
                print(match.player_1.last_name, match.player_1.first_name,
                      "- classement :", match.player_1.ranking)
                print("a battu")
                print(match.player_2.last_name, match.player_2.first_name,
                      "- classement :", match.player_2.ranking)
                print()
            else:
                print(match.player_2.last_name, match.player_2.first_name,
                      "- classement :", match.player_2.ranking)
                print("a battu")
                print(match.player_1.last_name, match.player_1.first_name,
                      "- classement :", match.player_1.ranking)
                print()
        input()
        ClearTerminal.clear_terminal()
        return ViewReport.view_report_menu()
