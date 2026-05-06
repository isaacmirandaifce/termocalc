import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ==========================================
# 1. Parâmetros e Dados (Apêndices)
# ==========================================
T0 = 298.15
S298_alpha = 30.7  # J/mol.K

# Coeficientes Cp (Ti-alpha): Cp = a + bT + c/T^2 + dT^2
# Nota: Para simplificação didática, usaremos os mesmos coeficientes para as fases 
# subsequentes, ajustando G e S nas transições conforme os dados de transição.
a, b, c, d = 24.94, 6.57e-3, -1.63e5, 1.34e-6

# Dados de Transição
T_trans_ab = 1155.0    # alpha -> beta (K)
dH_trans_ab = 4200.0   # J/mol
T_trans_bl = 1943.0    # beta -> liquid (K)
dH_trans_bl = 16700.0  # J/mol

# ==========================================
# 2. Funções de Integração Analítica
# ==========================================

def calc_S(T, S_ref, T_ref):
    """Calcula a entropia S(T) integrando Cp/T"""
    term_a = a * np.log(T / T_ref)
    term_b = b * (T - T_ref)
    term_c = -0.5 * c * (T**-2 - T_ref**-2)
    term_d = 0.5 * d * (T**2 - T_ref**2)
    return S_ref + term_a + term_b + term_c + term_d

def calc_G(T, G_ref, S_ref, T_ref):
    """Calcula G(T) integrando -S(T) dT"""
    dt = T - T_ref
    term_S0 = -S_ref * dt
    term_a = -a * (T * np.log(T / T_ref) - dt)
    term_b = -0.5 * b * dt**2
    term_c = (c / 2) * (-(1/T) + (1/T_ref) - (dt / T_ref**2))
    term_d = -(d / 2) * ((T**3 / 3) - (T_ref**2 * T) + (2 * T_ref**3 / 3))
    return G_ref + term_S0 + term_a + term_b + term_c + term_d

# ==========================================
# 3. Processamento das Fases
# ==========================================
# Fase Alpha (298.15 - 1155 K)
T_alpha = np.linspace(T0, T_trans_ab, 100)
S_alpha = calc_S(T_alpha, S298_alpha, T0)
G_alpha = calc_G(T_alpha, 0, S298_alpha, T0)

# Transição Alpha -> Beta
S_at_1155_alpha = calc_S(T_trans_ab, S298_alpha, T0)
G_at_1155_alpha = calc_G(T_trans_ab, 0, S298_alpha, T0)

S_start_beta = S_at_1155_alpha + (dH_trans_ab / T_trans_ab)
G_start_beta = G_at_1155_alpha # G é contínuo na transição

# Fase Beta (1155 - 1943 K)
T_beta = np.linspace(T_trans_ab, T_trans_bl, 100)
S_beta = calc_S(T_beta, S_start_beta, T_trans_ab)
G_beta = calc_G(T_beta, G_start_beta, S_start_beta, T_trans_ab)

# Transição Beta -> Líquido
S_at_1943_beta = calc_S(T_trans_bl, S_start_beta, T_trans_ab)
G_at_1943_beta = calc_G(T_trans_bl, G_start_beta, S_start_beta, T_trans_ab)

S_start_liq = S_at_1943_beta + (dH_trans_bl / T_trans_bl)
G_start_liq = G_at_1943_beta

# Fase Líquida (1943 - 2500 K)
T_liq = np.linspace(T_trans_bl, 2500, 100)
G_liq = calc_G(T_liq, G_start_liq, S_start_liq, T_trans_bl)

# ==========================================
# 4. Plotagem e Memória de Cálculo
# ==========================================
fig = plt.figure(figsize=(16, 8))
gs = GridSpec(1, 2, width_ratios=[1, 1.5])

# Painel Lateral (LaTeX)
ax_txt = fig.add_subplot(gs[0])
ax_txt.axis('off')
memoria = (
    r"$\bf{MEMÓRIA\ DE\ CÁLCULO\ (Ti)}$" + "\n\n"
    r"$\bf{1.\ Capacidade\ Calorífica:}$" + "\n"
    r"$C_p = a + bT + cT^{-2} + dT^2$" + "\n\n"
    
    r"$\bf{2.\ Entropia\ Absoluta:}$" + "\n"
    r"$S(T) = S_{298} + \int_{298}^{T} \frac{C_p}{T'} dT'$" + "\n"
    r"$S(T) = S_{298} + a \ln\left(\frac{T}{298}\right) + b(T - 298) - \frac{c}{2}\left(\frac{1}{T^2} - \frac{1}{298^2}\right) + \frac{d}{2}(T^2 - 298^2)$" + "\n\n"
    
    r"$\bf{3.\ Energia\ de\ Gibbs:}$" + "\n"
    r"$G(T) = G_{ref} - \int_{T_{ref}}^{T} S(T') dT'$" + "\n\n"
    r"$\Delta G = G(T) - G(298) = \int_{298}^{T} -S(T)\, dT$" + "\n\n"
    r"$\Delta G = -S_{298}(T - 298)- a\left[T \ln\left(\frac{T}{298}\right) - (T - 298)\right]- \frac{b}{2}(T - 298)^2+ \frac{c}{2}\left[-\frac{1}{T} + \frac{1}{298} - \frac{T - 298}{298^2}\right]- \frac{d}{2}\left[\frac{T^3}{3} - 298^2 T + \frac{2}{3} \cdot 298^3\right]$" + "\n\n"
    
    r"$\bf{4.\ Transições\ de\ Fase:}$" + "\n"
    r"$\alpha \to \beta: 1155\ K, \Delta H = 4.2\ kJ/mol$" + "\n"
    r"$\beta \to Liq: 1943\ K, \Delta H = 16.7\ kJ/mol$" + "\n"
    r"$\Delta S_{trans} = \frac{\Delta H_{trans}}{T_{trans}}$" + "\n"

    r"$G_{\alpha}(T_{trans}) = " + f"{G_at_1155_alpha/1000: .3f}" + "  kJ/mol$\n\n"
    r"$G_{\beta}(T_{trans}) = " + f"{G_at_1155_alpha/1000: .3f}" + "  kJ/mol$\n\n"
    r"$G_{\beta}(T_{trans}) = G_{\alpha}(T_{trans})$" + "\n\n"

    r"$\bf{Dados\ Ti\ (\alpha):}$" + "\n"
    fr"$a={a}, b={b}, c={c}, d={d}$"
)
ax_txt.text(0.05, 0.95, memoria, transform=ax_txt.transAxes, fontsize=11, va='top', family='serif')

# Gráfico G x T
ax_plot = fig.add_subplot(gs[1])
ax_plot.plot(T_alpha, G_alpha/1000, 'b-', label='Ti-hex (alpha)', linewidth=2)
ax_plot.plot(T_beta, G_beta/1000, 'g-', label='Ti-bcc (beta)', linewidth=2)
ax_plot.plot(T_liq, G_liq/1000, 'r-', label='Ti-Líquido', linewidth=2)

# Marcações de Transição
ax_plot.axvline(T_trans_ab, color='k', linestyle='--', alpha=0.3)
ax_plot.axvline(T_trans_bl, color='k', linestyle='--', alpha=0.3)

ax_plot.set_title('Energia Livre de Gibbs Molar do Titânio', fontsize=14)
ax_plot.set_xlabel('Temperatura (K)')
ax_plot.set_ylabel('G - G(298) (kJ/mol)')
ax_plot.legend()
ax_plot.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()