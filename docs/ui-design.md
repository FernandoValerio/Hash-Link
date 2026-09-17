\# UI Design



\## Objetivo



A interface deve priorizar simplicidade operacional, clareza visual e redução da possibilidade de erro do operador.



O usuário deve conseguir realizar uma aquisição sem necessidade de conhecimento técnico sobre Python, HTTP ou linha de comando.



\---



\# Tecnologia



A interface será desenvolvida utilizando:



\*\*PySide6 / Qt\*\*



Tkinter não será utilizado.



\---



\# Menu superior



A janela principal possui uma barra de menu (`QMenuBar`) no topo, acima das abas.



Por hora, dois menus estão implementados:



\## Arquivo (\&Arquivo — mnemônico "A", \`Alt+A\`)



| Item | Atalho | Ação |

| --- | --- | --- |

| Nova aquisição | \`Ctrl+N\` | Volta para a aba "Aquisição" |

| Abrir histórico | \`Ctrl+H\` | Vai para a aba "Histórico" |

| Configurações | — | Vai para a aba "Configurações" |

| Sair | \`Ctrl+Q\` | Fecha a aplicação |



\## Help (\&Help — mnemônico "H", \`Alt+H\`)



| Item | Ação |

| --- | --- |

| Sobre o Hash Link | Exibe versão e descrição do programa |

| Documentação | Indica onde encontrar os documentos em \`docs/\` |



Cada item de menu também possui seu próprio mnemônico (letra sublinhada), permitindo navegação completa pelo teclado, por exemplo \`Alt+A\` seguido de \`N\` para "Nova aquisição".



Novos menus (ex.: Editar, Ferramentas, Exportar) serão adicionados futuramente seguindo o mesmo padrão, implementado em \`src/ui/main\_window.py\` (métodos \`\_build\_file\_menu\` e \`\_build\_help\_menu\`).



\---



\# Estrutura principal



A janela principal será dividida em:



```text

┌───────────────────────────────────────────────┐

│ Logo / File Hasher             Configurações  │

├──────────────┬────────────────────────────────┤

│              │                                │

│ Nova         │                                │

│ aquisição    │                                │

│              │                                │

│ Histórico    │        Conteúdo                │

│              │                                │

│ Configuração │                                │

│              │                                │

├──────────────┴────────────────────────────────┤

│ Pronto                         Versão 0.1.0   │

└───────────────────────────────────────────────┘

```



\---



\# Nova aquisição



A tela principal deverá destacar a entrada da URL.



Elementos:



\* campo URL;

\* botão "Analisar";

\* seleção de algoritmos;

\* diretório de destino;

\* opção de preservar arquivos;

\* botão "Iniciar aquisição".



\---



\# Tabela de arquivos



A tabela deve permitir:



\* seleção múltipla;

\* ordenação;

\* pesquisa;

\* filtros;

\* copiar URL;

\* copiar hash;

\* visualizar detalhes.



\---



\# Estados



Cada operação deverá possuir estado visual.



\### Aguardando



```text

● Aguardando

```



\### Processando



```text

◌ Processando

```



\### Concluído



```text

✓ Concluído

```



\### Erro



```text

! Erro

```



A cor não deve ser o único mecanismo de diferenciação; ícones e texto também devem indicar o estado.



\---



\# Aparência



A aplicação deverá possuir:



\* espaçamento consistente;

\* tipografia legível;

\* botões com hierarquia visual;

\* ícones;

\* tabelas limpas;

\* diálogos claros;

\* suporte a tela de alta resolução.



Deverá existir suporte futuro para:



\* tema claro;

\* tema escuro.



\---



\# Experiência do usuário



A aplicação deve evitar mensagens técnicas desnecessárias.



Em vez de:



```text

requests.exceptions.ConnectionError

```



mostrar:



```text

Não foi possível acessar o recurso.



Verifique:

• a conexão de rede;

• o endereço informado;

• se o servidor está disponível.



Detalhes técnicos podem ser consultados no registro da aquisição.

```



\---



\# Operações demoradas



Downloads e cálculos não poderão bloquear a interface.



A aplicação deverá utilizar:



```text

GUI

&#x20;│

&#x20;├── Worker de aquisição

&#x20;│

&#x20;├── Worker de hashing

&#x20;│

&#x20;└── Worker de exportação

```



Os workers comunicarão seu progresso à interface por sinais/eventos do Qt.



\---



\# Prevenção de erros



Antes de iniciar uma aquisição, o sistema deverá apresentar uma confirmação:



```text

Confirmar aquisição



URL:

https://exemplo.com/documentos/



Arquivos selecionados:

17



Algoritmos:

SHA-256

SHA-512



Destino:

D:\\Aquisições\\ACQ-20260910-140530



\[Cancelar]       \[Iniciar]

```



Isso reduz o risco de uma aquisição acidental ou com parâmetros incorretos.



