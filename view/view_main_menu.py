from view.view_tournament import ViewTournament
from view.view_player import ViewPlayer


class ViewMain:
    @classmethod
    def view_main_menu(cls):
        while True:
            print("1- Tournois (consultation, modification, création)")
            print("2- Joueurs (consultation, modification, création)")
            print("3- Quitter le programme")
            print("Saisir 1, 2 ou 3 puis entrée pour faire votre choix :")
            try:
                entry = int(input())
                if entry == 1:
                    return ViewTournament.view_tournament_menu()
                elif entry == 2:
                    return ViewPlayer.view_player_menu()
                elif entry == 3:
                    return "fin programme"
                else:
                    print("Saisie incorrecte, veuillez recommencer :")
            except ValueError:
                print("Saisie incorrecte, veuillez recommencer :")
