import numpy as np
import matplotlib.pyplot as plt

class FaseShomate:
    def __init__(self, nome, t_min, t_max, coeffs):
        self.nome = nome
        self.t_min = t_min
        self.t_max = t_max
        self.A = coeffs['A']
        self.B = coeffs['B']
        self.C = coeffs['C']
        self.D = coeffs['D']
        self.E = coeffs['E']
        self.F = coeffs['F']
        self.G = coeffs['G']
        self.H_shomate = coeffs['H']
        self.offset_g = 0.0  # Constante de ajuste para continuidade

    def calcular_propriedades(self, T):
        t = T / 1000.0
        # H° - H°298.15 (kJ/mol) conforme NIST
        H_rel = (self.A*t + self.B*(t**2)/2 + self.C*(t**3)/3 + 
                 self.D*(t**4)/4 - self.E/t + self.F - self.H_shomate)
        
        # S° (J/mol*K) conforme NIST
        S = (self.A*np.log(t) + self.B*t + self.C*(t**2)/2 + 
             self.D*(t**3)/3 - self.E/(2*t**2) + self.G)
        
        # G = H - TS (convertendo S para kJ)
        G_puro = H_rel - (T / 1000.0) * S
        return G_puro + self.offset_g

    def ajustar_referencia(self, T_trans, G_alvo):
        """Ajusta o offset para que G(T_trans) == G_alvo"""
        G_atual = self.calcular_propriedades(T_trans)
        self.offset_g = G_alvo - G_atual

def plotar_nist_shomate_corrigido():
    # --- Dados NIST ---
    c_alfa1 = {'A': 22.61942, 'B': 18.98795, 'C': -18.18735, 'D': 7.080792, 'E': -0.143457, 'F': -7.922279, 'G': 52.40962, 'H': 0.0}
    c_alfa2 = {'A': 44.37174, 'B': -44.09225, 'C': 31.70602, 'D': 0.052209, 'E': 0.036168, 'F': -12.72011, 'G': 93.08772, 'H': 0.0}
    c_beta  = {'A': 23.05660, 'B': 5.541331, 'C': -2.055881, 'D': 1.611745, 'E': -0.056075, 'F': -0.433228, 'G': 64.12691, 'H': 6.860003}
    c_liq   = {'A': 47.23694, 'B': 1.975192e-8, 'C': -5.335145e-9, 'D': 4.904109e-10, 'E': 1.564855e-8, 'F': -22.05273, 'G': 66.20218, 'H': 13.65202}

    # Instâncias
    alfa1 = FaseShomate("Alfa Low", 298, 700, c_alfa1)
    alfa2 = FaseShomate("Alfa High", 700, 1700, c_alfa2)
    beta  = FaseShomate("Beta", 1155, 1941, c_beta)
    liq   = FaseShomate("Líquido", 1941, 3000, c_liq)

    # 1. Alfa 2 deve continuar de onde Alfa 1 parou (em 700K)
    alfa2.ajustar_referencia(700, alfa1.calcular_propriedades(700))
    
    # 2. Beta deve cruzar Alfa na temperatura de transição (1155K)
    # G_alfa(1155) == G_beta(1155)
    g_trans_1155 = alfa2.calcular_propriedades(1155)
    beta.ajustar_referencia(1155, g_trans_1155)
    
    # 3. Líquido deve cruzar Beta na temperatura de fusão (1941K)
    g_fusao_1941 = beta.calcular_propriedades(1941)
    liq.ajustar_referencia(1941, g_fusao_1941)

    # --- Plotagem ---
    T = np.linspace(298, 2500, 500)
    plt.figure(figsize=(11, 7))
    
    # Alfa composta
    G_alfa = np.where(T < 700, alfa1.calcular_propriedades(T), alfa2.calcular_propriedades(T))
    plt.plot(T, G_alfa, 'b-', label='Ti-Alfa (HCP)', lw=2)
    plt.plot(T, beta.calcular_propriedades(T), 'g--', label='Ti-Beta (BCC)')
    plt.plot(T, liq.calcular_propriedades(T), 'r:', label='Ti-Líquido')

    # Destacar Interseções
    plt.scatter([1155, 1941], [alfa2.calcular_propriedades(1155), beta.calcular_propriedades(1941)], 
                color='black', zorder=5, label='Pontos de Transição')

    plt.title("Energia Livre de Gibbs do Ti (NIST - Shomate)", fontsize=14)
    plt.xlabel("Temperatura (K)")
    plt.ylabel("G (kJ/mol)")
    plt.axvline(x=1155, color='gray', alpha=0.4, linestyle='--')
    plt.axvline(x=1941, color='orange', alpha=0.4, linestyle='--')
    plt.text(1165, -100, '$\\alpha \\rightarrow \\beta$', fontsize=10)
    plt.text(1165, -120, f"{g_trans_1155:.2f}", fontsize=10)
    plt.text(1953, -100, 'Fusão', fontsize=10)
    plt.text(1953, -120, f"{g_fusao_1941:.2f}", fontsize=10)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    print(g_trans_1155)
    print(g_fusao_1941)


if __name__ == "__main__":
    plotar_nist_shomate_corrigido()