import json
import sys


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_data(data_question):
        # transforme des données au format titre, ((proposition1, False), (proposition2, True)...) en Question(titre, [proposition1, proposition2...], proposition2)
        proposals = [choix[0] for choix in data_question["choix"]]
        good_answer = [choix[0] for choix in data_question["choix"] if choix[1]]
        if len(good_answer) != 1:
            return None
        return Question(data_question["titre"], proposals, good_answer[0])

    def poser(self):
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")

        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Quizz:
    def __init__(self, category, title, difficulty, questions):
        self.category = category
        self.title = title
        self.difficulty = difficulty
        self.questions = questions
        self.nb_questions = len(questions)

    def from_json_file(json_file_name):
        try:
            json_file = open(json_file_name, "r")
        except FileNotFoundError:
            print("ERREUR: impossible d'ouvrir le fichier " + json_file_name)
            return None
        json_text = json_file.read()
        json_file.close()
        json_data = json.loads(json_text)
        return Quizz.from_json_data(json_data)

    def from_json_data(json_data):
        try:
            quizz_category = json_data["categorie"]
            quizz_title = json_data["titre"]
            quizz_difficulty = json_data["difficulte"]
            quizz_questions = [Question.from_data(question) for question in json_data["questions"]]
            # Eliminer les questions None qui n'ont pas pu être créées à cause du formal des données
            quizz_questions = [q for q in quizz_questions if q]
        except KeyError:
            print("KeyError: impossible de créer un questionnaire car les données du .json ne sont pas au format attendu.")
            return None
        if len(quizz_questions) == 0:
            print("Aucune des questions de ce fichier n'est compatible avec ce programme. Elles doivent obligatoirement avoir une seule bonne réponse.")
            return None
        return Quizz(quizz_category, quizz_title, quizz_difficulty, quizz_questions)

    def lancer(self):
        print("\n### Début du questionnaire sur " + self.title + " ###")
        print("  Catégorie : " + self.category)
        print("  Difficulté : " + self.difficulty)
        print("  " + str(self.nb_questions) + " questions\n")
        score = 0
        question_counter = 1
        for question in self.questions:
            print("QUESTION " + str(question_counter) + "/" + str(self.nb_questions))
            if question.poser():
                score += 1
            question_counter += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


try:
    json_file = sys.argv[1]
except IndexError:
    print("ERREUR : Vous devez ajouter un fichier json en argument : python questionnaire.py mon_questionnaire.json")
else:
    quizz = Quizz.from_json_file(json_file)
    if quizz:
        quizz.lancer()
