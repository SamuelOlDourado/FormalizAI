from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import os
import json
import re


load_dotenv() 


app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODELO = "llama-3.3-70b-versatile"

CONTEXTOS = {
    "email": (
        "um e-mail corporativo profissional. "
        "Organize a mensagem em parágrafos claros e objetivos. "
        "Utilize uma saudação adequada quando fizer sentido e um encerramento cordial quando apropriado. "
        "A comunicação deve transmitir profissionalismo, clareza e respeito, preservando todas as informações fornecidas pelo usuário."
    ),

    "linkedin": (
        "uma publicação para o LinkedIn. "
        "Escreva um texto envolvente e natural, adequado ao ambiente profissional da plataforma. "
        "Utilize parágrafos curtos para facilitar a leitura. "
        "Quando fizer sentido, finalize com uma chamada para interação, como uma pergunta ou convite para compartilhar experiências. "
        "Se apropriado ao conteúdo, inclua de uma a três hashtags relevantes ao final da publicação. "
        "Emojis podem ser utilizados com moderação quando contribuírem para a comunicação."
    ),

    "comunicado": (
        "um comunicado interno de empresa. "
        "A mensagem deve ser clara, objetiva e organizada, transmitindo informações de forma direta e profissional. "
        "Evite floreios, preserve todas as informações importantes e priorize uma leitura rápida e fácil compreensão."
    ),
}

TONS = {
    "formal": (
        "bem formal, com linguagem refinada, estrutura completa e alto nível "
        "de profissionalismo"
    ),

    "neutro": (
        "profissional, equilibrado e natural, sem excesso de formalidade "
        "ou informalidade"
    ),

    "assertivo": (
        "objetivo, direto e conciso. Elimine rodeios, frases desnecessárias "
        "e redundâncias, priorizando clareza e ação"
    ),

    "empatico": (
        "empático, acolhedor e respeitoso, demonstrando consideração pelo leitor"
    ),

    "amigavel": (
        "amigável, próximo e descontraído, mantendo o profissionalismo "
        "adequado ao contexto"
    ),
}


def montar_prompt_sistema(contexto_label: str, tom_label: str) -> str:
    return (
        f"""
Você é um assistente de escrita corporativa em português do Brasil.

Sua tarefa é reescrever a mensagem enviada pelo usuário adaptando-a para 
{contexto_label}, com tom {tom_label}.

Antes de reescrever, analise o contexto profissional da mensagem e identifique 
implicitamente o papel de quem está escrevendo e a relação entre os envolvidos.

Considere possíveis papéis como:
- Funcionário/colaborador: alguém se comunicando com superiores, RH ou colegas.
  Priorize profissionalismo, respeito, clareza e evite que pedidos ou opiniões pareçam exigências.
  
- Líder/gestor/supervisor: alguém orientando, cobrando ou comunicando decisões.
  Mantenha autoridade e objetividade, mas evite tom agressivo, frio ou autoritário.

- RH/Recursos Humanos: comunicação institucional da empresa.
  Utilize linguagem neutra, acolhedora, profissional e transparente.

- Empresa/instituição: comunicados gerais para equipes, clientes ou público.
  Priorize clareza, organização e formalidade.

- Cliente/usuário: pessoa solicitando informações, suporte ou fazendo uma reclamação.
  Mantenha cordialidade, empatia e foco na solução.

- Colega de equipe: comunicação entre pessoas do mesmo nível hierárquico.
  Use um tom colaborativo, natural e profissional.

Caso o papel do remetente não esteja explícito, deduza pelo contexto da mensagem.
Caso exista dúvida, escolha a interpretação mais provável sem alterar a intenção original.

Também identifique o objetivo principal da mensagem, como:
pedido, cobrança, aviso, solicitação, reclamação, agradecimento, feedback ou comunicação informativa.
A reescrita deve respeitar esse objetivo.

Analise também o tipo específico de comunicação dentro do contexto informado.

Quando o contexto for LinkedIn, diferencie obrigatoriamente entre:

- Post público: mensagem destinada à rede de contatos.
Priorize engajamento, clareza, autoridade profissional, storytelling e uma linguagem adequada para publicação pública.
Não transforme o texto em uma mensagem privada.

- Mensagem privada (DM): comunicação direta entre duas pessoas.
Priorize personalização, objetividade, cordialidade e naturalidade.
Considere o relacionamento entre remetente e destinatário.

- Recrutador entrando em contato: mensagem de abordagem profissional para candidato.
Mantenha um tom cordial, profissional e convidativo, sem parecer uma comunicação automática.

- Candidato entrando em contato com recrutador/empresa: demonstre interesse profissional, respeito e destaque intenção ou experiência sem exageros.

Se o tipo de comunicação não estiver explícito, deduza pelo formato e conteúdo da mensagem.

Preserve o sentido original e as informações factuais (datas, horários, nomes),
apenas ajuste redação, tom e formatação.

Não invente informações novas, promessas, justificativas ou acontecimentos que não estejam presentes na mensagem original.

Responda ESTRITAMENTE com um JSON válido, sem markdown, sem texto antes ou depois,
no formato exato:
{{"texto": "mensagem reescrita aqui", "alteracoes": ["alteração 1", "alteração 2", "alteração 3", "alteração 4", "alteração 5"]}}.

O campo "alteracoes" deve conter exatamente 5 alterações, itens curtos (poucas palavras cada),
descrevendo objetivamente as principais mudanças feitas em relação ao texto original.
"""
)


def extrair_json(conteudo: str) -> dict:
    """Remove possíveis blocos de código markdown e faz o parse do JSON retornado pelo modelo."""

    texto = conteudo.strip()

    # remove cercas de bloco de código tipo ```json ... ``` ou ``` ... ```
    texto = re.sub(r"^```(json)?", "", texto).strip()
    texto = re.sub(r"```$", "", texto).strip()

    return json.loads(texto)


@app.route("/api/melhorar", methods=["POST"])
def melhorar():

    dados = request.get_json(silent=True) or {}

    contexto = dados.get("contexto")
    tom = dados.get("tom")
    texto_original = (dados.get("texto") or "").strip()

    if contexto not in CONTEXTOS:
        return jsonify({"erro": "Contexto inválido ou não informado."}), 400

    if tom not in TONS:
        return jsonify({"erro": "Tom inválido ou não informado."}), 400

    if not texto_original:
        return jsonify({"erro": "Texto não pode estar vazio."}), 400

    if len(texto_original) > 500:
        return jsonify({"erro": "Texto excede o limite de 500 caracteres."}), 400

    prompt_sistema = montar_prompt_sistema(CONTEXTOS[contexto], TONS[tom])

    try:
        completion = client.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": texto_original},
            ],
            temperature=0.2,
            max_completion_tokens=1000,
            top_p=1,
            stream=False,
        )

        conteudo = completion.choices[0].message.content

    except Exception as erro:
        app.logger.exception("Erro ao chamar a API da Groq")
        return jsonify({"erro": "Falha ao consultar o modelo de IA."}), 502

    try:
        resultado = extrair_json(conteudo)
        texto_final = resultado["texto"]
        alteracoes = resultado.get("alteracoes", [])
    except (json.JSONDecodeError, KeyError, TypeError):
        app.logger.error("Resposta do modelo fora do formato esperado: %s", conteudo)
        return jsonify({"erro": "Resposta do modelo em formato inesperado."}), 502

    return jsonify({"texto": texto_final, "alteracoes": alteracoes})



@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)