# YouDownloader - Versão Desktop para Windows

Este projeto é um simples aplicativo com interface gráfica para baixar vídeos ou extrair o áudio em MP3 de links do YouTube.

---

## Requisitos Prévios

Antes de começar, garanta que você tem os seguintes programas instalados no seu sistema Windows:

1.  **Python 3.x**: Faça o download em [python.org](https://www.python.org/). **Importante:** Durante a instalação, marque a caixa "Add Python to PATH".
2.  **FFmpeg**: Essencial para a conversão de vídeo para áudio MP3.
    -   Faça o download da versão `essentials.zip` em [gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/).
    -   O arquivo `ffmpeg.exe` precisa de ser colocado na pasta principal deste projeto.

---

## Guia de Instalação e Configuração

Siga estes passos para configurar o ambiente e construir o executável:

**1. Clone ou Baixe o Projeto**
   - Coloque todos os arquivos do projeto numa pasta no seu computador.

**2. Crie e Ative um Ambiente Virtual (Recomendado)**
   - Abra um terminal (`cmd` ou `PowerShell`) na pasta do projeto e execute:
     ```cmd
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     ```cmd
     venv\Scripts\activate
     ```
   - Você saberá que funcionou porque `(venv)` aparecerá no início da linha do terminal.

**3. Instale as Dependências Python**
   - Com o ambiente virtual ativo, instale todas as bibliotecas listadas no `requirements.txt` com um único comando:
     ```cmd
     pip install -r requirements.txt
     ```

**4. Adicione o `ffmpeg.exe`**
   - Se ainda não o fez, coloque o arquivo `ffmpeg.exe` que você baixou na pasta principal do projeto, ao lado do `main.py` e do `requirements.txt`.

---

## Como Construir o Executável (`.exe`)

Com o ambiente virtual ainda ativo e todas as dependências instaladas, execute o seguinte comando no terminal:

```cmd
pyinstaller --onefile --windowed --name YouDownloader --add-data "ffmpeg.exe;." main.py