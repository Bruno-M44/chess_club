from view.view_player import ViewPlayer, ViewPlayerByTournament
from view.view_tournament import ViewTournament, ViewTournamentByTournament
from view.view_match import ViewMatch, ViewTour
from view.clear_terminal import ClearTerminal


class ViewReport:
    @classmethod
    def view_report_menu(cls):
        from view.view_main_menu import ViewMain
        ClearTerminal.clear_terminal()
        while True:
            print("1- Liste de tous les acteurs par ordre alphabétique")
            print("2- Liste de tous les acteurs par classement")
            print("3- Liste de tous les joueurs d'un tournoi par ordre "
                  "alphabétique")
            print("4- Liste de tous les joueurs d'un tournoi par classement")
            print("5- Liste de tous les joueurs d'un tournoi par score")
            print("6- Liste de tous les tournois")
            print("7- Liste de tous les tours d'un tournoi")
            print("8- Liste de tous les matchs d'un tournoi")
            print("9- Retour au menu précédent")
            try:
                entry = int(input())
                if entry == 1:
                    return ViewPlayer.view_players_by_alphabetical_order()
                elif entry == 2:
                    return ViewPlayer.view_players_by_ranking()
                elif entry == 3:
                    return ViewPlayerByTournament.\
                        view_players_by_alphabetical_order(
                            ViewTournament.view_consultation_tournament_menu())
                elif entry == 4:
                    return ViewPlayerByTournament.\
                        view_players_by_ranking(
                            ViewTournament.view_consultation_tournament_menu())
                elif entry == 5:
                    return ViewPlayerByTournament.\
                        view_players_by_score(
                            ViewTournament.view_consultation_tournament_menu())
                elif entry == 6:
                    return ViewTournamentByTournament.\
                        view_consultation_tournament(
                            ViewTournament.view_consultation_tournament_menu())
                elif entry == 7:
                    return ViewTour.view_tours(
                        ViewTournament.view_consultation_tournament_menu())
                elif entry == 8:
                    return ViewMatch.view_matches(ViewTour.view_tour_menu(
                        ViewTournament.view_consultation_tournament_menu()))
                elif entry == 9:
                    return ViewMain.view_main_menu()
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")
