import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class FaseTitanio:
    def __init__(self, nome, t_ref, g_ref, s_ref, cp_coeffs):
        self.nome = nome
        self.t_ref = t_ref
        self.g_ref = g_ref
        self.s_ref = s_ref
        self.a = cp_coeffs['a']
        self.b = cp_coeffs['b']
        self.c = cp_coeffs['c']
        self.d = cp_coeffs['d']

    def calcular_entropia_absoluta(self, T):
        T0 = self.t_ref
        return self.s_ref + (self.a * np.log(T/T0) + self.b * (T - T0) - 
                             (self.c / 2) * (1/T**2 - 1/T0**2) + (self.d / 2) * (T**2 - T0**2))

    def calcular_deHoff(self, T):
        T = np.where(T <= 0, 1e-9, T)
        T0 = self.t_ref
        t1 = -self.s_ref * (T - T0)
        t2 = -self.a * (T * np.log(T / T0) - (T - T0))
        t3 = -(self.b / 2) * (T - T0)**2
        t4 = (self.c / 2) * (-1/T + 1/T0 - (T - T0) / (T0**2))
        t5 = -(self.d / 2) * ((T**3 / 3) - (T0**2 * T) + (2 * T0**3 / 3))
        return self.g_ref + (t1 + t2 + t3 + t4 + t5)

def simular_com_memoria_calculo():
    # 1. Parâmetros Base
    cp = {'a': 24.94, 'b': 6.57e-3, 'c': -1.63e5, 'd': 1.34e-6}
    T_room, S_alfa_298 = 298.15, 30.7
    T_beta, DH_beta = 1155, 3010  # Delta H em J/mol
    T_fusao, DH_fusao = 1943, 14150

    # 2. Instanciação e Cálculos de Continuidade
    alfa = FaseTitanio("Alfa", T_room, 0, S_alfa_298, cp)
    
    G_at_1155_alfa = alfa.calcular_deHoff(T_beta)
    S_at_1155_alfa = alfa.calcular_entropia_absoluta(T_beta)
    beta = FaseTitanio("Beta", T_beta, G_at_1155_alfa, S_at_1155_alfa + (DH_beta/T_beta), cp)
    
    G_at_1943_beta = beta.calcular_deHoff(T_fusao)
    S_at_1943_beta = beta.calcular_entropia_absoluta(T_fusao)
    liquido = FaseTitanio("Líquido", T_fusao, G_at_1943_beta, S_at_1943_beta + (DH_fusao/T_fusao), cp)

    # 3. Preparação do Layout (Dashboard)
    fig = plt.figure(figsize=(18, 10))
    gs = GridSpec(2, 2, width_ratios=[1, 1.2], height_ratios=[1, 0.3])
    
    # --- Painel de Memória de Cálculo (Lado Esquerdo, ocupa as duas linhas) ---
    ax_txt = fig.add_subplot(gs[:, 0])
    ax_txt.axis('off')
    
    memoria = (
        r"$\bf{MEMÓRIA\ DE\ CÁLCULO\ (Ti)}$" + "\n\n"
        r"$\bf{1.\ Capacidade\ Térmica:}$" + "\n"
        r"$C_p = a + bT + cT^{-2} + dT^2$" + "\n\n"
        r"$\bf{2.\ Entropia\ Absoluta\ (Eq.\ 7.8):}$" + "\n"
        r"$S(T) = S_{298} + \int_{298}^{T} \frac{C_p}{T'} dT'$" + "\n\n"
        r"$\bf{3.\ Energia\ de\ Gibbs\ (Eq.\ 7.11):}$" + "\n"
        r"$G(T) = G_{ref} - \int_{T_{ref}}^{T} S(T') dT'$" + "\n\n"
        r"$\Delta G = -S_{298}(T - 298)- a\left[T \ln\left(\frac{T}{298}\right) - (T - 298)\right]- \frac{b}{2}(T - 298)^2+ $" + "\n\n"
        r"$\frac{c}{2}\left[-\frac{1}{T} + \frac{1}{298} - \frac{T - 298}{298^2}\right]- \frac{d}{2}\left[\frac{T^3}{3} - 298^2 T + \frac{2}{3} \cdot 298^3\right]$" + "\n\n"
        r"$\bf{4.\ Transições\ de\ Fase\ (Eq.\ 7.10\ e\ 7.12):}$" + "\n"
        r"$\alpha \to \beta: 1155\ K$" + "\n"
        r"$\beta \to Liq: 1943\ K$" + "\n\n"
        f"Em equilíbrio ($T = 1155$ K):\n"
        r"$G_{\alpha} = G_{\beta} = " + f"{G_at_1155_alfa/1000:.3f}" + r"\ kJ/mol$" + "\n"
        f"Em fusão ($T = 1943$ K):\n"
        r"$G_{\beta} = G_{Liq} = " + f"{G_at_1943_beta/1000:.3f}" + r"\ kJ/mol$" + "\n\n"
        r"$\bf{Dados\ de\ Entrada\ (\alpha-Ti):}$" + "\n"
        fr"$a={cp['a']}, b={cp['b']}, c={cp['c']}, d={cp['d']}$"
    )
    ax_txt.text(0.05, 0.95, memoria, transform=ax_txt.transAxes, fontsize=11, va='top', family='serif')

    # --- Painel do Gráfico (Topo Direito) ---
    ax_plot = fig.add_subplot(gs[0, 1])
    T_range = np.linspace(250, 2400, 500)
    ax_plot.plot(T_range, alfa.calcular_deHoff(T_range)/1000, label='$G_{\\alpha}$', color='blue')
    ax_plot.plot(T_range, beta.calcular_deHoff(T_range)/1000, label='$G_{\\beta}$', color='green', linestyle='--')
    ax_plot.plot(T_range, liquido.calcular_deHoff(T_range)/1000, label='$G_{Liq}$', color='red', linestyle=':')
    ax_plot.set_ylabel("G (kJ/mol)")
    ax_plot.legend()
    ax_plot.grid(True, alpha=0.2)
    ax_plot.set_title("Energia livre de Gibbs vs Temperatura")
    ax_plot.axvline(x=1155, color='gray', linestyle='-', alpha=0.5)
    ax_plot.axvline(x=1943, color='gray', linestyle='-', alpha=0.5)
    ax_plot.text(1165, -100, '$\\alpha \\rightarrow \\beta$', fontsize=10)
    ax_plot.text(1953, -100, 'Fusão', fontsize=10)

    # --- Painel da Tabela (Base Direita) ---
    ax_tab = fig.add_subplot(gs[1, 1])
    ax_tab.axis('off')
    col_labels = ['Fase', 'Intervalo ', 'G inicial (kJ)', 'G final (kJ)']
    data = [
        ["Alfa (hcp)", "298 - 1155 K", "0.00", f"{G_at_1155_alfa/1000:.2f}"],
        ["Beta (bcc)", "1155 - 1943 K", f"{G_at_1155_alfa/1000:.2f}", f"{G_at_1943_beta/1000:.2f}"],
        ["Líquido", "1943 - 2400 K", f"{G_at_1943_beta/1000:.2f}", f"{liquido.calcular_deHoff(2400)/1000:.2f}"]
    ]
    tabela = ax_tab.table(cellText=data, colLabels=col_labels, loc='center', cellLoc='center')
    tabela.scale(1, 2)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simular_com_memoria_calculo()