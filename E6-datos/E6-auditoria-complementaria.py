"""Consultas complementarias E6. Solo lectura. No muestra CUI completos."""
import sqlite3
from pathlib import Path

DB = Path.home() / 'Downloads/QA-evidencias-privadas/qa-inicial.db'
if not DB.is_file():
    raise SystemExit(f'No existe el respaldo original: {DB}')
conn = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)

CHECKS = [
    ('Duplicados: IDs de las altas y tamaño del grupo', '''
        SELECT merchant_id, COUNT(*) AS cantidad, GROUP_CONCAT(id, ', ') AS signup_ids
        FROM signups GROUP BY merchant_id, cui HAVING COUNT(*) > 1
    '''),
    ('Códigos de invitación vinculados a sgn_h07', '''
        SELECT code, signup_id, merchant_id, status, created_at, consumed_at
        FROM invitation_codes WHERE signup_id='sgn_h07'
    '''),
    ('Detalles mínimos de alta sgn_h06 frente a su comercio', '''
        SELECT s.id, s.merchant_id, s.channel AS canal_alta,
               m.channel AS canal_configurado, s.kyc_check_id, s.created_at
        FROM signups s LEFT JOIN merchants m ON s.merchant_id=m.id
        WHERE s.id='sgn_h06'
    '''),
    ('Alta enlazada a verificación de otro comercio o CUI', '''
        SELECT s.id AS signup_id, s.merchant_id AS comercio_alta,
               k.merchant_id AS comercio_kyc, s.kyc_check_id
        FROM signups s JOIN kyc_checks k ON s.kyc_check_id=k.id
        WHERE s.merchant_id<>k.merchant_id OR s.cui<>k.cui
    '''),
    ('Altas con verificación no consumida', '''
        SELECT s.id, s.kyc_check_id, k.status, k.consumed_by_signup_id
        FROM signups s JOIN kyc_checks k ON s.kyc_check_id=k.id
        WHERE k.status<>'CONSUMED'
    '''),
    ('Altas creadas después del vencimiento de verificación', '''
        SELECT s.id, s.kyc_check_id, k.expires_at, s.created_at
        FROM signups s JOIN kyc_checks k ON s.kyc_check_id=k.id
        WHERE k.expires_at IS NOT NULL
          AND datetime(s.created_at)>datetime(k.expires_at)
    '''),
    ('Altas con coincidencia facial menor al umbral del comercio', '''
        SELECT s.id, s.merchant_id, k.face_match_score, m.face_match_threshold
        FROM signups s JOIN kyc_checks k ON s.kyc_check_id=k.id
        JOIN merchants m ON s.merchant_id=m.id
        WHERE m.face_match_required=1 AND k.face_match_score IS NOT NULL
          AND k.face_match_score<m.face_match_threshold
    '''),
]
try:
    for title, sql in CHECKS:
        rows = conn.execute(sql).fetchall()
        print('\n===', title, '===')
        print('Filas:', len(rows))
        for row in rows:
            print(tuple(row))
finally:
    conn.close()
