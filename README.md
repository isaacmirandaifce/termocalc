# TermoCalc | Dashboard de Termodinâmica dos Materiais

O **TermoCalc** é uma ferramenta interativa de visualização e cálculo de propriedades termodinâmicas de substâncias puras (metais e cerâmicos), desenvolvida para fins didáticos na disciplina de **Termodinâmica dos Materiais**.

A aplicação permite visualizar como a Entalpia ($H$), Entropia ($S$), Energia Livre de Gibbs ($G$) e Capacidade Calorífica ($C_p$) variam com a temperatura, utilizando os coeficientes oficiais do **NIST (National Institute of Standards and Technology)**.


---

##  Funcionalidades

* **Seleção de Materiais:** Banco de dados integrado com diversos elementos (Al, Fe, Cu, Ti, W, Ni, SiC, etc.).
* **Cálculo Multfásico:** Visualização simultânea de diferentes fases (Sólido I, II, Líquido, etc.) para identificar pontos de transição.
* **Gráficos Interativos:** Plotagem em tempo real utilizando a biblioteca Chart.js.
* **Parâmetros Técnicos:** Exibição dos coeficientes da Equação de Shomate para cada fase selecionada.

##  Fundamentação Teórica

O "motor" matemático do projeto baseia-se na **Equação de Shomate**, utilizada pelo NIST para descrever as propriedades termodinâmicas em função da temperatura.

Seja $t = T / 1000$ (onde $T$ é a temperatura em Kelvin), as propriedades são calculadas da seguinte forma:

### 1. Capacidade Calorífica ($J/mol \cdot K$)
$$C_p = A + B \cdot t + C \cdot t^2 + D \cdot t^3 + \frac{E}{t^2}$$

### 2. Entalpia ($kJ/mol$)
$$H^\circ - H^\circ_{298} = A \cdot t + \frac{B \cdot t^2}{2} + \frac{C \cdot t^3}{3} + \frac{D \cdot t^4}{4} - \frac{E}{t} + F$$

### 3. Entropia ($J/mol \cdot K$)
$$S^\circ = A \cdot \ln(t) + B \cdot t + \frac{C \cdot t^2}{2} + \frac{D \cdot t^3}{3} - \frac{E}{2t^2} + G$$

### 4. Energia Livre de Gibbs ($kJ/mol$)
Calculada através da relação fundamental:
$$G = H - T \cdot S$$

---

##  Tecnologias Utilizadas

* **HTML5/CSS3:** Estrutura e estilização com layout responsivo (Grid e Flexbox).
* **JavaScript (ES6+):** Lógica de cálculo, manipulação de DOM e processamento de dados JSON.
* **Chart.js:** Biblioteca para renderização dos gráficos de alta performance.
* **JSON:** Armazenamento dos coeficientes termodinâmicos.

##  Estrutura do Repositório

* `index.html`: Interface principal.
* `style.css`: Estilização visual e definições de layout.
* `scripts.js`: Motor de cálculo termodinâmico e lógica do gráfico.
* `materiais_db.json`: Banco de dados contendo os coeficientes NIST para cada material.

---

##  Como usar

1.  Clone o repositório ou baixe os arquivos.
2.  Abra o arquivo `index.html` em qualquer navegador moderno.
3.  Selecione um material no menu lateral.
4.  Escolha a propriedade ($G, H, S, C_p$) que deseja analisar.
5.  Clique em **PLOTAR** para atualizar o gráfico.

---

**Nota:** Este projeto possui caráter estritamente educativo. Para aplicações de engenharia e projetos reais, recomenda-se consultar diretamente o [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry/).
