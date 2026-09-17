# Modelo de Domínio

## Acquisition

```python
id: str
source_url: str
final_url: str
started_at: datetime
finished_at: datetime
status: str
```

## AcquiredFile

```python
name: str
url: str
size: int
mime_type: str
local_path: str
status: str
```

## HashResult

```python
algorithm: str
value: str
calculated_at: datetime
```
