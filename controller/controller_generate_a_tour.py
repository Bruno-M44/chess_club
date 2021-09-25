from models.match import Match


class ControllerGenerateATour:
    def __init__(self, tournament):
        self.tournament = tournament

    def player_score(self, player):
        score = 0
        for tour in self.tours:
            for match in tour.matches:
                if match.player_1.__dict__ == player.__dict__:
                    score += match.score_1
                elif match.player_2.__dict__ == player.__dict__:
                    score += match.score_2
        return score

    def players_met(self, player):
        players_met = []
        for tour in self.tours:
            for match in tour.matches:
                if match.player_1.__dict__ == player.__dict__:
                    players_met.append(match.player_2.__dict__)
                elif match.player_2.__dict__ == player.__dict__:
                    players_met.append(match.player_1.__dict__)
        return players_met

    def player_played_this_tour(self, player):
        player_played = False
        for match in self.tours[-1].matches:
            if match.player_1.__dict__ == player.__dict__:
                player_played = True
            elif match.player_2.__dict__ == player.__dict__:
                player_played = True
        return player_played

    def generate_a_tour(self):
        if not self.tours[0].matches:  # 1st tour generated
            players_sorted = sorted(self.players,
                                    key=lambda players: int(players.ranking))
            for iPlayer in range(int(len(players_sorted) / 2)):
                self.tours[0].matches.append(Match(
                    {"player_1": players_sorted[iPlayer].__dict__,
                     "score_1": 0,
                     "player_2": players_sorted[int(len(players_sorted) / 2
                                                    + iPlayer)].__dict__,
                     "score_2": 0}))
        else:
            players_sorted = sorted(self.players,
                                    key=lambda player:
                                    (-ControllerGenerateATour.
                                     player_score(self, player),
                                     int(player.ranking)))
            # sorted by score (decreasing with the sign -) and ranking
            for iPlayer in range(len(players_sorted)):
                if not ControllerGenerateATour. \
                        player_played_this_tour(self, players_sorted[iPlayer]):
                    j = 1
                    while True:
                        try:
                            player_met = players_sorted[iPlayer + j].\
                                         __dict__ in ControllerGenerateATour.\
                                         players_met(self,
                                                     players_sorted[iPlayer])
                            if player_met:
                                j += 1
                            else:
                                self.tours[-1].matches.append(Match({
                                    "player_1":
                                        players_sorted[
                                            iPlayer].__dict__,
                                    "score_1": 0,
                                    "player_2":
                                        players_sorted[
                                            iPlayer + j].__dict__,
                                    "score_2": 0
                                }))
                                break
                        except IndexError:
                            print(
                                "Il n'est plus possible de générer de matchs.")
                            break
