from models.tournament import Tournament, Tour
from controller.controller_generate_a_tour import ControllerGenerateATour
from view.clear_terminal import ClearTerminal
from datetime import datetime


class ViewTour:
    def __init__(self, tournament):
        self.tournament = tournament

    def view_generate_a_tour(self):
        from view.view_tournament import ViewTournament
        ClearTerminal.clear_terminal()
        tour_created = {"name": str("Round " +
                                    str(len(self.tours) + 1)),
                        "start_date": datetime.today().strftime('%d/%m/%Y'),
                        "end_date": "",
                        "matches": []}
        self.tours.append(Tour(tour_created))
        ControllerGenerateATour.generate_a_tour(self)
        Tournament.save_table(self)
        ClearTerminal.clear_terminal()
        print("Entrer les résultats du ", tour_created["name"], " :")
        print("Appuyer sur 'r' pour sortir")
        if input() == "r":
            return ViewTournament.view_tournament_menu()
        else:
            return ViewTour.view_results_entry(self)

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
        self.tours[-1].end_date = datetime.today().strftime('%d/%m/%Y')
        self.save_table()
        print("Les résultats ont été sauvegardés")
        if len(self.tours) < self.number_of_tours:
            print("Le tour suivant va être généré. Appuyer sur 'r' si vous "
                  "voulez revenir au menu du tournoi")
            if input() == "r":
                return ViewTournament.view_tournament_menu()
            else:
                return ViewTour.view_generate_a_tour(self)
        else:
            print("Le tournoi a entièrement été généré, il n'est plus "
                  "modifiable.")
            return ViewTournament.view_tournament_menu()

    def view_tours(self):
        from view.view_report import ViewReport
        ClearTerminal.clear_terminal()
        print("Voici les différents tours du tournoi :")
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
