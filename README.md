# Acelera Concurso IA
API Rest responsável por gerar conteúdo a parti da IA do Google, [Gemini](https://gemini.google.com/).

Esse projeto é pensado para a configuração de prompts e respostas sobre questões para concurso e organização.

Você pode utilizar essa API para gerar através de Inteligência Artificial:
* Dicas de Estudo;
* Questões com base em arquivo PDF;
* Questões com base em link de legislação.

Uma vez que essas questões são geradas no formato [QuestionResponse](src/models/question_response.py), você poderá:
* Fazer o Download de um arquivo PDF com as questões geradas (gabarito já incluso).

Esse projeto utiliza-se de recursos de [Web Scrapping](https://en.wikipedia.org/wiki/Web_scraping) na opção de gerar questões por
link de legislação.

## Tabela de Conteúdo
1. [Fazendo Funcionar](#fazendo-funcionar)
2. [Configuração](#configuração)
3. [Scripts Utilitários](#scripts-utilitários)
4. [Variáveis de Ambiente](#variáveis-de-ambiente)
5. [Modelos I.A. Utilizados](#modelos-ia-utilizados)
6. [Rotas e Modelo](#rotas-e-modelos)

## Fazendo Funcionar
Esse projeto possui um modulo que faz todo o inicio da configuração, lhes apresento o [App](app.py). Lembrando que primero o projeto e as dependências devem
estar devidamente ajustadas.

Você pode tanto usar a IDE de vocês como correr o seguinte comando no console:
```commandline
python app.py
```

Ou através de comandos do FLask -- com ou sem debug ativado:
```commandline
flask --app app run --debug
```
```commandline
flask --app app run
```

**OBSERVAÇÃO:** Para que tenha o efeito necessário, siga os passos descritos no capítulo: [Configuração](#configuração).

# Configuração
Esse projeto foi construído sob a versão Python 3.14, instalada com o [PyEnv](https://github.com/pyenv/pyenv).

Uma vez sabendo disso, utilize a IDE para criar um ambiente virtual ".venv" na raiz do seu projeto. Se preferir a linha de comando:
```commandline
python3 -m venv .venv
```
Lembrando que será seguido a versão do Python para essa instalação. Eu recomendo fortemente usar a interface do [PyCharm](https://www.jetbrains.com/pycharm).

Uma vez configurado o ambiente virtual, corra o seguinte comando, ele irá instalar as dependências no ambiente virtual.
```commandline
pip install -r requirements.txt
```
Copie o arquivo [.env.example](.env.example) para um novo arquivo chamado [.env](.env). Se desejar, apenas execute o script [rename_env.py](rename_env.py) descrito
na tabela de [Scripts Utilitários](#scripts-utilitários), ou cole o seguinte comando:
```commandline
python rename_env.py
```
Acesse o tópico [Variáveis de Ambiente](#variáveis-de-ambiente) e faça a sua devida configuração.

As variáveis de ambiente são carregadas no arquivo [constraints.py](/src/core/constraints.py).

**OBSERVAÇÃO:** Se você utiliza Debian/Ubuntu ou alguma distribuição linux que utiliza debian como "background", corra o seguinte comando:
```commandline
sudo apt install xclip
```
Esse processo é necessário para que o script [gen_secret_key.py](gen_secret_key.py) funcione nessas distribuições linux.

Agora com as dependências instaladas, você poderá fazer funcionar esse projeto!

## Scripts Utilitários
Esse projeto possui alguns scripts utilitários que visa auxiliar o desenvolvedor em tarefas como escritas de comandos, uma vez que esse processo se torna semi-automatizado.

Abaixo uma tabela dos "Scripts Utilitários" que existem nesse projeto.

| Script                                     | Descrição                                    |
|--------------------------------------------|----------------------------------------------|
| [gitter.py](gitter.py)                     | Tarefas que envolve GIT.                     |
| [rename_env.py](rename_env.py)             | Renomear arquivo [.env.example] para `.env`. |
| [gen_secret_key.py](gen_secret_key.py)     | Gerar uma chave no padrão SSH.               |
| [rename_cors_file.py](rename_cors_file.py) | Renomear arquivo cors_origin.example.txt     |

## Variáveis de Ambiente
Garanta que você já copiou o arquivo [.env.example](.env.example) para [.env](.env). Se pronto, agora veja a tabela de variáveis de ambiente:

| Variável          | Descrição                                                      | Valor Esperado             |
|-------------------|----------------------------------------------------------------|----------------------------|
| `GEMINI_API_KEY`  | Chave de API do Google Gemini.                                 | zUDi6p4nJVv...cLCZsS7ctI=  |
| `SELECT_MODEL`    | O modelo que será utilizado.                                   | Flash ou Pro ou FlashLight |
| `APP_NAME`        | O nome ou tag para a aplicação.                                | AceleraConcursoAI          |
| `HOST`            | Nome do hospedeiro ou IP.                                      | localhost                  |
| `PORT`            | Número da porta de acesso.                                     | 8000                       |
| `ENVIRON`         | Ambiente de desenvolvimento, influencia a escolha do servidor. | DEVELOPMENT ou PRODUCTION  |
| `DEFAULT_TIMEOUT` | Tempo máximo de espera para uma resposta desta API.            | 120 (pode personalizar)    |
| `CORS_FILE_NAME`  | Nome do arquivo da lista de origins.                           | cors_origins.txt           |
| `PUBLIC_SECRET`   | Chave pública para acesso a esta API.                          | zUDi6p4nJVv...cLCZsS7ctI=  |
| `PRIVATE_SECRET`  | Chave privada para acesso a esta API (interna).                | zUDi6p4nJVv...cLCZsS7ctI=  |

Lembrando de executar o script [RenameCorsFile](rename_cors_file.py) pela primeira vez, então a variável `CORS_FILE_NAME`
funcionará perfeitamente.

Lembrando que a variável `GEMINI_API_KEY` deve ser gerada na sua conta [Google AI Studio](https://aistudio.google.com/).

Disponibilizo esse tutorial: [Tutorial Gerar Gemini API KEY](https://ai.google.dev/gemini-api/docs/api-key).

Copie a chave gerada para a `GEMINI_API_KEY` variável dentro do [.env](.env).

## Modelos I.A. Utilizados
Esse tópico é sobre os modelos de IA utilizados na configuração desse projeto. Aqui você encontra alguns links interessantes para aprofundamento, aproveite!

Esse projeto utiliza largamente os modelos disponibilizados pelo Gemini. O dataclass [environ.GeminiModel](src/core/constraints.py:#L19).

Para saber mais sobre os modelos do Gemini, acesse: [docs](https://ai.google.dev/gemini-api/docs/models).

## Rotas e Modelos
Aqui você encontra as rotas, os modelos e os requisitos para o funcionamento adequado da aplicação. Trata-se de uma tabela com as informações pertinentes sobre
as rotas dessa aplicação. **TODAS AS ROTAS ESTÃO SOB AUTENTICAÇÃO DE USUÁRIO VIA *JSON WEB TOKEN (JWT).***

| Método | Rota                          | DTO                                                                   | Auth | Header                                                                                                    |
|--------|-------------------------------|-----------------------------------------------------------------------|------|-----------------------------------------------------------------------------------------------------------|
| POST   | `/prompt-questions/study-tip` | [PromptDTO](src/models/prompt_dto.py)                                 | ON   | <details><code>{ "Content-Type": "application/json", "Authorization": "Bearer <token>" }</code></details> |
| POST   | `/question`                   | [QuestionDTO](src/models/question_dto.py)                             | ON   | <details><code>{ "Content-Type": "application/json", "Authorization": "Bearer <token>" }</code></details> |
| POST   | `/question/from-pdf`          | [QuestionDTO](src/models/question_dto.py) + PDF file (multipart/form) | ON   | <details><code>{ "Authorization": "Bearer <token>" }</code></details>                                     |
| POST   | `/question/convert/to-pdf`    | [QuestionResponse](src/models/question_response.py)                   | ON   | <details><code>{ "Content-Type": "application/json", "Authorization": "Bearer <token>" }</code></details> |

* A rota `/question/convert/to-pdf` retorna um arquivo pdf para download.

As respostas dessa API segue a convenção do modelo de response:
* [PromptResponse](src/models/prompt_response.py);
* [QuestionResponse](src/models/question_response.py).

[PromptDTO](src/models/prompt_dto.py)
```json
{
  "prompt": "prompt message to generating another text", 
  "params": ["param 1","param 2"]
}
```

* O valor de texto `prompt` é obrigatório, já a lista `params` é opcional.

[QuestionDTO](src/models/question_dto.py)
```json
{
  "level": "UNDEFINED | GRADUATED | HIGH_SCHOOL | TECHNICAL",
  "status": "three alternatives | four alternatives | five alternatives | six alternatives | right wrong alternatives",
  "prompt": "configuração do texto do prompt", 
  "questions": 20,
  "format": "formato de retorno | null",
  "language": "brazilian portuguese",
  "public_tender": "nome do concurso | null",
  "subject":  "nome da disciplina do concurso | null",
  "board_name": "nome da banca do concurso | null",
  "topic": "nome do assunto da disciplina do concurso | null",
  "law_link": "law link url | null"
}
```

[PromptResponse](src/models/prompt_response.py)
```json
{
  "text": "text value generated by AI setting here to returns as a json"
}
```

[QuestionResponse](src/models/question_response.py)
```json
{
  "questions": [{
    "id": 0,
    "question": "enunciado da questão",
    "alternatives": ["alternativa a","alternativa b"],
    "answer": "alternativa a"
  }],
  "public_tender": "nome do concurso | null",
  "board_name": "nome da banca do concurso | null"
}
```

[StudyTipsResponse](src/models/study_tips_response.py)
```json
{
  "name": "texto principal da dica de estudo",
  "description": "breve descrição da dica de estudo",
  "ai_generate": true
}
```

* `ai_generate` pode ser `true` quando o conteúdo foi gerado por inteligência artificial, `false` quando não foi.

**Considerações**

* Os parametros de lista aqui descrito, podem ter de 0 elementos a vários, obedecendo o tipo;
* Tudo o que está entre aspas é texto;
* Os parametros que são opcionais, você encontra declarado como `"alguma coisa | null"` no objeto acima.

*That's All Folks!*
