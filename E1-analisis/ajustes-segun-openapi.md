# E1 — Ajustes tras comparar HU-410 con OpenAPI

Este anexo no sustituye las siete observaciones originales; corrige su interpretación donde el contrato aporta reglas más específicas.

1. **CA-08 vs OpenAPI — Intentos cancelados:** la historia dice que cada sesión es un intento, pero la descripción de `POST /v1/identity/sessions` expresa que **las canceladas no cuentan**. Esto es una contradicción verificable, no solo una pregunta sobre ventanas de 24 horas. **Pregunta al PO:** ¿la cancelación devuelve el intento al cupo y cómo se evita que un usuario cancele repetidamente para eludir el límite? **Supuesto:** para el test del cuarto intento se dejan todas las sesiones sin cancelar.
2. **CA-03 y OpenAPI — Puntaje facial:** el contrato especifica `REJECTED` con `rejectReason.code=FACE_MISMATCH` si `faceMatch.score` es menor al umbral, aunque el proveedor anuncie approved. El escenario `face_borderline=0.72` reproducido dio `APPROVED`; se documentó BUG-02.
3. **CA-07/CA-10 e idempotencia:** mismas clave y solicitud deben devolver la respuesta original; misma clave con otra solicitud devuelve HTTP `422`. Una alta existente en el mismo comercio reutiliza con HTTP `200`. El sistema no puede producir dos altas simultáneas del mismo CUI/comercio.
4. **Regla 4 — Enlaces de imágenes:** OpenAPI fija una validez de **5 minutos** para URLs firmadas y privadas. Por ello la duración dejó de ser un vacío, pero queda pendiente comprobar en ambiente si las URLs devueltas implementan firma/caducidad y si el acceso es realmente privado. No inferir acceso público solo por un fragmento `/public/` en la URL.
5. **CA-06 — Expiración:** OpenAPI espera HTTP `409` con error `VERIFICATION_EXPIRED` cuando corresponda. La precisión del instante 30:00 debe resolverse con PO; el test 31 minutos está fuera de cualquier ambigüedad del límite.
6. **CA-04 vs regla de negocio 5:** persiste contradicción sobre editabilidad de datos del DPI, cuya resolución corresponde al PO.
