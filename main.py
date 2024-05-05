from collections import Counter
from enum import StrEnum
from os import system, name as nm
from random import choice

from colorama import Fore, Style


class DatasText(StrEnum):
    """Ensemble des données textuelles affichées dans le terminal."""
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
    """Ensemble des constantes utilisées. Paramétrages du jeu."""
    # Définition des couleurs à l'aide de colorama
    COLORS: dict = {
        'Jaune': Fore.LIGHTYELLOW_EX,
        'Bleu': Fore.BLUE,
        'Rouge': Fore.RED,
        'Vert': Fore.GREEN,
        'Blanc': Fore.LIGHTWHITE_EX,
        'Magenta': Fore.MAGENTA
    }
    # Objets nécessaires et constantes
    COLOUR_SQUARE, COLOUR_INDICATOR = "\u25A0", "\u25CF"
    LIM_SECRET_COMBO, LIM_TOUR = 4, 10

    def __init__(self):
        self._all_colors_names, self._all_colors = list(MasterMind.COLORS.keys()), list(MasterMind.COLORS.values())
        self._secret_combo: list = [choice(self._all_colors_names) for _ in range(MasterMind.LIM_SECRET_COMBO)]
        self._secret_colors: str = self._four_colors(self._secret_combo)

    @staticmethod
    def _four_colors(color_list: list[str]) -> str:
        """
        Génère et retourne les quatre carrés de couleurs.
        :param color_list: Les quatre noms de couleurs.
        :return str: La chaîne des quatre carrés de couleurs.
        """
        return "".join([f" {MasterMind.COLORS[color]}{MasterMind.COLOUR_SQUARE}{Style.RESET_ALL} "
                        for color in color_list])

    def _ask_secret_combo(self) -> list[str]:
        """
        Demande et retourne la combinaison du joueur.
        :return list: La liste des noms de couleur choisis par le joueur.
        """
        while True:
            user_combo = input(DatasText.ASK_SECRET_COMBO)
            # Condition pour vérifier la saisie de l'utilisateur qui doit contenir 4 chiffres :
            if not (len(user_combo) == MasterMind.LIM_SECRET_COMBO and user_combo.isdigit() and
                    all(int(n) in range(1, len(MasterMind.COLORS) + 1) for n in user_combo)):
                print(DatasText.ERROR_INPUT)
                continue
            return [self._all_colors_names[int(n) - 1] for n in user_combo]

    def _evaluate_game_turn(self, player_combo: list[str]) -> tuple[int, int]:
        """
        Compare la proposition du joueur avec la combinaison à trouver, et fournit en retour les indicateurs.
        :param player_combo: Liste des couleurs proposées par le joueur.
        :return tuple: Le nombre d'indicateurs rouges et blancs.
        """
        red_indicators = white_indicators = 0
        #  Counter pour compter les occurrences de chaque couleur dans les combinaisons
        secret_counts = Counter(self._secret_combo)
        player_counts = Counter(player_combo)

        # Deux itérations sur la combinaison du joueur :
        # 1 - Évaluation des indices rouges (bonne position dans la combinaison)
        for player_color, secret_color in zip(player_combo, self._secret_combo):
            if player_color == secret_color:
                red_indicators += 1
                # Décrémentez le compteur d'occurrences pour cette couleur dans la combinaison secrète
                secret_counts[player_color] -= 1

        # 2 - Évaluation des indices blancs (mauvaise position dans la combinaison)
        for color, count in player_counts.items():
            if color in secret_counts:
                # min() = minimum d'occurrences = nombre d'indicateurs blancs
                white_indicators += min(count, secret_counts[color])
                # Nouvelle décrémentation (évite les comptages doubles)
                secret_counts[color] -= min(count, secret_counts[color])

        return red_indicators, white_indicators

    def _game_rules(self) -> str:
        """
        Pour l'affichage des règles du jeu.
        :return str: Annonce des règles du jeu avant début de partie.
        """
        sentence_color = "".join([f"[{i + 1}]: {self._all_colors[i]}{self._all_colors_names[i]}{Style.RESET_ALL}\t"
                                  for i in range(len(self._all_colors_names))])  # Toutes les couleurs du jeu
        return f"{DatasText.RULES_MAIN}\n{sentence_color}"

    def game(self) -> str:
        """
        Méthode principale du jeu, appelée depuis le 'main'.
        :return str: La phrase finale du jeu : gagné ou perdu.
        """
        print(self._game_rules())
        tour = 0
        while True:  # Deux conditions de sortie : combinaison trouvée ou limite nombre de tours de jeu
            tour += 1
            player_combination = self._ask_secret_combo()
            # Générer les indicateurs à afficher :
            indicators = self._evaluate_game_turn(player_combination)
            all_red_indicators = f"{Fore.RED}{MasterMind.COLOUR_INDICATOR}{Style.RESET_ALL}" * indicators[0]
            all_white_indicators = f"{Fore.LIGHTWHITE_EX}{MasterMind.COLOUR_INDICATOR}{Style.RESET_ALL}" * indicators[1]
            # Affichage combinaison joueur + indicateurs :
            print(f"{self._four_colors(player_combination)} Indicateurs : {all_red_indicators}{all_white_indicators}")
            # Conditions de sortie de la boucle de jeu :
            if player_combination == self._secret_combo or tour == MasterMind.LIM_TOUR:
                end_game_msg = DatasText.WIN if player_combination == self._secret_combo else DatasText.LOOSE
                return end_game_msg + self._secret_colors


if __name__ == "__main__":
    system('cls' if nm == 'nt' else 'clear')
    print(MasterMind().game())
