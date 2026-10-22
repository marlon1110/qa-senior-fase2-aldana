# QA Senior — HU-410: Alta sin código con verificación de identidad

**Caso práctico Fase 2 | Entrega QA de caja negra**

## Objetivo y alcance

Evaluar si el backend de alta en autoservicio puede liberarse con seguridad, contrastando la historia HU-410 y OpenAPI con pruebas de API, automatización y consultas SQLite. La aplicación móvil no fue proporcionada: sus casos están diseñados pero no ejecutados. El proveedor de identidad se simuló con el ambiente QA.

## Índice de entregables

| Entregable | Archivo(s) |
|---|---|
| E1 — Análisis y discrepancias | `E1-analisis/analisis.md`, `E1-analisis/ajustes-segun-openapi.md` |
| E2 — Estrategia | `E2-estrategia/estrategia.md` |
| E3 — Matriz trazable | `E3-casos/matriz-preliminar.csv` |
| E4 — Ejecución y defectos | `E4-defectos/BUG-01.md` a `BUG-08.md`, `otros-hallazgos.md`, `Evidencias/` |
| E5 — Suite ejecutable de API | `E5-automatizacion/tests/`, `pytest.ini`, `requirements.txt`, `README-ejecucion.md`, `resumen-ejecutado.md`, `evidencia-resumen-ejecuciones.md` |
| E6 — Validación SQL | `E6-datos/E6-resultados-consolidados.md`, `consulta-cp09.sql`, `E6-consultas-reproducibles.sql` |
| E7 — Informe ejecutivo | `E7-informe/informe.md` |
| E8 — Bitácora de herramientas | `E8-herramientas/bitacora.md` |
| E9 — Demostración | [Video en YouTube](https://youtu.be/o1ufeCWFcyQ) · [`E9-video.md`](E9-video.md) |

## E9 — Video de demostración

**[Ver video «Caso Práctico de QA» en YouTube](https://youtu.be/o1ufeCWFcyQ)**

La demostración fue grabada y publicada por el candidato. El enlace se presenta también en [`E9-video.md`](E9-video.md). Confirmar su reproducción en navegación privada antes del envío final.

## Cómo ejecutar desde ambiente recién iniciado

**Requisitos:** Node.js >=22.13; Python 3.9+; servicio y `openapi.yaml` suministrados de forma privada por la empresa. No se adjuntan ni publican.

1. En terminal independiente, entrar a carpeta **privada** `ambiente/` y ejecutar `node server.mjs`. Queda en `http://localhost:4010`. **Arrancar reinicia `qa.db`.**
2. Desde la raíz de este repositorio, preparar Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r E5-automatizacion/requirements.txt
```

3. Exportar variables **solo en la terminal**, según las instrucciones y tokens ficticios proporcionados en `ambiente/README.md`:

```bash
export QA_BASE_URL=http://localhost:4010
export QA_OPENAPI=/ruta/privada/ambiente/openapi.yaml
export QA_APP_NORTE=<TOKEN_QA_NORTE>
export QA_APP_ESTE=<TOKEN_QA_ESTE>
export QA_APP_SUR=<TOKEN_QA_SUR>
export QA_APP_OESTE=<TOKEN_QA_OESTE>
export QA_OPS_NORTE=<TOKEN_QA_OPERACIONES>
```

4. Ejecutar smoke independiente y luego suite completa:

```bash
python -m pytest -q -m smoke E5-automatizacion/tests
python -m pytest -q -ra E5-automatizacion/tests
```

**Precaución:** el fixture llama a `POST /v1/_sandbox/reset` antes de cada prueba y borra los datos anteriores. Usar exclusivamente en el ambiente local aislado. Se espera que las pruebas fallen si detectan defectos reales; no modificar aserciones para obtener PASS.

## Resultados observados en ejecución local

- Smoke: **1 PASSED, 9 FAILED** (10 ejecutadas).
- Completa: **8 PASSED, 10 FAILED** (18 ejecutadas).
- BUG-02 se reprodujo manualmente y se comprobó mediante SQLite con KYC facial 0.72 frente a umbral 0.80, alta persistida y código consumido.
- Los resultados históricos en E6 están separados de las pruebas nuevas. Altas del 15/10/2026 en Guatemala: **2**.
- **Recomendación: NO-GO** hasta corregir controles críticos y reejecutar regresión.

## Confidencialidad

Este repositorio solo contiene la entrega. No incluir el enunciado original, `ambiente/`, `qa.db`, copias SQLite, tokens, CUI completos, fotos de DPI/selfie, credenciales o reportes sin saneamiento. Verificar en GitHub que el repositorio y el video sean accesibles sin iniciar sesión.

## Estado y límites de evidencia

Los resultados de E3 están diferenciados por ejecución completa, parcial o sin ejecutar. En E4, BUG-03 a BUG-07 proceden de ejecuciones automatizadas, mientras BUG-08 procede de una inconsistencia histórica; no se atribuyen reproducciones manuales inexistentes. La demostración E9 fue grabada y subida a YouTube; enlace en [E9-video.md](E9-video.md). No se incluye el archivo de video en el repositorio.
