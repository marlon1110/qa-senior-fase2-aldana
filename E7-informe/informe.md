# E7 — Informe de calidad HU-410

**Fecha de evaluación:** 21 de octubre de 2026 · **Recomendación:** **NO-GO**

**Alcance.** Se evaluó caja negra de API y SQLite del alta sin código: habilitación por comercio, verificación facial, vencimiento, intentos, autorización entre comercios, webhooks e idempotencia. La aplicación móvil no estaba incluida; sus casos se diseñaron, pero no se ejecutaron. Se analizaron separadamente registros históricos y pruebas nuevas.

**Resultados.** Smoke automatizado: **1 PASS / 9 FAIL** (10). Suite completa: **8 PASS / 10 FAIL** (18). Dos defectos se reprodujeron manualmente: BUG-01 (sesiones de comercios no habilitados) y BUG-02 (KYC 0.72 aprobado con alta creada). El BUG-02 también quedó demostrado en SQLite: alta `sgn_887343af0d8e`, verificación CONSUMED y código CONSUMED, pese al umbral 0.80. Se documentaron además los BUG-03 a BUG-08 con pruebas automatizadas o SQL histórico, distinguiendo el alcance de cada evidencia.

**Defectos abiertos y priorización propuesta.** Entre los ocho reportes principales: **6 críticos** (BUG-02, 03, 04, 05, 06 y 08; BUG-08 basado solo en registro histórico), **2 altos** (BUG-01 y 07). En la suite también aparecieron incumplimientos de esquema de respuesta. Severidades y prioridades sujetas a triage con el equipo.

**Riesgos residuales.** Posible alta sin cumplir controles de identidad; recepción de webhooks no autenticados; exposición de verificación de otro tenant; reintentos concurrentes inconsistentes; ausencia de comprobación con proveedor real y dispositivos físicos; anomalías históricas de integridad. En la concurrencia se constataron dos IDs devueltos, pero falta verificar persistencia de ambas filas en la Mac.

**Decisión.** **NO-GO.** Requerir corrección y regresión satisfactoria de controles de identidad, firma, aislamiento, expiración, intentos e idempotencia; validar integridad y tratamiento de registros históricos; reejecutar smoke y suite; documentar riesgo residual y obtener aprobación de Producto y Seguridad antes de liberar.

**CTO summary (five lines):**  
1. QA tested identity self-onboarding APIs and SQLite with risk-based black-box checks.  
2. The full automated suite passed 8 of 18 tests; 10 failed.  
3. A below-threshold facial match resulted in an actual persisted signup.  
4. Other blockers include unsigned webhooks, cross-tenant access and expired verification acceptance.  
5. **Recommendation: NO-GO** until critical controls are fixed and regression tests pass.
