from view.view_tournament import ViewTournament
from view.view_player import ViewPlayer
from view.view_report import ViewReport
from view.clear_terminal import ClearTerminal


class ViewMain:
    @classmethod
    def view_main_menu(cls):
        ClearTerminal.clear_terminal()
        while True:
            print("1- Joueurs (consultation, modification, création)")
            print("2- Tournois (modification, création)")
            print("3- Rapports (consultation)")
            print("4- Quitter le programme")
            print("Saisir 1, 2, 3 ou 4 puis entrée pour faire votre choix :")
            try:
                entry = int(input())
                if entry == 1:
                    return ViewPlayer.view_player_menu()
                elif entry == 2:
                    return ViewTournament.view_tournament_menu()
                elif entry == 3:
                    return ViewReport.view_report_menu()
                elif entry == 4:
                    return "fin programme"
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")
