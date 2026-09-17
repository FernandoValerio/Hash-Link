# Arquitetura do Sistema

## Visão Geral

O Hash Link é uma aplicação desktop desenvolvida em Python com interface gráfica baseada em PySide6.

O objetivo principal do sistema é realizar a aquisição, preservação, identificação e documentação de arquivos disponibilizados através de URLs, gerando hashes criptográficos e registros auditáveis do procedimento realizado.

A arquitetura foi projetada para manter separação clara entre interface, regras de negócio e persistência de dados.

## Estrutura de Diretórios

```text
src/
├── aquisition/
├── exporters/
├── hashing/
├── manifest/
├── models/
├── ui/
└── utils/
```

## Responsabilidades dos Módulos

### acquisition
- análise de URLs
- identificação de recursos
- descoberta de arquivos
- download
- monitoramento de progresso

### hashing
- cálculo de hashes
- validação de algoritmos
- processamento em blocos

### manifest
- geração do manifesto
- registro de metadados
- rastreabilidade

### exporters
- JSON
- CSV
- XLSX
- PDF

### models
Modelos de domínio da aplicação.

### ui
Interface gráfica PySide6.

### utils
Funções auxiliares compartilhadas.
