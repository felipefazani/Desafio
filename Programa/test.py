import unittest
import main


class TestaMain(unittest.TestCase):

    def setUp(self):
        self.data = {"a": 249, "b": 260, "c": 200, "d": 230}
        self.result = main.maiores(self.data, 2)

    def test_maiores(self):
        self.assertEqual(self.result[0][1], 260, "Maiores deveria uma lista organizada com os maiores")

    def test_maiores_n(self):
        self.assertEqual(len(self.result), 2, "Maiores deveria retornar uma lista com tamanho n")

    def test_maiores_tupla(self):
        self.assertEqual(type(self.result[0]), type(()), "Maiores deveria retornar uma lista de tuplas")
