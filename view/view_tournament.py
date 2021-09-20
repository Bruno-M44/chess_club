from models.tournament import Tournament
from view.view_player import ViewPlayerByTournament
from view.view_match import ViewMatch
from tinydb import TinyDB
from controller.controller_creation import ControllerCreationTournament


class ViewTournament:
    @classmethod
    def view_tournament_menu(cls):
        while True:
            print("1- Consultation tournois")
            print("2- Création nouveau tournoi")
            print("3- Retour au menu précédent")
            print("Saisir 1, 2 ou 3 puis entrée pour faire votre choix :")
            try:
                entry = int(input())
                if entry == 1:
                    return ViewTournament.view_consultation_tournament_menu()
                elif entry == 2:
                    return ViewTournament.view_creation_tournament()
                elif entry == 3:
                    from view.view_main_menu import ViewMain
                    return ViewMain.view_main_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")

    @classmethod
    def view_creation_tournament(cls):
        i_tournament_created = False
        tournament_created = {}
        while ControllerCreationTournament. \
                controller_creation_tournament(tournament_created) != "OK" \
                and not i_tournament_created:
            print("Saisir le nom du tournoi :")
            tournament_created["name"] = input()
            print("Saisir le lieu du tournoi :")
            tournament_created["place"] = input()
            print("Saisir la date de début du tournoi (format JJ/MM/SSAA) :")
            tournament_created["start_date"] = input()
            print("Saisir la date de fin du tournoi (format JJ/MM/SSAA) - "
                  "facultatif :")
            tournament_created["end_date"] = input()
            print("Saisir le nombre de tour du tournoi - facultatif (4 par "
                  "défaut) :")
            tournament_created["number_of_tours"] = input()
            print("Saisir le contrôle du temps du tournoi. Saisir 'bullet', "
                  "'blitz' ou 'coup rapide'")
            tournament_created["time_control"] = input()
            print("Saisir la description du tournoi - facultatif :")
            tournament_created["description"] = input()
            tournament_created["players"] = []
            tournament_created["tours"] = []
            if ControllerCreationTournament. \
                    controller_creation_tournament(tournament_created) == "OK":
                Tournament(tournament_created).save_table()
                print("Tournoi créé")
                i_tournament_created = True
                ViewTournament.view_tournament_menu()
            else:
                for i in range(len(
                        ControllerCreationTournament.
                        controller_creation_tournament(
                        tournament_created))):
                    print(ControllerCreationTournament.
                          controller_creation_tournament(
                           tournament_created)[i])

    @classmethod
    def view_consultation_tournament_menu(cls):
        for iTournament in range(len(TinyDB("tables.json").
                                     table("tournaments").all())):
            print(iTournament + 1, "- ",
                  TinyDB("tables.json").table("tournaments").all()[
                      iTournament]["name"])
        print(
            "Sélectionner le tournoi sur le quel vous voulez agir (entrée "
            "sans saisie pour retour au menu précédent) :")
        while True:
            entry = input()
            try:
                entry = int(entry)
                for iTournament in range(
                        len(TinyDB("tables.json").table("tournaments").all())):
                    if entry == iTournament + 1:
                        return ViewTournamentByTournament.\
                            view_consultation_tournament(
                                Tournament(TinyDB("tables.json").
                                           table("tournaments").
                                           all()[iTournament]))
                print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                if entry == "":
                    return ViewTournament.view_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")


class ViewTournamentByTournament(Tournament):
    def view_consultation_tournament(self):
        print("Détails du tournoi sélectionné :")
        print()
        print("Nom : ", self.name)
        print("Lieu : ", self.place)
        print("Date de début : ", self.start_date)
        print("Date de fin : ", self.end_date)
        print("Nombre de tours : ", self.number_of_tours)
        print("Contrôle du temps : ", self.time_control)
        print("Description : ", self.description)
        print()
        print("Sélectionner l'action désirée :")
        print("1- Liste de tous les joueurs par ordre alphabétique")
        print("2- Liste de tous les joueurs par classement")
        if len(self.players) < 4:
            print("3- Ajout joueurs")
            print("4- Retour au menu précédent")
        elif not self.tours:
            print("3- Ajout joueurs")
            print("4- Générer un tour")
            print("5- Retour au menu précédent")
        elif self.tours[-1].matches and \
                self.tours[-1].matches[0].score_1 == 0 and \
                self.tours[-1].matches[0].score_2 == 0:
            print("3- Rentrer les résultats du dernier tour généré")
            print("4- Liste de tous les matchs d'un tournoi")
            print("5- Retour au menu précédent")
        elif len(self.tours) < self.number_of_tours:
            print("3- Générer un tour")
            print("4- Liste de tous les matchs d'un tournoi")
            print("5- Retour au menu précédent")
        else:
            print("3- Liste de tous les matchs d'un tournoi")
            print("4- Retour au menu précédent")

        try:
            entry = int(input())
            if len(self.players) < 4:
                if entry == 1:
                    return ViewPlayerByTournament.\
                        view_players_by_alphabetical_order(self)
                elif entry == 2:
                    return ViewPlayerByTournament.view_players_by_ranking(self)
                elif entry == 3:
                    return ViewPlayerByTournament.view_add_players(self)
                elif entry == 4:
                    return ViewTournament.view_consultation_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
                    return ViewTournament.view_consultation_tournament(self)
            elif not self.tours:
                if entry == 1:
                    return ViewPlayerByTournament.\
                        view_players_by_alphabetical_order(self)
                elif entry == 2:
                    return ViewPlayerByTournament.view_players_by_ranking(self)
                elif entry == 3:
                    return ViewPlayerByTournament.view_add_players(self)
                elif entry == 4:
                    return ViewMatch.view_generate_a_tour(self)
                elif entry == 5:
                    return ViewTournament.view_consultation_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
                    return ViewTournament.view_consultation_tournament(self)
            elif self.tours[-1].matches and \
                    self.tours[-1].matches[0].score_1 == 0 and \
                    self.tours[-1].matches[0].score_2 == 0:
                if entry == 1:
                    return ViewPlayerByTournament.\
                        view_players_by_alphabetical_order(self)
                elif entry == 2:
                    return ViewPlayerByTournament.view_players_by_ranking(
                        self)
                elif entry == 3:
                    return ViewMatch.view_results_entry(self)
                elif entry == 4:
                    return ViewMatch.view_matches(self)
                elif entry == 5:
                    return ViewTournament.\
                        view_consultation_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
                    return ViewTournament.\
                        view_consultation_tournament(self)
            elif len(self.tours) < self.number_of_tours:
                if entry == 1:
                    return ViewPlayerByTournament.\
                        view_players_by_alphabetical_order(self)
                elif entry == 2:
                    return ViewPlayerByTournament.view_players_by_ranking(self)
                elif entry == 3:
                    return ViewMatch.view_generate_a_tour(self)
                elif entry == 4:
                    return ViewMatch.view_matches(self)
                elif entry == 5:
                    return ViewTournament.view_consultation_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
                    return ViewTournamentByTournament.\
                        view_consultation_tournament(self)
            else:
                if entry == 1:
                    return ViewPlayerByTournament.\
                        view_players_by_alphabetical_order(self)
                elif entry == 2:
                    return ViewPlayerByTournament.view_players_by_ranking(self)
                elif entry == 3:
                    return ViewMatch.view_matches(self)
                elif entry == 4:
                    return ViewTournament.view_consultation_tournament_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
                    return ViewTournamentByTournament.\
                        view_consultation_tournament(self)
        except ValueError:
            print("Saisie incorrecte, veuillez recommencer :")
