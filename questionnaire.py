import json
import sys


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromData(data):
        # ....
        q = Question(data[2], data[0], data[1])
        return q

    def poser(self):
        print("QUESTION")
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

    def lancer(self):
        score = 0
        for question in self.questions:
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


def create_quizz_object_from_json_file(json_file_name):
    # Lecture et désérialisation du JSON
    try:
        json_file = open(json_file_name, "r")
    except FileNotFoundError:
        print("ERREUR: impossible d'ouvrir le fichier " + json_file_name)
        return None
    json_text = json_file.read()
    json_file.close()
    quizz_from_json = json.loads(json_text)
    try:
        # préparation des variables d'instances du Quizz à partir du dictionnaire quizz_from_json
        quizz_category = quizz_from_json["categorie"]
        quizz_title = quizz_from_json["titre"]
        quizz_difficulty = quizz_from_json["difficulte"]
        quizz_questions = []
        for question in quizz_from_json["questions"]:
            # préparation des variables d'instances des questions à partir du dictionnaire quizz_from_json
            question_title = question["titre"]
            question_proposals = []
            question_good_answer = ""
            for choix in question["choix"]:
                question_proposals.append(choix[0])
                if choix[1]:
                    question_good_answer = choix[0]
            # Création des objets Question() et ajout à la variable d'instance questions du Quizz
            new_question = Question(question_title, question_proposals, question_good_answer)
            quizz_questions.append(new_question)
    except KeyError:
        print("KeyError: impossible de créer un questionnaire à partir du fichier " + json_file_name)
        return None
    # Création de l'objet Quizz avec les variables d'instances préparées
    return Quizz(quizz_category, quizz_title, quizz_difficulty, quizz_questions)


quizz = create_quizz_object_from_json_file(sys.argv[1])
if quizz:
    quizz.lancer()
else:
    print("ERREUR: Le questionnaire n'a pas pu être chargé. Fin du programme.")
