# E5 — Suite API (caja negra)

Esta suite utiliza `pytest`, `requests`, `PyYAML` y `jsonschema`, y consume el `openapi.yaml` original del ambiente. No abre el código del servicio.

1. Levanta **una sola instancia** de `node server.mjs` dentro de la carpeta privada `ambiente` (Node >= 22.13).
2. En otra terminal, desde la raíz del repositorio, crea el venv e instala `E5-automatizacion/requirements.txt`.
3. Define estas variables solo en la terminal (NUNCA dentro de Git):

```bash
export QA_BASE_URL=http://localhost:4010
export QA_OPENAPI="$HOME/Downloads/ambiente/openapi.yaml"  # Ajustar a la ruta real de tu Mac
export QA_APP_NORTE="<TOKEN_QA_NORTE>"
export QA_APP_ESTE="<TOKEN_QA_ESTE>"
export QA_APP_SUR="<TOKEN_QA_SUR>"
export QA_APP_OESTE="<TOKEN_QA_OESTE>"
export QA_OPS_NORTE="<TOKEN_QA_OPS_NORTE>"
```

4. Smoke de liberación:

```bash
python -m pytest -q -m smoke E5-automatizacion/tests --junitxml=smoke-local.xml
```

5. Suite completa:

```bash
python -m pytest -q E5-automatizacion/tests --junitxml=resultado-local.xml
```

**Precaución:** cada test invoca `POST /v1/_sandbox/reset`, que borra y recrea la base. Nunca ejecutar contra producción. Si necesitas preservar E6, antes de ejecutar la suite guarda una copia privada de `qa.db`. Ejecutar estas pruebas **solo** en una instancia nueva y aislada de QA.

Los fallos encontrados en la suite deben permanecer como fallos. No modificar los asserts para esconder defectos. Antes de entregar, ejecuta la suite en tu Mac, conserva capturas de la terminal y el XML de resultados en una carpeta de evidencia que no contenga datos personales ni tokens; no publiques trazas sin revisarlas.

**Nota:** La prueba concurrente utiliza dos solicitudes simultáneas; repítela si es necesario y conserva evidencia de base de datos para confirmar los efectos persistidos.
