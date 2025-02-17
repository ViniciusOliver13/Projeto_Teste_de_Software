import unittest
from main.domain import Paciente, Atendimento, Risco
from main.service import ProntoSocorroService
from main.repository import PacienteRepository, AtendimentoRepository
from main.error import PacienteNaoCadastradoError

class TestAtendimentoRepository(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para os testes"""
        self.paciente_repo = PacienteRepository()
        self.atendimento_repo = AtendimentoRepository(self.paciente_repo)
        self.ps_service = ProntoSocorroService(self.paciente_repo, self.atendimento_repo)

    def test_rtb_k2_paciente_sem_atendimentos(self):
        """RTB: Paciente cadastrado, mas sem atendimentos registrados"""

        paciente = self.ps_service.registrar_paciente("Carlos", "11111111111", "carlos@teste.com", "15/06/1990")
        
        historico = self.ps_service.buscar_historico(paciente)
        self.assertEqual(historico, [])  

    def test_rt1_k1_paciente_nao_cadastrado(self):
        """RT1: Tentar buscar o histórico de paciente não cadastrado"""

        with self.assertRaises(PacienteNaoCadastradoError) as context:
            self.ps_service.buscar_historico(Paciente("Ana", "22222222222", "ana@teste.com", "10/12/1985"))
        self.assertIn("Paciente não cadastrado", str(context.exception))

        with self.assertRaises(PacienteNaoCadastradoError) as context:
            atendimento = Atendimento(Paciente("Ana", "22222222222", "ana@teste.com", "10/12/1985"), Risco.VERDE)
            self.atendimento_repo.inserir(atendimento)
        self.assertIn("Paciente não cadastrado", str(context.exception))


    def test_rt2_k3_paciente_com_atendimentos(self):
        """RT2: Paciente cadastrado com atendimentos registrados"""

        paciente = self.ps_service.registrar_paciente("Fernanda", "33333333333", "fernanda@teste.com", "20/04/1987")
        
        atendimento1 = self.ps_service.registrar_atendimento(paciente, Risco.AMARELO)
        atendimento2 = self.ps_service.registrar_atendimento(paciente, Risco.VERDE)
        atendimento3 = self.ps_service.registrar_atendimento(paciente, Risco.AZUL)  

        historico = self.ps_service.buscar_historico(paciente)

        self.assertEqual(len(historico), 3)
        