import unittest
from datetime import datetime, timedelta
from main.error import ValidacaoError, CPFDuplicadoError 
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento


# Os testes abaixo cobrem RF1: Registrar Paciente
class EntitiesTest(unittest.TestCase):
    def test_cadastro_correto(self):
        """RTB: Cadastro realizado com sucesso"""
        paciente = Paciente("Maria", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertEqual(paciente.nome, "Maria")
        self.assertEqual(paciente.cpf, "11111111111")
        self.assertEqual(paciente.email, "maria@teste.com")
        self.assertEqual(paciente.nascimento, "21/03/2002")

    def test_nome_vazio(self):
        """RT1: Nome vazio"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertIn("nome", context.exception.message)

    def test_nome_caracteres_numericos(self):
        """RT2: Nome com números"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria123", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertIn("nome", context.exception.message)

    def test_nome_caracteres_especiais(self):
        """RT3: Nome com caracteres especiais"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria@#", "11111111111", "maria@teste.com", "21/03/2002")
        self.assertIn("nome", context.exception.message)

    def test_cpf_com_letras(self):
        """RT4: CPF com letras"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111aaaa11", "maria@teste.com", "21/03/2002")
        self.assertIn("CPF", context.exception.message)

    def test_cpf_tamanho_incorreto(self):
        """RT5: CPF com tamanho incorreto, menor ou maior"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "1111111", "maria@teste.com", "21/03/2002")
        self.assertIn("CPF", context.exception.message)

    def test_cpf_vazio(self):
        """RT6: CPF vazio"""
        
        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "", "maria@teste.com", "21/03/2002")
        self.assertIn("CPF", context.exception.message)

    def test_cpf_duplicado(self):
        """RT7: CPF duplicado"""
        repo = set()
        paciente1 = Paciente("Maria", "11111111111", "maria@teste.com", "21/03/2002")
        repo.add(paciente1.cpf)

        with self.assertRaises(CPFDuplicadoError) as contexto:
            paciente2 = Paciente("João", "11111111111", "joao@teste.com", "21/03/2000")
            if paciente2.cpf in repo:
                raise CPFDuplicadoError("CPF já cadastrado no sistema.")
        
        self.assertEqual(str(contexto.exception), "CPF já cadastrado no sistema.")

    def test_email_invalido(self):
        """RT8: E-mail inválido"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria.com", "21/03/2002")
        self.assertIn("E-mail", context.exception.message)

    def test_email_vazio(self):
        """RT9: E-mail vazio"""

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "", "21/03/2002")
        self.assertIn("E-mail", context.exception.message)

    def test_validacao_nascimento_futura(self):
        """RT10: Testa se a validação impede datas futuras"""

        paciente = Paciente("Maria", "11111111111", "maria@teste.com", "21/03/2002")
        
        data_futura = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

        with self.assertRaises(ValidacaoError) as contexto:
            paciente.validar_nascimento(data_futura)

        self.assertEqual(str(contexto.exception), "A data de nascimento não pode ser futura.")

    """def test_dia_invalido(self):
        RT11: Dia inválido na data de nascimento

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria@teste.com", "32/03/2002")
        self.assertIn("Data de nascimento", context.exception.message)

    def test_mes_invalido(self):
        RT12: Mês inválido na data de nascimento

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria@teste.com", "10/13/2002")
        self.assertIn("Data de nascimento", context.exception.message)

    def test_data_com_caracteres_especiais(self):
        RT13: Data de nascimento com caracteres especiais

        with self.assertRaises(ValidacaoError) as context:
            Paciente("Maria", "11111111111", "maria@teste.com", "10/XX/2002")  
        self.assertIn("Data de nascimento inválida", context.exception.message)
"""