"""E6: inspecciona copia privada de DB tras pruebas manuales, sin modificarla ni exponer CUI."""
import sqlite3
from pathlib import Path

DB = Path.home() / 'Downloads/QA-evidencias-privadas/qa-pruebas-manuales.db'
if not DB.exists():
    raise SystemExit(f'No se encontró: {DB}')

connection = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
try:
    query = '''
    SELECT s.id, s.merchant_id, s.commercial_name,
           s.kyc_check_id, k.status AS estado_kyc,
           k.face_match_score, m.face_match_threshold,
           COUNT(c.code) AS cantidad_codigos,
           GROUP_CONCAT(c.status, ', ') AS estados_codigos
    FROM signups AS s
    LEFT JOIN kyc_checks AS k ON s.kyc_check_id=k.id
    LEFT JOIN merchants AS m ON s.merchant_id=m.id
    LEFT JOIN invitation_codes AS c ON c.signup_id=s.id
    WHERE s.commercial_name='Comercio Prueba CP09'
    GROUP BY s.id, s.merchant_id, s.commercial_name,
             s.kyc_check_id, k.status, k.face_match_score,
             m.face_match_threshold
    ORDER BY s.id
    '''
    rows = connection.execute(query).fetchall()
    print('=== Registros CP09 del respaldo de pruebas MANUALES ===')
    print('Cantidad de altas CP09:', len(rows))
    for row in rows:
        print(row)
    if not rows:
        print('Sin coincidencias; revisar cuándo se tomó el respaldo respecto del CP09.')
finally:
    connection.close()
