# E5 — Automatización de API

Suite aún NO implementada, a la espera de `openapi.yaml` y pruebas reales del servicio. No presentar esta carpeta como automatización terminada.

**Tecnología propuesta:** Python + pytest + requests + jsonschema + PyYAML. Ajustar a herramientas que controles.

## Comandos objetivo (a completar al implementar)

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r E5-automatizacion/requirements.txt
# Verificar primero la preparación de variables locales y el servidor
pytest -m smoke E5-automatizacion/tests
pytest E5-automatizacion/tests
```

## Obligatorio

- URL base, token y device ID parametrizados sin subir secretos.
- Helpers para sesiones y simulador.
- Verificación de esquemas contra el contrato.
- Prueba concurrente sobre Idempotency-Key.
- Casos negativos que fallen cuando se reproduzca el defecto real.
- Documentar orden/reset y manejo de base recreada.
