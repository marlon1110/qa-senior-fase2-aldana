-- HU-410 / E6 — Consultas reproducibles sobre respaldo ORIGINAL de SQLite
-- Abrir qa-inicial.db en modo de SOLO LECTURA (no subir la base al repositorio).
-- No muestran ningún CUI completo.

-- 01. Altas del 15 oct 2026, hora Guatemala (UTC-06:00)
SELECT COUNT(*) AS total_altas_locales
FROM signups WHERE datetime(created_at) >= '2026-10-15 06:00:00'
  AND datetime(created_at) < '2026-10-16 06:00:00';

-- 01b. Detalle de altas locales
SELECT id, merchant_id, created_at AS utc,
       datetime(created_at, '-6 hours') AS guatemala
FROM signups WHERE datetime(created_at) >= '2026-10-15 06:00:00'
  AND datetime(created_at) < '2026-10-16 06:00:00'
ORDER BY created_at;

-- H01. Mismo comercio/CUI con múltiples altas
SELECT merchant_id, COUNT(*) AS cantidad, GROUP_CONCAT(id, ', ') AS altas
FROM signups GROUP BY merchant_id, cui HAVING COUNT(*) > 1;

-- H02. Alta sin verificación relacionada
SELECT s.id, s.merchant_id FROM signups AS s
LEFT JOIN kyc_checks AS k ON s.kyc_check_id = k.id WHERE k.id IS NULL;

-- H03. Alta sin invitación CONSUMED
SELECT s.id, s.merchant_id FROM signups AS s
WHERE NOT EXISTS(SELECT 1 FROM invitation_codes AS c
                 WHERE c.signup_id = s.id AND c.status = 'CONSUMED');

-- H03b. Estado del código histórico puntual
SELECT code, signup_id, merchant_id, status, created_at, consumed_at
FROM invitation_codes WHERE signup_id = 'sgn_h07';

-- H04. Canal comercial discordante
SELECT s.id, s.merchant_id, s.channel AS canal_alta, m.channel AS canal_comercio
FROM signups AS s JOIN merchants AS m ON s.merchant_id = m.id
WHERE s.channel <> m.channel;

-- H05. Verificación CONSUMED sin referencia válida a un alta
SELECT k.id, k.merchant_id FROM kyc_checks AS k
LEFT JOIN signups AS s ON k.consumed_by_signup_id = s.id
WHERE k.status = 'CONSUMED'
  AND (k.consumed_by_signup_id IS NULL OR s.id IS NULL);

-- H06. Discordancia comercio/CUI entre alta y KYC; no expone el CUI
SELECT s.id AS alta, s.merchant_id AS comercio_alta,
       k.merchant_id AS comercio_kyc, s.kyc_check_id,
       CASE WHEN s.cui <> k.cui THEN 'DIFERENTE' ELSE 'IGUAL' END AS comparacion_cui
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE s.merchant_id <> k.merchant_id OR s.cui <> k.cui;

-- H07. Alta asociada a verificación no CONSUMED
SELECT s.id, s.kyc_check_id, k.status, k.consumed_by_signup_id
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE k.status <> 'CONSUMED';

-- H08. Alta posterior al vencimiento de su KYC
SELECT s.id, s.kyc_check_id, k.expires_at, s.created_at
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
WHERE k.expires_at IS NOT NULL
  AND datetime(s.created_at) > datetime(k.expires_at);

-- H09. Alta con puntaje facial debajo de mínimo comercial
SELECT s.id, s.merchant_id, k.face_match_score, m.face_match_threshold
FROM signups AS s JOIN kyc_checks AS k ON s.kyc_check_id = k.id
JOIN merchants AS m ON s.merchant_id = m.id
WHERE m.face_match_required = 1 AND k.face_match_score IS NOT NULL
  AND k.face_match_score < m.face_match_threshold;
