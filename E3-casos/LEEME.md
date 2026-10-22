# E3 — Matriz de 24 casos y estado de ejecución

Abrir `matriz-preliminar.csv` en Numbers, Excel o editor CSV. La matriz contiene 24 casos; la columna `Resultado REAL` diferencia **FAIL**, **PASS API**, **PARCIAL** y **NO EJECUTADO**.

- **PARCIAL:** la suite ejercitó una parte comprobable, pero no todos los pasos del caso matriz.
- **NO EJECUTADO:** no hay prueba completa que permita atribuir un resultado. En particular, las pruebas móviles no se ejecutaron porque no se proporcionó aplicación.
- **FAIL:** resultado demostrado por curl/pytest y/o SQLite, referenciado en `Evidencia`.

Las 18 pruebas de `pytest` **no equivalen** a 18 filas de la matriz: algunas son parámetros y otras no corresponden uno-a-uno. No sumar los estados de E3 como si fueran el resultado de E5.
