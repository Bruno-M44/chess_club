from models.tournament import Tournament, Tour
from controller.controller_creation import ControllerCreationTour
from controller.controller_generate_a_tour import ControllerGenerateATour


class ViewMatch(Tournament):
    def view_generate_a_tour(self):
        from view.view_tournament import ViewTournamentByTournament
        tour_created = {}
        while ControllerCreationTour.controller_creation_tour(tour_created) !=\
                "OK":
            print("Saisir le nom du tour :")
            tour_created["name"] = input()
            print("Saisir la date de début du tour (format JJ/MM/SSAA) :")
            tour_created["start_date"] = input()
            print("Saisir la date de fin du tour (format JJ/MM/SSAA) - si non "
                  "renseigné, le tour sera par défaut sur 1 journée :")
            tour_created["end_date"] = input()
            tour_created["matches"] = []
            if ControllerCreationTour.controller_creation_tour(tour_created)\
                    == "OK":
                self.tours.append(Tour(tour_created))
                ControllerGenerateATour.generate_a_tour(self)
                self.save_table()
                print("Le tour a été généré")
                return ViewTournamentByTournament.\
                    view_consultation_tournament(self)
            else:
                for i in range(len(ControllerCreationTour.
                                   controller_creation_tour(tour_created))):
                    print(ControllerCreationTour.
                          controller_creation_tour(tour_created)[i])

    def view_results_entry(self):
        from view.view_tournament import ViewTournamentByTournament
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
        self.save_table()
        print("Les résultats ont été sauvegardés")
        return ViewTournamentByTournament.view_consultation_tournament(self)

    def view_matches(self):
        from view.view_tournament import ViewTournamentByTournament
        print("Voici les différents matchs du tournoi :")
        for tour in self.tours:
            print("Au Tour :", tour.name, "- date de début : ",
                  tour.start_date, "- date de fin : ", tour.end_date)
            for match in tour.matches:
                if match.score_1 == 0 and match.score_2 == 0:
                    print(match.player_1.last_name, match.player_1.first_name,
                          "- classement :", match.player_1.ranking)
                    print("rencontre")
                    print(match.player_2.last_name, match.player_2.first_name,
                          "- classement :", match.player_2.ranking)
                elif match.score_1 == 0.5:
                    print(match.player_1.last_name, match.player_1.first_name,
                          "- classement :", match.player_1.ranking)
                    print("a fait match nul avec")
                    print(match.player_2.last_name, match.player_2.first_name,
                          "- classement :", match.player_2.ranking)
                elif match.score_1 == 1:
                    print(match.player_1.last_name, match.player_1.first_name,
                          "- classement :", match.player_1.ranking)
                    print("a battu")
                    print(match.player_2.last_name, match.player_2.first_name,
                          "- classement :", match.player_2.ranking)
                else:
                    print(match.player_2.last_name, match.player_2.first_name,
                          "- classement :", match.player_2.ranking)
                    print("a battu")
                    print(match.player_1.last_name, match.player_1.first_name,
                          "- classement :", match.player_1.ranking)
        return ViewTournamentByTournament.view_consultation_tournament(self)
