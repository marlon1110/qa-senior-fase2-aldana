# E6 — Validación de datos e integridad (HU-410)

**Alcance:** SQLite del ambiente QA, revisión histórica del sprint 14–15 de octubre de 2026 y comprobaciones de integridad del alta sin código.  
**Fuente de evidencia histórica:** respaldo `qa-inicial.db`, obtenido antes de las ejecuciones de QA.  
**Método:** SQL de solo lectura; sin modificar el código del servicio.  
**Separación de datos:** los resultados **H01–H09** de este informe pertenecen *exclusivamente* al respaldo original. Las pruebas manuales y la suite automatizada se reportan en otra sección; no se mezclan sus datos.  
**Privacidad:** no se publican CUI completos, base de datos, imágenes de identidad ni tokens.

## 1. Altas creadas el 15/10/2026, hora de Guatemala

**Respuesta: 2 altas.**

| Alta | Comercio | `created_at` UTC | Fecha/hora Guatemala (UTC−6) |
|---|---|---|---|
| `sgn_h08` | `M-NORTE` | `2026-10-15T14:05:00Z` | `2026-10-15 08:05:00` |
| `sgn_h09` | `M-ESTE` | `2026-10-16T00:02:00Z` | `2026-10-15 18:02:00` |

```sql
SELECT COUNT(*) AS total
FROM signups
WHERE datetime(created_at) >= '2026-10-15 06:00:00'
  AND datetime(created_at) <  '2026-10-16 06:00:00';
```

**Interpretación.** Guatemala usa UTC−6 sin cambio estacional; por ello el día 15 local comprende `[2026-10-15 06:00:00, 2026-10-16 06:00:00)` en UTC. La comparación usa un inicio inclusivo y un final exclusivo. El registro `sgn_h09` se cuenta porque a pesar de tener fecha UTC del día 16 corresponde al día 15 en Guatemala. Los resultados corresponden a la fecha de **creación** de las altas, no a la de las verificaciones.

## 2. Validación de integridad — Sprint anterior

### H01. Altas repetidas para el mismo comercio y CUI

```sql
SELECT merchant_id, COUNT(*) AS cantidad, GROUP_CONCAT(id, ', ') AS altas
FROM signups
GROUP BY merchant_id, cui
HAVING COUNT(*) > 1;
```

**Resultado:** 1 grupo duplicado, `M-ESTE`, 2 altas: `sgn_h03` y `sgn_h04`.  
**Interpretación:** contradice la reutilización del alta para el mismo DPI dentro del comercio (CA-07). La consulta no expone el CUI.

### H02. Altas sin verificación relacionada

```sql
SELECT s.id, s.merchant_id
FROM signups AS s
LEFT JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE k.id IS NULL;
```

**Resultado:** 0 filas.  
**Interpretación:** no se hallaron referencias a identificadores de verificación inexistentes. No implica que las verificaciones sean válidas o estén aprobadas.

### H03. Altas sin invitación en estado CONSUMED

```sql
SELECT s.id, s.merchant_id
FROM signups AS s
WHERE NOT EXISTS (
  SELECT 1 FROM invitation_codes AS c
  WHERE c.signup_id = s.id AND c.status = 'CONSUMED'
);
```

**Resultado:** `sgn_h07` (`M-NORTE`). Consulta complementaria a `invitation_codes` encontró `INV-5T6Y7G` con estado **`GENERATED`**, `consumed_at = NULL`.  
**Interpretación:** existe código, pero no se consumió automáticamente; incumple CA-05.

### H04. Canal comercial distinto al configurado

```sql
SELECT s.id, s.merchant_id, s.channel AS canal_alta,
       m.channel AS canal_comercio
FROM signups AS s JOIN merchants AS m ON s.merchant_id = m.id
WHERE s.channel <> m.channel;
```

**Resultado:** `sgn_h06` de `M-ESTE`, canal del alta `omega`, canal configurado `alfa`; asociado a `kyc_h05`.  
**Interpretación:** incumple el requisito de resolver el canal en el servidor desde la configuración del comercio (regla de negocio 3). Se desconoce el origen del valor erróneo.

### H05. Verificaciones marcadas CONSUMED con referencia de alta inexistente

```sql
SELECT k.id, k.merchant_id
FROM kyc_checks AS k
LEFT JOIN signups AS s ON k.consumed_by_signup_id = s.id
WHERE k.status = 'CONSUMED'
  AND (k.consumed_by_signup_id IS NULL OR s.id IS NULL);
```

**Resultado:** 0 filas.  
**Interpretación:** no hay referencias a altas ausentes para verificaciones `CONSUMED`, conforme al alcance de la consulta; esto no comprueba CUI, comercio ni validez de aprobación.

### H06. Inconsistencia entre la identidad del alta y su verificación

```sql
SELECT s.id AS alta, s.merchant_id AS comercio_alta,
       k.merchant_id AS comercio_verificacion, s.kyc_check_id,
       CASE WHEN s.cui <> k.cui THEN 'DIFERENTE' ELSE 'IGUAL' END AS cui_coincide
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE s.merchant_id <> k.merchant_id OR s.cui <> k.cui;
```

**Resultado:** `sgn_h05`, comercio de alta `M-NORTE`, comercio de verificación `M-NORTE`, verificación `kyc_h04`.  
**Interpretación:** ambos comercios coinciden; por la condición del filtro `OR`, la diferencia corresponde al **CUI** de la persona. No se muestran los valores. Incumple la obligación de tomar los datos personales de la verificación aprobada.

### H07. Alta enlazada a verificación cuyo estado no es CONSUMED

```sql
SELECT s.id, s.kyc_check_id, k.status, k.consumed_by_signup_id
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE k.status <> 'CONSUMED';
```

**Resultado:** alta `sgn_h02` asociada con `kyc_h02`, cuyo estado es **`REJECTED`**, pese a que `consumed_by_signup_id = 'sgn_h02'`.  
**Interpretación:** inconsistencia crítica de estado de identidad: existe alta relacionada con verificación rechazada (CA-06). No se ha establecido cómo se originó históricamente.

### H08. Altas creadas después de la expiración de la verificación

```sql
SELECT s.id, s.kyc_check_id, k.expires_at, s.created_at
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE k.expires_at IS NOT NULL
  AND datetime(s.created_at) > datetime(k.expires_at);
```

**Resultado:** 0 filas.  
**Interpretación:** no se detectaron altas históricas posteriores al vencimiento en los registros examinados. **No demuestra** que el backend controle correctamente el vencimiento: la prueba automatizada E5 sí obtuvo un `201` después de adelantar 31 minutos el reloj.

### H09. Altas con coincidencia facial inferior al umbral

```sql
SELECT s.id, s.merchant_id, k.face_match_score, m.face_match_threshold
FROM signups AS s
JOIN kyc_checks AS k ON s.kyc_check_id = k.id
JOIN merchants AS m ON s.merchant_id = m.id
WHERE m.face_match_required = 1
  AND k.face_match_score IS NOT NULL
  AND k.face_match_score < m.face_match_threshold;
```

**Resultado:** `sgn_h08`, `M-NORTE`, puntaje **0.74** frente al umbral **0.80**.  
**Interpretación:** incumple CA-03; coincide con la clase de problema reproducida manualmente en CP09 (0.72), aunque corresponde a un registro distinto del sprint anterior.

## 3. Pruebas ejecutadas por QA (separadas del histórico)

**Origen:** respaldo privado `qa-pruebas-manuales.db` creado después de ejecutar la prueba CP09 y antes de reiniciar para automatización. Comprobación realizada con `E6-verificar-manuales.py` en modo solo lectura. Este origen NO se mezcla con `qa-inicial.db`.

### P01 — Persistencia de alta creada con coincidencia facial insuficiente (CP09 / BUG-02)

```sql
SELECT s.id AS signup_id, s.merchant_id, s.commercial_name,
       s.kyc_check_id, k.status AS kyc_status,
       k.face_match_score, m.face_match_threshold,
       COUNT(c.code) AS cantidad_codigos,
       GROUP_CONCAT(c.status, ', ') AS estados_codigos
FROM signups s
LEFT JOIN kyc_checks k ON s.kyc_check_id = k.id
LEFT JOIN merchants m ON s.merchant_id = m.id
LEFT JOIN invitation_codes c ON c.signup_id = s.id
WHERE s.commercial_name = 'Comercio Prueba CP09'
GROUP BY s.id, s.merchant_id, s.commercial_name, s.kyc_check_id,
         k.status, k.face_match_score, m.face_match_threshold;
```

**Resultado ejecutado:** 1 alta, `sgn_887343af0d8e`, en `M-NORTE`, enlazada a `kyc_62d15c1663cd`. Verificación `CONSUMED`, `face_match_score=0.72`, umbral comercial `0.80`, **1** código en estado `CONSUMED`.

**Interpretación:** quedó persistida una cuenta cuya coincidencia facial estaba por debajo del umbral requerido. Corrobora la prueba API CP09, que anteriormente había obtenido `APPROVED` y `201 Created`. El resultado demuestra persistencia real del defecto, no solamente respuesta errónea del endpoint. Fuente ejecutada: `e6-manuales.txt` (copia privada); publicar un extracto sin tokens ni CUI completos si se requiere evidencia.

### P02 — Concurrencia / idempotencia: límite de lo comprobado

La suite E5 devolvió **dos `signupId` diferentes** ante solicitudes simultáneas con el mismo `Verification-Id` y `Idempotency-Key`. Esta ejecución confirma incumplimiento de idempotencia en la respuesta. Para afirmar cuántas filas se **persistieron** en ese caso debe hacerse otra comprobación SQL justo después de reproducir concurrencia, ya que el fixture de la suite reinicia la base entre pruebas. No mezclar los identificadores de esa ejecución con los del respaldo manual CP09.

La ejecución automatizada E5 incluyó 18 pruebas: 8 `PASSED` y 10 `FAILED` (1 advertencia TLS ajena a estos fallos en las solicitudes HTTP locales). El smoke incluyó 10: 1 `PASSED`, 9 `FAILED`.

## 4. Riesgos y recomendación

Los datos iniciales revelan duplicados por comercio/CUI, un código sin consumir, canal incorrecto, discordancia del CUI con la verificación, alta relacionada con un KYC rechazado y alta con puntaje facial insuficiente. Esta información amerita investigación y reparación de datos, además de controles preventivos.

**Recomendación preliminar: No-Go**, corroborada sobre todo por defectos funcionales reproducidos contra la API (alta aprobada con puntaje facial de 0.72, alta posterior a vencimiento, exposición intercomercio y firma de webhook no rechazada). La decisión final se formaliza en E7 e incluye el estado de los defectos y riesgos residuales.

## 5. Evidencia y limitaciones

- `QA-evidencias-privadas/qa-inicial.db`: copia del estado original (**privada; no publicar**).
- `e6-altas-15-octubre.txt`, `e6-integridad-historica.txt`, `e6-complementaria.txt`: salidas de SQL ejecutadas.
- `E6-consultas-reproducibles.sql`: SQL sin credenciales ni datos personales, incluido con la entrega.
- `E6-verificar-manuales.py`: consulta read-only ejecutada sobre el respaldo manual, con salida `e6-manuales.txt`.
- Las consultas demuestran anomalías observadas, **no atribuyen causas** ni evalúan el código fuente (fuera del alcance).
