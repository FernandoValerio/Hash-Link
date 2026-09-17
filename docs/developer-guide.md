# Guia do Desenvolvedor

## Requisitos

- Python 3.11+
- PySide6
- requests
- beautifulsoup4
- openpyxl
- reportlab

## Convenções

### Classes

```python
AcquisitionSession
ManifestBuilder
HashResult
```

### Funções

```python
calculate_hash()
generate_manifest()
export_to_csv()
```

## Regras

- A UI não deve conter regras de negócio.
- Downloads devem ocorrer fora da thread principal.
- Todo módulo novo deve possuir testes.

## Menu superior

A barra de menu principal (`QMenuBar`) é montada em `src/ui/main_window.py`.

Convenções ao adicionar um novo menu ou item:

- criar um método `_build_<nome>_menu()` que retorna um `QMenu`;
- registrar o menu em `_create_menu_bar()` via `menu_bar.addMenu(...)`;
- todo título de menu/ação deve ter um mnemônico (`&Letra`), evitando letras repetidas dentro do mesmo menu;
- atalhos de teclado (`QKeySequence`) são opcionais, mas recomendados para ações frequentes;
- a lógica do slot deve ser curta — se envolver regra de negócio, delegar para um controller/service.

Ver detalhes de UX dos menus em `docs/ui-design.md`.
