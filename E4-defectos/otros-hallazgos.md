# E4 — Hallazgos complementarios

La selección de los ocho reportes principales combina defectos reproducidos por API y una inconsistencia histórica explícitamente identificada. Los hallazgos siguientes deben distinguirse de aquellos con reproducción mediante HTTP.

| Identificación | Severidad sugerida | Esperado | Obtenido | Fuente |
|---|---|---|---|---|
| E4-A01 — `economicActivity` nulo | Media | Campo presente de tipo string, según SignupRequest/Signup | Respuesta de alta HTTP 201 incluye `economicActivity: null` | `test_alta_exitosa_y_esquemas` / OpenAPI |
| E4-A02 — `images.selfie` nulo | Media | URI o ausencia del campo, según schema de Verification | Rechazo por DPI vencido devuelve `selfie: null` | `test_rechazos_del_proveedor[document_expired]` / OpenAPI |
| E6-H01 — Alta duplicada en M-ESTE | Alta | Reutilización por comercio/CUI | `sgn_h03` y `sgn_h04` comparten comercio y CUI | Respaldo inicial SQLite |
| E6-H03 — Código no consumido | Alta | Código generado y consumido en alta | `sgn_h07`: `GENERATED`, `consumed_at=NULL` | Respaldo inicial SQLite |
| E6-H04 — Canal incorrecto | Alta | Canal desde comercio (`alfa`) | `sgn_h06`: `omega` | Respaldo inicial SQLite |
| E6-H06 — CUI discordante | Alta | Datos personales desde verificación | `sgn_h05` difiere del KYC en CUI | Respaldo inicial SQLite |
| E6-H09 — Coincidencia 0.74 inferior a 0.80 | Crítica | No permitir alta bajo el umbral | `sgn_h08` histórico | Respaldo inicial SQLite |

**Nota:** los resultados históricos indican anomalías de datos, no determinan su causa. BUG-02 sí tiene reproducción manual de API y confirmación SQL del alta `sgn_887343af0d8e`.
