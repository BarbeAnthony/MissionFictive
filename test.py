import os
import unittest
from unittest.mock import patch
import questionnaire


class TestsQuestion(unittest.TestCase):
    def test_question_from_data(self):
        print("\ntest : création de question depuis des données similaire à création de question depuis le constructeur normal")
        question1 = questionnaire.Question("Texte question", ["choix1", "choix2", "choix3"], "choix2")
        question2 = questionnaire.Question.from_data({"titre": "Texte question", "choix": (("choix1", False), ("choix2", True), ("choix3", False))})
        self.assertEqual(question1.titre, question2.titre)
        self.assertEqual(question1.choix, question2.choix)
        self.assertEqual(question1.bonne_reponse, question2.bonne_reponse)

    def test_bonne_mauvaise_reponse(self):
        print("\ntest : bonne ou mauvaise réponse donnée")
        question = questionnaire.Question("Texte question", ("choix1", "choix2", "choix3"), "choix2")
        with patch("builtins.input", return_value="2"):
            self.assertEqual(question.poser(), True)
        with patch("builtins.input", return_value="3"):
            self.assertEqual(question.poser(), False)


class TestQuestionnaire(unittest.TestCase):
    def test_lancer_alien_debutant(self):
        print("\ntest : cinema_alien_debutant.json (fichier complet et valide)")
        filename = os.path.join("test_data", "cinema_alien_debutant.json")
        quizz = questionnaire.Quizz.from_json_file(filename)
        self.assertIsNotNone(quizz)
        self.assertEqual(quizz.title, "Alien")
        self.assertEqual(quizz.category, "Cinéma")
        self.assertEqual(quizz.difficulty, "débutant")
        self.assertEqual(quizz.nb_questions, 10)
        with patch("builtins.input", return_value="1"):
            self.assertEqual(quizz.lancer(), 2)

    def test_formats_incomplets(self):
        print("\ntest : sans_categorie_ni_difficulte.json (fichier incomplet mais valide)")
        filename = os.path.join("test_data", "sans_categorie_ni_difficulte.json")
        quizz = questionnaire.Quizz.from_json_file(filename)
        self.assertEqual(quizz.category, "inconnue")
        self.assertEqual(quizz.difficulty, "inconnue")
        with patch("builtins.input", return_value="1"):
            self.assertEqual(quizz.lancer(), 2)

        print("\ntest : uniquement_titre.json (fichier invalide)")
        filename = os.path.join("test_data", "uniquement_titre.json")
        quizz = questionnaire.Quizz.from_json_file(filename)
        self.assertIsNone(quizz)

        print("\ntest : uniquement_questions.json (fichier invalide)")
        filename = os.path.join("test_data", "uniquement_questions.json")
        quizz = questionnaire.Quizz.from_json_file(filename)
        self.assertIsNone(quizz)

        print("\ntest : structure_complete_mais_toutes_questions_invalides.json")
        filename = os.path.join("test_data", "structure_complete_mais_toutes_questions_invalides.json")
        quizz = questionnaire.Quizz.from_json_file(filename)
        self.assertIsNone(quizz)


