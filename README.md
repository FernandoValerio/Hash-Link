# Hash link

Aplicação desktop para aquisição, identificação, preservação e cálculo de hashes criptográficos de arquivos disponibilizados através de URLs.

O sistema possui uma interface gráfica desenvolvida em **PySide6/Qt**, permitindo que todo o processo seja realizado sem necessidade de utilização de terminal ou comandos.

> **Status:** Em desenvolvimento — MVP.

---

## Objetivo

O File Hasher foi desenvolvido para facilitar a aquisição e documentação técnica de arquivos disponibilizados através da Internet.

A partir de uma URL, o sistema pode:

1. acessar o recurso;
2. identificar seu tipo;
3. localizar arquivos disponíveis;
4. apresentar os arquivos encontrados ao operador;
5. permitir a seleção dos arquivos;
6. realizar o download;
7. calcular hashes criptográficos;
8. registrar informações da aquisição;
9. preservar os arquivos recebidos;
10. gerar um manifesto;
11. exportar os resultados.

---

# Interface gráfica

Toda a operação do sistema deve ser realizada através da interface gráfica.

Não é necessário conhecimento de programação ou utilização do terminal.

A janela principal possui uma barra de menu superior. Por hora, os menus disponíveis são:

* **Arquivo** (mnemônico `A`, `Alt+A`) — nova aquisição, abrir histórico, configurações, sair;
* **Help** (mnemônico `H`, `Alt+H`) — sobre o programa, documentação.

Novos menus serão adicionados conforme o desenvolvimento avançar.

A interface será organizada em páginas:

```text
┌──────────────────────────────────────────────────────┐
│ Arquivo   Help                                        │
├──────────────────────────────────────────────────────┤
│ File Hasher                              ⚙ Config.  │
├──────────────┬───────────────────────────────────────┤
│              │                                       │
│  Aquisição   │                                       │
│              │                                       │
│  Resultados  │         ÁREA PRINCIPAL                │
│              │                                       │
│  Histórico   │                                       │
│              │                                       │
│  Configurações│                                      │
│              │                                       │
├──────────────┴───────────────────────────────────────┤
│ Status: Pronto                         v0.1.0        │
└──────────────────────────────────────────────────────┘
```

---

# Fluxo de utilização

## 1. Nova aquisição

O operador informa a URL:

```text
┌─────────────────────────────────────────────────────┐
│ Nova aquisição                                      │
│                                                     │
│ URL                                                 │
│ ┌─────────────────────────────────────────────────┐ │
│ │ https://exemplo.com/documentos/                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│              [ Analisar URL ]                       │
└─────────────────────────────────────────────────────┘
```

---

## 2. Identificação

O sistema verifica o recurso e apresenta:

* tipo de recurso;
* URL;
* URL final;
* status HTTP;
* quantidade de arquivos encontrados.

---

## 3. Seleção dos arquivos

Os arquivos encontrados são apresentados em uma tabela:

| Selecionar | Arquivo       | Tipo | Tamanho | URL |
| ---------- | ------------- | ---- | ------: | --- |
| ☑          | documento.pdf | PDF  |  2,3 MB | ... |
| ☑          | foto01.jpg    | JPEG |  4,8 MB | ... |
| ☐          | video.mp4     | MP4  |  184 MB | ... |

O operador poderá:

* selecionar todos;
* desmarcar todos;
* selecionar individualmente;
* filtrar por nome;
* filtrar por extensão;
* ordenar por tamanho;
* ordenar por nome.

---

# 4. Algoritmos

O operador seleciona os algoritmos desejados:

```text
Algoritmos de hash

☑ SHA-256
☑ SHA-512
☐ SHA-384
☐ SHA-3-256
☐ SHA-3-512
☐ BLAKE2b
☐ MD5
☐ SHA-1
```

**SHA-256 será selecionado por padrão.**

MD5 e SHA-1 estarão disponíveis principalmente para compatibilidade e comparação com registros legados.

---

# 5. Aquisição

Após iniciar:

```text
Aquisição em andamento

████████████████████░░░░░  78%

Arquivo atual:
foto02.jpg

3 de 4 arquivos

Velocidade:
12,4 MB/s

Recebido:
154 MB / 184 MB
```

O sistema deverá permanecer responsivo durante a aquisição.

Operações demoradas deverão ser executadas em threads/workers separados da interface.

---

# 6. Resultado

Ao terminar:

```text
Aquisição concluída

4 arquivos processados
4 arquivos adquiridos
4 hashes calculados
0 erros

[ Ver resultados ]
[ Abrir pasta ]
[ Exportar ]
```

---

# 7. Resultados

Os resultados serão apresentados em tabela:

| Arquivo       | Tamanho | SHA-256  | SHA-512  | Status |
| ------------- | ------: | -------- | -------- | ------ |
| documento.pdf |  2,3 MB | `a8f...` | `72c...` | OK     |
| foto01.jpg    |  4,8 MB | `9bd...` | `31a...` | OK     |

Será possível copiar o hash individualmente.

---

# 8. Manifesto

Cada aquisição possuirá um manifesto contendo os dados necessários para documentar o procedimento.

Exemplo:

```json
{
    "acquisition_id": "ACQ-20260910-140530",
    "source_url": "https://exemplo.com/",
    "final_url": "https://exemplo.com/",
    "started_at": "2026-09-10T14:05:30-03:00",
    "finished_at": "2026-09-10T14:08:42-03:00",
    "algorithms": [
        "sha256",
        "sha512"
    ],
    "files": []
}
```

---

# Exportação

O sistema deverá permitir exportação para:

* JSON;
* CSV;
* XLSX;
* PDF.

A exportação deverá ser realizada pela interface.

---

# Histórico

O sistema deverá manter um histórico das aquisições realizadas:

```text
Histórico

ACQ-20260910-140530
10/09/2026 14:05
4 arquivos
SHA-256 / SHA-512

ACQ-20260909-091422
09/09/2026 09:14
17 arquivos
SHA-256
```

O operador poderá abrir uma aquisição anterior e visualizar seus resultados.

---

# Tecnologia

## Interface

**PySide6 / Qt**

A escolha do Qt permite:

* interface moderna;
* tabelas avançadas;
* menus;
* diálogos;
* barras de progresso;
* ícones;
* temas;
* escalabilidade;
* suporte a Windows, Linux e macOS.

---

## Backend

Python.

Principais componentes:

* `requests` — comunicação HTTP;
* `BeautifulSoup` — análise HTML;
* `hashlib` — hashes;
* `openpyxl` — XLSX;
* `reportlab` — PDF;
* `PySide6` — interface gráfica.

---

# Princípios do projeto

## Separação entre interface e processamento

A interface não deve conter regras de aquisição ou hashing.

## Integridade

Os arquivos recebidos devem ser preservados.

## Rastreabilidade

Cada aquisição recebe um identificador único.

## Reprodutibilidade

As informações relevantes da aquisição devem ser registradas.

## Segurança

O programa não deve executar automaticamente arquivos adquiridos.

## Transparência

Erros, redirecionamentos e alterações de estado devem ser registrados.

---

# Uso forense

O File Hasher é uma ferramenta auxiliar.

O cálculo de hash não comprova isoladamente:

* autoria;
* autenticidade;
* origem;
* data de criação;
* ausência de alteração anterior à aquisição.

A interpretação dos resultados deve considerar o procedimento completo de aquisição e preservação.

---

# Requisitos

* Windows 10/11 ou sistema operacional suportado pelo Qt;
* Python 3.11+ durante o desenvolvimento;
* conexão de rede quando a aquisição depender de recurso remoto.

Futuramente poderão ser disponibilizados instaladores:

```text
FileHasher-Setup.exe
```

permitindo utilizar o programa sem instalação do Python.

---

# Roadmap

## MVP

* [x] Interface PySide6
* [x] Menu superior (Arquivo, Help)
* [ ] Entrada de URL
* [ ] Detecção do recurso
* [ ] Descoberta de arquivos
* [ ] Seleção de arquivos
* [ ] Download
* [ ] SHA-256
* [ ] SHA-512
* [ ] Manifesto
* [ ] CSV
* [ ] JSON
* [ ] Histórico

## Versão 0.2

* [ ] XLSX
* [ ] PDF
* [ ] filtros
* [ ] pesquisa
* [ ] logs
* [ ] identificação MIME
* [ ] comparação entre aquisições

## Versão 0.3

* [ ] cadeia de custódia
* [ ] informações TLS
* [ ] timestamp
* [ ] assinatura digital
* [ ] WARC
* [ ] banco de dados

## Futuro

* [ ] instalador Windows
* [ ] execução portátil
* [ ] armazenamento externo
* [ ] integração com sistemas periciais
