WITH source_data AS (
    SELECT * FROM public.raw_products
)

-- Limpieza de datos
SELECT
    id,
    title,
    category,
    price,
    CAST(rating::json->>'rate' AS DECIMAL(3,1)) as calificacion,
    CAST(rating::json->>'count' AS INTEGER) as numero_votos,
    ingestion_date
FROM source_data