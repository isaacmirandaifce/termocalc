### 1. Fundamentos 
Em sistemas unários (compostos por um único componente puro), o **potencial químico ($\mu$) é idêntico à energia livre de Gibbs molar ($G$)**. A variação desta propriedade com a temperatura ($T$) e a pressão ($P$) é regida pela equação fundamental:
$$d\mu = dG = -SdT + VdP$$.

Para fases condensadas (sólidos e líquidos), a dependência com a pressão ($VdP$) é frequentemente pequena em pressões moderadas, permitindo focar a análise na seção isobárica ($G \times T$), onde a inclinação da curva é dada por $-S$ e a curvatura por $-C_p/T$.



### 2. Algoritmo Matemático para o Cálculo de $G(T)$

O processo de cálculo segue um caminho de integração dupla a partir de um estado de referência (geralmente $T_0 = 298,15\text{ K}$ e $P = 1\text{ atm}$):

#### **Passo 1: Coleta de Dados Experimentais**
Para o Titânio, os dados necessários são extraídos dos apêndices:
*   **Entropia Padrão ($S_{298}$):** $30,7 \text{ J/mol}\cdot\text{K}$.
*   **Capacidade Calorífica ($C_p$):** Definida pela equação empírica $C_p(T) = a + bT + cT^{-2} + dT^2$.
    *   Constantes para o Ti: $a = 24,94$; $b = 6,57 \times 10^{-3}$; $c = -1,63 \times 10^5$; $d = 1,34 \times 10^{-6}$.

#### **Passo 2: Cálculo da Entropia Absoluta $S(T)$**
A entropia em qualquer temperatura é obtida integrando a relação $dS = (C_p/T)dT$:

$$S(T) = S_{298} + \int_{298}^{T} \frac{C_p(T)}{T} dT$$

Substituindo a expansão de $C_p$:

$$S(T) = S_{298} + \int_{298}^{T} \left( \frac{a}{T} + b + cT^{-3} + dT \right) dT$$

A integração resulta em:

$$S(T) = S_{298} + a \ln\left(\frac{T}{298}\right) + b(T - 298) - \frac{c}{2}\left(\frac{1}{T^2} - \frac{1}{298^2}\right) + \frac{d}{2}(T^2 - 298^2)$$

#### **Passo 3: Cálculo da Energia Livre de Gibbs $G(T)$**
A variação de $G$ (ou $\mu$) é a integral da entropia negativa:

$$G(T) - G(298) = \int_{298}^{T} -S(T) dT$$

Onde $G(298)$ é convencionado como o estado de referência (frequentemente definido como zero para a fase estável a 298 K). A integração desta função fornece a **superfície isobárica** da fase estudada.


### 3. Tratamento de Mudanças de Fase

O Titânio apresenta transformações alotrópicas que exigem a repetição do algoritmo para cada fase. A estratégia fundamental apresentada na **Equação 7.11** consiste em calcular a energia livre de uma fase de alta temperatura (como o líquido ou a fase $\beta$) partindo do ponto de equilíbrio com a fase anterior, em vez de tentar integrar todas as fases desde a referência de 298 K.

#### **Raciocínio da Estratégia**
Para calcular a energia do Titânio líquido ($G^L$) em uma temperatura $T$, o caminho matemático é dividido em dois segmentos conectados pela temperatura de fusão ($T_m$):
1.  **Segmento Sólido ($\alpha \rightarrow \beta$):** Calcula-se a energia livre da fase sólida até $T_m$.
2.  **Ponto de Conexão:** No equilíbrio ($T_m$), utiliza-se a identidade fundamental de que as energias livres são iguais: **$G^L(T_m) = G^\beta(T_m)$**.
3.  **Segmento Líquido (Equação 7.11):** A partir de $T_m$, a curva para o líquido é "estendida" usando suas propriedades intrínsecas ($C_p^L$ e $S^L$):
    $$G^L(T) - G^L(T_m) = \int_{T_m}^{T} -\left[ S^L(T_m) + \int_{T_m}^{T} \frac{C_p^L(T)}{T} dT \right] dT$$.

 O uso desta estratégia garante que a interseção das curvas no gráfico $G \times T$ ocorra exatamente nas temperaturas de transformação tabeladas.
*   **Entropia de Transição:** Para iniciar a nova integral, a entropia $S^L(T_m)$ é obtida somando a entropia da fase anterior à **entropia de fusão** ($\Delta S^{\beta \rightarrow L}$), conforme a Equação 7.12:
    $$S^L(T_m) = S_{298}^\alpha + \int_{298}^{T_m} \frac{C_p}{T} dT + \Delta S^{\beta \rightarrow L}$$.

#### **Aplicação aos Dados do Titânio**
*   **Transição $\alpha$ (hex) $\rightarrow$ $\beta$ (bcc):** Ocorre a **1155 K**. O valor de $G^\alpha(1155)$ torna-se o ponto de partida para a integral da fase $\beta$.
*   **Fusão $\beta \rightarrow$ Líquido (L):** Ocorre a **1943 K**. O valor de $G^\beta(1943)$ torna-se o ponto inicial para a integral da fase líquida via Equação 7.11.


### 4. Resumo das Integrações para Programação
Para plotar a curva final, deve-se:

1.  **Calcular $G^\alpha(T)$** de 298 K a 1155 K usando os coeficientes da fase sólida $\alpha$.
2.  **Calcular $G^\beta(T)$** de 1155 K a 1943 K, usando o valor de $G^\alpha(1155)$ como ponto de partida para a nova integral.
3.  **Calcular $G^L(T)$** acima de 1943 K, partindo de $G^\beta(1943)$.

A fase estável em qualquer temperatura será aquela que apresentar o **menor valor de $G$** (ou $\mu$).
