let DADOS_MATERIAIS = {};
    let meuGrafico = null;
    let propriedadeAtual = 'G';

    window.onload = async function() {
        try {
            const resposta = await fetch('./materiais_db.json');
            DADOS_MATERIAIS = await resposta.json();
            const seletor = document.getElementById('seletorMaterial');
            seletor.innerHTML = '<option value="">Selecione o Elemento...</option>';
            Object.keys(DADOS_MATERIAIS).sort().forEach(mat => {
                const opt = document.createElement('option');
                opt.value = mat; opt.text = mat;
                seletor.appendChild(opt);
            });
        } catch (e) { alert("Erro ao carregar banco de dados JSON."); }
    };

    function setProp(prop, btn) {
        propriedadeAtual = prop;
        document.querySelectorAll('.prop-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        plotarGrafico();
    }

    function aoMudarMaterial() {
        const mat = document.getElementById('seletorMaterial').value;
        if (!mat) return;
        const fases = DADOS_MATERIAIS[mat].fases;
        const container = document.getElementById('listaFases');
        container.innerHTML = "";
        Object.keys(fases).forEach(nome => {
            container.innerHTML += `<div class="fase-badge">
                <input type="checkbox" id="chk_${nome}" value="${nome}" checked onchange="plotarGrafico()">
                <label for="chk_${nome}">${nome}</label>
            </div>`;
        });
        gerarTabela(fases);
        plotarGrafico();
    }

   function gerarTabela(fases) {
    // Definimos o cabeçalho completo
    const cabecalho = ["Fase", "T Min", "T Max", "A", "B", "C", "D", "E", "F", "G"];
    
    let html = `<table><thead><tr>`;
    cabecalho.forEach(h => html += `<th>${h}</th>`);
    html += `</tr></thead><tbody>`;

    for (let f in fases) {
        const faseData = fases[f];
        const c = faseData.coefs;
        
        html += `<tr>`;
        html += `<td>${f}</td>`;
        html += `<td style="color: #2980b9; font-weight: bold;">${faseData.t_min}</td>`;
        html += `<td style="color: #c0392b; font-weight: bold;">${faseData.t_max}</td>`;
        
        // Itera pelos coeficientes de A a G
        ["A", "B", "C", "D", "E", "F", "G"].forEach(p => {
            const val = c[p] || 0;
            html += `<td>${val.toFixed(2)}</td>`;
        });
        
        html += `</tr>`;
    }
    
    document.getElementById('tabelaDados').innerHTML = html + `</tbody></table>`;
}

    // MOTOR MATEMÁTICO CORRIGIDO (NIST Standard)
    function calcularShomate(T, coefs) {
        const t = T / 1000.0;
        const {A, B, C, D, E, F, G} = coefs;
        
        // Cp em J/mol·K
        const Cp = A + B*t + C*Math.pow(t,2) + D*Math.pow(t,3) + E/Math.pow(t,2);
        
        // H em kJ/mol (Fator F já ajusta para kJ no NIST)
        const H_kj = (A*t + B*Math.pow(t,2)/2 + C*Math.pow(t,3)/3 + D*Math.pow(t,4)/4 - E/t + F);
        
        // S em J/mol·K
        const S_j = (A*Math.log(t) + B*t + C*Math.pow(t,2)/2 + D*Math.pow(t,3)/3 - E/(2*Math.pow(t,2)) + G);
        
        // G em kJ/mol (CORREÇÃO DE UNIDADE: S/1000 para alinhar com H em kJ)
        const G_kj = H_kj - (T * (S_j / 1000.0));

        return { G: G_kj, H: H_kj, S: S_j, Cp: Cp };
    }

    function plotarGrafico() {
    const mat = document.getElementById('seletorMaterial').value;
    if (!mat) return;
    const checks = document.querySelectorAll('#listaFases input:checked');
    const datasets = [];

    checks.forEach(cb => {
        const nomeFase = cb.value;
        const f = DADOS_MATERIAIS[mat].fases[nomeFase];
        const pontos = [];
        for (let T = f.t_min; T <= f.t_max; T += 5) {
            const res = calcularShomate(T, f.coefs);
            pontos.push({ x: T, y: res[propriedadeAtual] });
        }

        const estilo = getFaseStyle(nomeFase);

        datasets.push({
            label: nomeFase,
            data: pontos,
            borderColor: estilo.color,
            borderDash: estilo.dash,
            borderWidth: 2,
            pointRadius: 0,
            hoverRadius: 8, // O ponto aparece ao passar o mouse
            pointStyle: 'circle',
            tension: 0.1
        });
    });

    if (meuGrafico) meuGrafico.destroy();
    const ctx = document.getElementById('mainChart').getContext('2d');
    
    meuGrafico = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'nearest', intersect: false }, // Facilita selecionar a linha
            plugins: {
                title: { display: true, text: `${propriedadeAtual} vs T - ${mat}` },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)} ${propriedadeAtual}`
                    }
                },
                legend: {
                    onHover: (e, legendItem) => {
                        const index = legendItem.datasetIndex;
                        meuGrafico.data.datasets.forEach((ds, i) => {
                            ds.borderColor = i === index ? getFaseStyle(ds.label).color : 'rgba(200, 200, 200, 0.15)';
                        });
                        meuGrafico.update('none');
                    },
                    onLeave: () => {
                        meuGrafico.data.datasets.forEach((ds) => {
                            ds.borderColor = getFaseStyle(ds.label).color;
                        });
                        meuGrafico.update('none');
                    }
                }
            },
            scales: {
                x: { type: 'linear', title: { display: true, text: 'Temperatura (K)' } },
                y: { title: { display: true, text: propriedadeAtual } }
            }
        }
    });
}

    function getFaseStyle(fase) {
    const f = fase.toLowerCase();
    const match = f.match(/\d+/);
    const num = match ? parseInt(match[0]) : 1;

    // Cores fixas para estados universais
    if (f.includes('liquid')) return { color: '#3498db', dash: [] }; 
    if (f.includes('gas')) return { color: '#e67e22', dash: [] };

    // Paleta profissional para múltiplos sólidos
    const coresSolidos = ['#2c3e50', '#e74c3c', '#16a085', '#8e44ad', '#f39c12'];
    const estilosDash = [[], [5, 5], [2, 2], [10, 5], [5, 2, 2, 2]];

    return {
        color: coresSolidos[num - 1] || `hsl(210, 30%, ${20 + (num * 5)}%)`,
        dash: estilosDash[num - 1] || []
    };
}