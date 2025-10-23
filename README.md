# Acelera Concurso IA
API Rest responsável por gerar conteúdo a parti da IA do Google, [Gemini](https://gemini.google.com/).

Esse projeto é pensado para a configuração de prompts e respostas sobre questões para concurso e organização.

## Fazendo Funcionar
Esse projeto possui um modulo que faz todo o inicio da configuração, lhes apresento o [App](app.py). Lembrando que primero o projeto e as dependências devem
estar devidamente ajustadas.

Você pode tanto usar a IDE de vocês como correr o seguinte comando no console:
```commandline
python app.py
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

| Script                                 | Descrição                                    |
|----------------------------------------|----------------------------------------------|
| [gitter.py](gitter.py)                 | Tarefas que envolve GIT.                     |
| [rename_env.py](rename_env.py)         | Renomear arquivo [.env.example] para `.env`. |
| [gen_secret_key.py](gen_secret_key.py) | Gerar uma chave no padrão SSH.               |

## Variáveis de Ambiente
Garanta que você já copiou o arquivo [.env.example](.env.example) para [.env](.env). Se pronto, agora veja a tabela de variáveis de ambiente:

| Variável         | Descrição                       | Valor Esperado             |
|------------------|---------------------------------|----------------------------|
| `GEMINI_API_KEY` | Chave de API do Google Gemini.  | zUDi6p4nJVv...cLCZsS7ctI=  |
| `SELECT_MODEL`   | O modelo que será utilizado.    | Flash ou Pro ou FlashLight |
| `APP_NAME`       | O nome ou tag para a aplicação. | AceleraConcursoAI          |

Lembrando que a variável `GEMINI_API_KEY` deve ser gerada na sua conta [Google AI Studio](https://aistudio.google.com/).

Disponibilizo esse tutorial: [Tutorial Gerar Gemini API KEY](https://ai.google.dev/gemini-api/docs/api-key).

Copie a chave gerada para a `GEMINI_API_KEY` variável dentro do [.env](.env).

## Modelos Utilizados
Esse projeto utiliza largamente os modelos disponibilizados pelo Gemini. O dataclass [environ.GeminiModel](src/core/constraints.py:17).

Para saber mais sobre os modelos do Gemini, acesse: [docs](https://ai.google.dev/gemini-api/docs/models).

## Rotas e Modelos
Aqui você encontra as rotas, os modelos e os requisitos para o funcionamento adequado da aplicação. Trata-se de uma tabela com as informações pertinentes sobre
as rotas dessa aplicação.

| Método | Rota                | DTO                                   | Auth | Header                                                                 |
|--------|---------------------|---------------------------------------|------|------------------------------------------------------------------------|
| POST   | `/prompt-questions` | [PromptDTO](src/models/prompt_dto.py) | OFF  | <details><code>{ "Content-Type": "application/json" }</code></details> |

As respostas dessa API segue a convenção do modelo de response: [PromptResponse](src/models/prompt_resp.py).

*That's All Folks!*
