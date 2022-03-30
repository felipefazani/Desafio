import unittest
import Programa


class TestaMain(unittest.TestCase):

    def test_maiores(self):
        data = {"a": 249, "b": 260, "c": 200, "d": 230}
        result = main.maiores(data, 2)
        self.assertEqual(result[0][1], 260, "Maiores deveria uma lista organizada com os maiores")

    def test_maiores_n(self):
        data = {"a": 249, "b": 260, "c": 200, "d": 230}
        result = main.maiores(data, 2)
        self.assertEqual(len(result), 2, "Maiores deveria retornar uma lista com tamanho n")

    def test_maiores_tupla(self):
        data = {"a": 249, "b": 260, "c": 200, "d": 230}
        result = main.maiores(data, 2)
        self.assertEqual(type(result[0]), type(()), "Maiores deveria retornar uma lista de tuplas")
