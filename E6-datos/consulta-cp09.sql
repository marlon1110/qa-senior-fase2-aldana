-- Ejecutar sobre la copia PRIVADA qa-pruebas-manuales.db, no sobre la inicial.
-- No divulgar ningún CUI completo, token o imagen de identidad.
SELECT s.id AS alta, s.merchant_id, s.commercial_name,
       s.kyc_check_id, k.status AS verificacion_estado,
       k.face_match_score, m.face_match_threshold,
       COUNT(c.code) AS codigos,
       GROUP_CONCAT(c.status, ', ') AS estados_codigo
FROM signups AS s
LEFT JOIN kyc_checks AS k ON s.kyc_check_id = k.id
LEFT JOIN merchants AS m ON s.merchant_id = m.id
LEFT JOIN invitation_codes AS c ON c.signup_id = s.id
WHERE s.commercial_name = 'Comercio Prueba CP09'
GROUP BY s.id, s.merchant_id, s.commercial_name,
         s.kyc_check_id, k.status, k.face_match_score,
         m.face_match_threshold;
