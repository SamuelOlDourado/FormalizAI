const txtRascunho = document.getElementById('txtRascunho');
const contadorChar = document.getElementById('contadorChar');

const btnMelhorar = document.getElementById('btnMelhorar');
const selContexto = document.getElementById('selContexto')
const selTom = document.getElementById('selTom')
const btnLimpar = document.getElementById('btnLimpar');
const btnCopiar = document.getElementById('btnCopiar');
const btnAlteracoes = document.getElementById('btnAlteracoes');

const txtResultado = document.getElementById('txtResultado');

const listaAlteracoes = document.getElementById('listaAlteracoes');
const itensAlteracoes = document.getElementById('itensAlteracoes');
const lblAlteracoes = document.getElementById('lblAlteracoes');


const API_URL = '/api/melhorar';

function validarFormulario() {

    const possuiTexto = txtRascunho.value.trim().length > 0;
    const contextoSelecionado = selContexto.value !== "";
    const tomSelecionado = selTom.value !== "";

    btnMelhorar.disabled = !(
        possuiTexto &&
        contextoSelecionado &&
        tomSelecionado
    );
}

txtRascunho.addEventListener('input', () => {

    const qtdCaracteres = txtRascunho.value.length;
    contadorChar.textContent = qtdCaracteres;

    validarFormulario();

    btnLimpar.classList.toggle('visivel', qtdCaracteres > 0);

    if (qtdCaracteres === 0) {
        txtResultado.value = '';
        btnAlteracoes.classList.remove('visivel');
        btnAlteracoes.classList.remove('aberto');
        listaAlteracoes.classList.remove('aberto');
    }

});

selContexto.addEventListener('change', validarFormulario);
selTom.addEventListener('change', validarFormulario);

btnLimpar.addEventListener('click', () => {

    txtRascunho.value = '';
    txtRascunho.dispatchEvent(new Event('input'));
    txtRascunho.focus();

});

btnCopiar.addEventListener('click', () => {

    if (!txtResultado.value) return;
    navigator.clipboard.writeText(txtResultado.value);
    btnCopiar.textContent = '✓';

    setTimeout(() => {btnCopiar.textContent = '⧉';}, 1200);

});

btnAlteracoes.addEventListener('click', () => {

    const aberto = listaAlteracoes.classList.toggle('aberto');

    btnAlteracoes.classList.toggle('aberto', aberto);

});

function mostrarErro(mensagem) {

    txtResultado.classList.add('erro');
    txtResultado.value = mensagem;

    btnAlteracoes.classList.remove('visivel');
    btnAlteracoes.classList.remove('aberto');
    listaAlteracoes.classList.remove('aberto');

}

async function chamarAPIMelhorar(contexto, tom, texto) {

    const resposta = await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ contexto, tom, texto })
    });

    if (!resposta.ok) {

        let detalhe = '';
        try {
            const erroJson = await resposta.json();
            detalhe = erroJson.erro || '';
        } catch (_) {
            
        }

        throw new Error(
            detalhe || `Erro ao chamar a API (status ${resposta.status})`
        );
    }
    return resposta.json(); 
}

btnMelhorar.addEventListener('click', async () => {

    const contexto = selContexto.value;
    const tom = selTom.value;
    const texto = txtRascunho.value.trim();

    btnMelhorar.disabled = true;
    selContexto.disabled = true;
    selTom.disabled = true;
    btnMelhorar.textContent = 'Gerando...';

    try {
        const dados = await chamarAPIMelhorar(contexto, tom, texto);
        txtResultado.classList.remove('erro');
        txtResultado.value = dados.texto ?? '';
        const lista = Array.isArray(dados.alteracoes) ? dados.alteracoes : [];

        itensAlteracoes.innerHTML = lista
            .map(item => `<li>${item}</li>`)
            .join('');

        lblAlteracoes.textContent = `Ver alterações feitas (${lista.length})`;
        btnAlteracoes.classList.toggle('visivel', lista.length > 0);

    }catch (erro) {
        console.error('Falha ao consumir a API:', erro);
        mostrarErro('Não foi possível gerar o texto agora. Tente novamente em instantes.');

    }finally {
        btnMelhorar.disabled = false;
        btnMelhorar.textContent = 'Melhorar';
        selContexto.disabled = false;
        selTom.disabled = false;
        validarFormulario();
    }
});