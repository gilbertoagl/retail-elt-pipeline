WITH ventas_reales AS (
    SELECT 
        category,
        COUNT(*) as total_productos,
        SUM(numero_votos) as votos_totales,
        AVG(calificacion) as calificacion_promedio
    FROM {{ ref('tabla_limpia') }}
    GROUP BY category
),

metas AS (
    SELECT * FROM {{ ref('metas_por_categoria') }}
)

SELECT
    v.category,
    v.votos_totales as votos_reales,
    m.meta_votos as meta_objetivo,
    CASE 
        WHEN v.votos_totales >= m.meta_votos THEN 'CUMPLIDO'
        ELSE 'FALTA'
    END as estado_meta,
    ROUND((v.votos_totales::numeric / m.meta_votos::numeric) * 100, 2) as porcentaje_cumplimiento
FROM ventas_reales v
LEFT JOIN metas m ON v.category = m.category