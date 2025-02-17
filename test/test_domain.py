import unittest
from datetime import datetime
from main.error import ValidacaoError, CPFDuplicadoError 
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento


# Os testes abaixo cobrem RF1: Registrar Paciente
class EntitiesTest(unittest.TestCase):
    def test_rtb_cadastro_sucesso(self):
        """RTB: Cadastro realizado com sucesso"""
        paciente = Paciente("Maria", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertEqual(paciente.nome, "Maria")
        self.assertEqual(paciente.cpf, "11111111111")
        self.assertEqual(paciente.email, "maria@teste.com")
        self.assertEqual(paciente.nascimento, "21/03/2002")

    def test_rt1_nome_vazio(self):
        """RT1: Nome vazio"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertIn("nome", context.exception.message)

    def test_rt2_nome_caracteres_invalidos(self):
        """RT2: Nome com números"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria123", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertIn("nome", context.exception.message)

    def test_rt3_nome_caracteres_invalidos(self):
        """RT3: Nome com caracteres especiais"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria@#", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertIn("nome", context.exception.message)

    def test_rt4_cpf_com_letras(self):
        """RT4: CPF com letras"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111aaaa11", "maria@teste.com", "21/03/2002")
        self.assertIn("CPF", context.exception.message)

    def test_rt5_cpf_tamanho_incorreto(self):
        """RT5: CPF com tamanho inválido"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "1111111", "maria@teste.com", "21/03/2002")
        self.assertIn("CPF", context.exception.message)

    def test_rt6_cpf_vazio(self):
        """RT6: CPF vazio"""
        
        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "", "maria@teste.com", "21/03/2002")
        self.assertIn("CPF", context.exception.message)

    def test_rt7_cpf_duplicado(self):
        """RT7: CPF duplicado"""

        # Temos já um CPF cadastrado
        Paciente("Maria", "11111111111", "maria@teste.com", "21/03/2002")

        with self.assertRaises(CPFDuplicadoError) as context:
            Paciente("João", "11111111111", "joao@teste.com", "21/03/2000")
        self.assertIn("CPF", context.exception.message)

    def test_rt8_email_invalido(self):
        """RT8: E-mail inválido"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria.com", "21/03/2002")
        self.assertIn("E-mail", context.exception.message)

    def test_rt9_email_vazio(self):
        """RT9: E-mail vazio"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "", "21/03/2002")
        self.assertIn("E-mail", context.exception.message)

    def test_data_futura(self):
        """Data de nascimento futura"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "98765432100", "maria@teste.com", "10/12/2100")
        self.assertIn("A data de nascimento não pode ser futura", context.exception.message)

    def test_rt11_dia_invalido(self):
        """RT11: Dia inválido na data de nascimento"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria@teste.com", "32/03/2002")
        self.assertIn("Data de nascimento", context.exception.message)

    def test_rt12_mes_invalido(self):
        """RT12: Mês inválido na data de nascimento"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria@teste.com", "10/13/2002")
        self.assertIn("Data de nascimento", context.exception.message)

    def test_data_com_caracteres_invalidos(self):
        """Data de nascimento com caracteres inválidos"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Ana", "55566677788", "ana@teste.com", "10/XX/2002")  
        self.assertIn("Data de nascimento inválida", context.exception.message)
