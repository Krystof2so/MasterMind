from collections import Counter
from enum import StrEnum
from os import system, name as nm
from random import choice

from colorama import Fore, Style

# Todo:
#  - Docstrings à finaliser + commentaires + annotations de type
#  - Autre algorithme pour la méthode '_evaluate_game_turn(self, player_combo: list)'


class DatasText(StrEnum):
    ASK_SECRET_COMBO = "Veuillez saisir vos quatre chiffres pour les couleurs : "
    ERROR_INPUT = "Votre saisie est incorrecte..."
    LOOSE = "Perdu la combinaison secrète était :\n"
    RULES_MAIN = """JEU DU MASTERMIND
Trouver la bonne combinaison de quatre couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.
Entrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles."""
    WIN = "Bravo, la combinaison était bien :\n"


class MasterMind:
    # Définition des couleurs à l'aide de colorama
    COLORS = {
        'Jaune': Fore.LIGHTYELLOW_EX,
        'Bleu': Fore.BLUE,
        'Rouge': Fore.RED,
        'Vert': Fore.GREEN,
        'Blanc': Fore.LIGHTWHITE_EX,
        'Magenta': Fore.MAGENTA
    }
    # Objets nécessaires à la classe
    COLOUR_SQUARE = "\u2588"
    COLOUR_INDICATOR = "\u25CF"
    LIM_SECRET_COMBO = 4
    LIM_TOUR = 10

    def __init__(self):
        self.all_colors_names, self.all_colors = list(MasterMind.COLORS.keys()), list(MasterMind.COLORS.values())
        self.secret_combo: list = [choice(self.all_colors_names) for _ in range(MasterMind.LIM_SECRET_COMBO)]
        self.secret_colors: str = self._four_colors(self.secret_combo)

    @staticmethod
    def _four_colors(color_list: list) -> str:
        """
        Génère et retourne les quatre carrés de couleurs.
        :param color_list: Les quatre noms de couleurs.
        :return str: La chaîne des quatre carrés de couleurs.
        """
        return "".join([f" {MasterMind.COLORS[color]}{MasterMind.COLOUR_SQUARE}{Style.RESET_ALL} "
                        for color in color_list])

    def _ask_secret_combo(self) -> list:
        """
        Demande et retourne la combinaison du joueur.
        :return list: La liste des noms de couleur choisis par le joueur.
        """
        while True:
            user_combo = input(DatasText.ASK_SECRET_COMBO)
            if (len(user_combo) != MasterMind.LIM_SECRET_COMBO or not user_combo.isdigit() or
                    any(int(n) not in range(1, len(MasterMind.COLORS) + 1) for n in user_combo)):
                print(DatasText.ERROR_INPUT)
                continue
            return [self.all_colors_names[int(n) - 1] for n in user_combo]

    def _evaluate_game_turn(self, player_combo: list):
        red_indicators = white_indicators = 0
        copy_player_combo = player_combo.copy()
        copy_secret_combo = self.secret_combo.copy()

        # Évaluation des indices rouges (bonne position dans la combinaison)
        for player_color, secret_color in zip(player_combo, self.secret_combo):
            if player_color == secret_color:
                red_indicators += 1
                copy_player_combo.remove(player_color)
                copy_secret_combo.remove(secret_color)

        # Évaluation des indices blancs (mauvaise position dans la combinaison)
        player_counts = Counter(copy_player_combo)
        secret_counts = Counter(copy_secret_combo)
        for color, count in player_counts.items():
            if color in secret_counts:
                white_indicators += min(count, secret_counts[color])

        return red_indicators, white_indicators

    def _game_rules(self) -> str:
        """
        Pour l'affichage des règles du jeu.
        :return str: Annonce des règles du jeu avant début de partie.
        """
        sentence_color = "".join([f"[{i + 1}]: {self.all_colors[i]}{self.all_colors_names[i]}{Style.RESET_ALL}\t"
                                  for i in range(len(self.all_colors_names))])
        return f"{DatasText.RULES_MAIN}\n{sentence_color}"

    def game(self):
        print(self._game_rules())
        tour = 0
        while True:
            tour += 1
            player_combination = self._ask_secret_combo()
            indicators = self._evaluate_game_turn(player_combination)
            all_red_indicators = f"{Fore.RED}{MasterMind.COLOUR_INDICATOR}{Style.RESET_ALL}" * indicators[0]
            all_white_indicators = f"{Fore.LIGHTWHITE_EX}{MasterMind.COLOUR_INDICATOR}{Style.RESET_ALL}" * indicators[1]
            # Les couleurs du joueur :
            print(f"{self._four_colors(player_combination)} Indicateurs : {all_red_indicators}{all_white_indicators}")
            if player_combination == self.secret_combo:
                return DatasText.WIN + self.secret_colors
            if tour == MasterMind.LIM_TOUR:
                return DatasText.LOOSE + self.secret_colors


if __name__ == "__main__":
    system('cls' if nm == 'nt' else 'clear')
    print(MasterMind().game())
