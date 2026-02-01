-- Este test falla si encuentra precios menores o iguales a cero
SELECT
    id,
    price
FROM {{ ref('tabla_limpia') }}
WHERE price <= 0