# E2 — Estrategia de pruebas

**Estado:** estrategia consolidada con el contrato revisado. Las pruebas móviles permanecen diseñadas y no ejecutadas por ausencia de la aplicación.

**Objetivo:** determinar si HU-410 puede liberarse manteniendo seguridad, integridad e aislamiento entre comercios.

**Alcance ejecutable:** endpoints API del alta sin código, webhook simulado, transiciones de estados, validación del gate y persistencia en SQLite.

**Pruebas móviles (solo diseño):** Se contemplan pruebas de permisos de cámara, captura del DPI y selfie, interrupciones de red, segundo plano, abandono del proceso y compatibilidad entre dispositivos Android e iOS. Para ejecutarlas sería necesaria la aplicación instalada en dispositivos físicos. El ambiente recibido no incluye la aplicación móvil.

**Fuera de alcance:** validación del NIT con SAT, accesibilidad de pantallas de captura, flujo anterior con código (solo regresión crítica, según fuente).

**Riesgos prioritarios:** gate de identidad/expiración/consumo; umbral facial; aislamiento multi-tenant; idempotencia y concurrencia; webhook con firma; control de intentos; trazabilidad BD/PII.

**Técnicas:** partición equivalencia, frontera (0.80, 3 intentos, 30 min), tabla decisiones para config, transiciones, abuso de API y concurrencia.

**Datos/proveedor:** tokens y documentos ficticios del sandbox; escenarios aprobados, rechazo, revisión; separar evidencias del sprint anterior y nuevas.

**Dependencia externa:** El proveedor de identidad es necesario para validar documento, prueba de vida y coincidencia facial. En el ambiente QA se utilizará el simulador para reproducir respuestas y validar el comportamiento del backend. Esto no sustituye las pruebas de integración con el proveedor real ni la captura en dispositivos físicos. Ante fallas del proveedor, se deberá comprobar que no se permita crear un alta sin verificación aprobada.

**Criterios de entrada:** API y BD disponibles; OpenAPI revisado; fixtures identificados; reinicio controlado.

**Criterios de salida:** Los casos smoke críticos deben ejecutarse satisfactoriamente. No recomendaría liberar con defectos abiertos que permitan crear altas sin identidad aprobada, acceder a información de otro comercio, reutilizar indebidamente verificaciones o generar altas duplicadas. Los defectos de menor severidad deberán evaluarse según su impacto y contar con aceptación explícita del riesgo. Cualquier prueba no ejecutada o bloqueada debe quedar documentada antes de recomendar la liberación.