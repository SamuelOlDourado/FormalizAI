# FormalizAI - Tradutor de Mensagens Corporativas com IA

O **FormalizAI** é uma aplicação web que utiliza Inteligência Artificial para transformar mensagens simples em comunicações profissionais, adequando o tom, contexto e formalidade para diferentes situações corporativas.

A ferramenta ajuda usuários a escreverem e-mails, mensagens profissionais e comunicados de forma mais clara, objetiva e adequada ao ambiente de trabalho.

---

## 🚀 Funcionalidades

- Reescrita de mensagens utilizando Inteligência Artificial
- Escolha de contexto da mensagem:
  - E-mail
  - WhatsApp Business
  - LinkedIn
  - Comunicado interno

- Escolha de estilo de comunicação:
  - Formal
  - Muito formal
  - Amigável
  - Empático
  - Objetivo

- Exibição da mensagem original e da versão aprimorada
- Botão para copiar resultado
- Contador de caracteres
- Interface responsiva
- API protegida no backend


---

## 🛠️ Tecnologias utilizadas

### Front-end

- HTML5
- CSS3
- JavaScript
- Bootstrap 5

### Back-end

- Python
- Flask
- Requests
- Python-dotenv

### Inteligência Artificial

- Groq API
- Modelo de linguagem Llama

### Deploy

- Vercel

---

## 📂 Estrutura do projeto

```
FormalizAI/
│
├── app.py                 # Servidor Flask e rotas da aplicação
├── requirements.txt       # Dependências do projeto
├── vercel.json            # Configurações de deploy
│
├── templates/
│   └── index.html         # Interface principal
│
├── static/
│   ├── style.css          # Estilos da aplicação
│   └── script.js          # Lógica do front-end
│
├── .env                   # Variáveis de ambiente (não enviado ao GitHub)
└── .gitignore
```

---

# ⚙️ Como executar o projeto localmente

## 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
```

Entre na pasta:

```bash
cd FormalizAI
```

---

## 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente:

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configure as variáveis de ambiente

Crie um arquivo chamado:

```
.env
```

Adicione sua chave da API:

```env
GROQ_API_KEY=sua_chave_aqui
```

---

## 5. Execute a aplicação

```bash
python app.py
```

Acesse:

```
http://127.0.0.1:5000
```

---

# 🔒 Segurança

A chave da API da Groq não fica exposta no JavaScript ou no navegador.

O fluxo da aplicação funciona assim:

```
Usuário
   ↓
Interface Web
   ↓
Backend Flask
   ↓
Groq API
   ↓
Resposta da IA
   ↓
Usuário
```

A variável `GROQ_API_KEY` é armazenada utilizando variáveis de ambiente e nunca é enviada ao repositório.

---

# 🌐 Deploy

O projeto está preparado para deploy utilizando a plataforma Vercel.

As variáveis de ambiente devem ser configuradas diretamente no painel da Vercel:

```
GROQ_API_KEY = sua_chave
```

---

# 👨‍💻 Autor

**Samuel Dourado**

Desenvolvedor Full Stack em formação.

- GitHub: https://github.com/SamuelOlDourado
- Portfólio: https://samueld-portfolio-oficial.vercel.app/

---

⭐ Se este projeto foi útil, considere deixar uma estrela no repositório!