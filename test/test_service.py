import unittest
from typing import List
from main.domain import *
from main.repository import PacienteRepository, AtendimentoRepository
from main.service import ProntoSocorroService


# Os testes abaixo cobrem RF2: Realizar Triagem
class TestProntoSocorroService(unittest.TestCase):
    def setUp(self):
        """Inicialização dos testes"""
        self.paciente_repo = PacienteRepository()
        self.atendimento_repo = AtendimentoRepository(self.paciente_repo)
        self.ps_service = ProntoSocorroService(self.paciente_repo, self.atendimento_repo)
        self.fila = FilaAtendimento()

    def test_rtb_risco_azul(self):
        """RTB: Paciente sem critério de gravidade"""

        ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=False)
        self.assertEqual(self.ps_service.classificar_risco(ficha), Risco.AZUL)

    def test_rt1_risco_verde(self):
        """RT1: Paciente com gravidade baixa"""

        ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=True)
        self.assertEqual(self.ps_service.classificar_risco(ficha), Risco.VERDE)

    def test_rt2_risco_laranja(self):
        """RT2: Paciente com gravidade moderada"""

        ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=True, gravidade_baixa=False)
        self.assertEqual(self.ps_service.classificar_risco(ficha), Risco.LARANJA)

    def test_rt3_risco_amarelo(self):
        """RT3: Paciente com gravidade alta"""

        ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
        self.assertEqual(self.ps_service.classificar_risco(ficha), Risco.AMARELO)

    def test_rt4_risco_vermelho(self):
        """RT4: Paciente com risco de morte"""
        ficha = FichaAnalise(risco_morte=True, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=False)
        self.assertEqual(self.ps_service.classificar_risco(ficha), Risco.VERMELHO)

    

    # Os testes abaixo cobrem o RF3: Gerenciar Fila de Atendimento 
    def test_rtb_g1_h3_maior_risco_primeiro(self):
        """RTB: Paciente com maior risco deve ser atendido primeiro"""
        paciente1 = self.ps_service.registrar_paciente("Carlos", "11111111111", "carlos@teste.com", "10/01/1980")
        paciente2 = self.ps_service.registrar_paciente("Bruna", "22222222222", "bruna@teste.com", "23/09/1995")

        atendimento1 = self.ps_service.registrar_atendimento(paciente1, Risco.AMARELO)
        atendimento2 = self.ps_service.registrar_atendimento(paciente2, Risco.VERMELHO)

        self.ps_service.inserir_fila_atendimento(atendimento1)
        self.ps_service.inserir_fila_atendimento(atendimento2)

        proximo = self.ps_service.chamar_proximo()
        self.assertEqual(proximo, atendimento2)  

    """def test_rt1_g2_h4_mesmo_risco_ordem_chegada(self):
        RT1: Se os pacientes tiverem o mesmo risco, o primeiro a chegar deve ser chamado primeiro
        paciente1 = Paciente("Diego", "55555555555", "diego@teste.com", "20/03/1985")
        paciente2 = Paciente("Fernanda", "66666666666", "fernanda@teste.com", "11/07/1990")

        atendimento1 = Atendimento(paciente1, Risco.AMARELO)
        atendimento2 = Atendimento(paciente2, Risco.AMARELO)

        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)

        proximo = self.fila.proximo()
        self.assertEqual(proximo, atendimento1)  
    """

    def test_rt2_g3_h3_fila_mantem_ordem_apos_remocao(self):
        """RT2: Após remoção, a fila continua na ordem correta"""

        paciente1 = self.ps_service.registrar_paciente("Lucas", "55555555555", "lucas@teste.com", "15/08/1993")
        paciente2 = self.ps_service.registrar_paciente("Fernanda", "66666666666", "fernanda@teste.com", "02/11/1990")
        paciente3 = self.ps_service.registrar_paciente("Miguel", "77777777777", "miguel@teste.com", "30/07/2000")

        atendimento1 = self.ps_service.registrar_atendimento(paciente1, Risco.VERMELHO)
        atendimento2 = self.ps_service.registrar_atendimento(paciente2, Risco.AMARELO)
        atendimento3 = self.ps_service.registrar_atendimento(paciente3, Risco.VERDE)

        self.ps_service.inserir_fila_atendimento(atendimento1)
        self.ps_service.inserir_fila_atendimento(atendimento2)
        self.ps_service.inserir_fila_atendimento(atendimento3)

        self.ps_service.chamar_proximo()  
        proximo = self.ps_service.chamar_proximo()
        self.assertEqual(proximo, atendimento2)  

    def test_rt3_g1_h1_fila_vazia(self):
        """RT3: Tentar chamar um paciente com uma fila vazia"""

        with self.assertRaises(Exception) as context:
            self.ps_service.chamar_proximo()
        self.assertIn("fila de atendimento", str(context.exception))

    def test_rt4_g1_h2_um_paciente_na_fila(self):
        """RT4: Com um único paciente na fila, ele deve ser chamado corretamente"""
        paciente = self.ps_service.registrar_paciente("Eduardo", "88888888888", "eduardo@teste.com", "11/03/1985")
        atendimento = self.ps_service.registrar_atendimento(paciente, Risco.VERDE)

        self.ps_service.inserir_fila_atendimento(atendimento)

        proximo = self.ps_service.chamar_proximo()
        self.assertEqual(proximo, atendimento)

    """def test_rt5_g1_h4_multiplos_pacientes_riscos_iguais(self):
        RT5: Com múltiplos pacientes na fila com o mesmo risco, o primeiro a chegar deve ser chamado primeiro
        paciente1 = self.ps_service.registrar_paciente("Amanda", "99999999999", "amanda@teste.com", "05/07/1982")
        atendimento1 = self.ps_service.registrar_atendimento(paciente1, Risco.AZUL)
        self.ps_service.inserir_fila_atendimento(atendimento1)  # Insere primeiro paciente
        
        paciente2 = self.ps_service.registrar_paciente("Roberto", "10101010101", "roberto@teste.com", "29/12/1978")
        atendimento2 = self.ps_service.registrar_atendimento(paciente2, Risco.AZUL)
        self.ps_service.inserir_fila_atendimento(atendimento2)  # Insere segundo paciente

        proximo = self.ps_service.chamar_proximo()
        self.assertEqual(proximo, atendimento1)  # Paciente inserido primeiro deve ser chamado primeiro
    """






    # Os testes abaixo cobrem RF4: Chamar Próximo da Fila
    def test_rtb_i3_j1_multiplo_pacientes_removido_corretamente(self):
        """RTB: Múltiplos pacientes na fila, o de maior prioridade deve ser chamado primeiro"""

        paciente1 = Paciente("Alice", "11111111111", "alice@teste.com", "10/02/1990")  
        paciente2 = Paciente("Bruno", "22222222222", "bruno@teste.com", "15/03/1985") 
        paciente3 = Paciente("Carlos", "33333333333", "carlos@teste.com", "22/07/1995")  

        atendimento1 = Atendimento(paciente1, Risco.VERMELHO)  
        atendimento2 = Atendimento(paciente2, Risco.AMARELO)  
        atendimento3 = Atendimento(paciente3, Risco.VERDE)  

        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)
        self.fila.inserir(atendimento3)

        proximo = self.fila.proximo()
        self.assertEqual(proximo, atendimento1)  
        self.assertEqual(self.fila.tamanho(), 2) 

        
    """def test_rt1_i1_j1_fila_vazia(self):
        RT1: Tentativa de remover paciente com fila vazia
        with self.assertRaises(FilaVaziaError) as context:
            self.fila.proximo()
        self.assertIn("fila de atendimento", str(context.exception))
    """

    
    """def test_rt3_i3_j2_fila_mantem_ordem_apos_remocao(self):
        RT3: Após remoção, a fila mantém a ordem correta
        paciente1 = Paciente("Eduardo", "55555555555", "eduardo@teste.com", "05/06/1988")  
        paciente2 = Paciente("Fernanda", "66666666666", "fernanda@teste.com", "30/08/1993") 
        paciente3 = Paciente("Gabriel", "77777777777", "gabriel@teste.com", "12/12/1980")  

        atendimento1 = Atendimento(paciente1, Risco.VERMELHO)
        atendimento2 = Atendimento(paciente2, Risco.AMARELO)
        atendimento3 = Atendimento(paciente3, Risco.VERDE)

        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)
        self.fila.inserir(atendimento3)

        self.fila.proximo() 
        proximo = self.fila.proximo()
        self.assertEqual(proximo, atendimento2)  
        self.assertEqual(self.fila.tamanho(), 1)  
        """
    """def test_rt4_i3_j3_paciente_mesmo_risco(self):
        RT4: Remover paciente com risco igual aos outros
        paciente1 = Paciente("Hugo", "88888888888", "hugo@teste.com", "11/11/1975")
        paciente2 = Paciente("Isabela", "99999999999", "isabela@teste.com", "01/01/1990")

        atendimento1 = Atendimento(paciente1, Risco.AMARELO)
        atendimento2 = Atendimento(paciente2, Risco.AMARELO)  

        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)

        proximo = self.fila.proximo()
        self.assertEqual(proximo, atendimento1) 
        self.assertEqual(self.fila.tamanho(), 1)  
        proximo = self.fila.proximo()
        self.assertEqual(proximo, atendimento2) 
        self.assertEqual(self.fila.tamanho(), 0)  
"""