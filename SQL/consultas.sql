CREATE OR REPLACE TABLE `arctic-nectar-443501-m3.retail_sales.TABLE_FINAL` AS
SELECT * 
FROM `arctic-nectar-443501-m3.retail_sales.TABLE_RETAIL`;


SELECT * 
FROM (
    SELECT 
        'Maior Estoque' AS tipo, 
        data, 
        estoque
    FROM `arctic-nectar-443501-m3.retail_sales.view_base`
    ORDER BY estoque DESC
    LIMIT 1
) 

UNION ALL

SELECT * 
FROM (
    SELECT 
        'Menor Estoque' AS tipo, 
        data, 
        estoque
    FROM `arctic-nectar-443501-m3.retail_sales.view_base`
    ORDER BY estoque ASC
    LIMIT 1
);


SELECT 
    EXTRACT(YEAR FROM data) AS ano,
    EXTRACT(MONTH FROM data) AS mes,
    SUM(venda * preco) AS receita_total
FROM `arctic-nectar-443501-m3.retail_sales.view_base`
GROUP BY ano, mes
ORDER BY ano, mes;


SELECT 
    COUNTIF(data IS NULL) AS nulos_data,
    COUNTIF(venda IS NULL) AS nulos_venda,
    COUNTIF(estoque IS NULL) AS nulos_estoque,
    COUNTIF(preco IS NULL) AS nulos_preco
FROM `arctic-nectar-443501-m3.retail_sales.TABLE_FINAL`;


SELECT *, COUNT(*) AS count
FROM `arctic-nectar-443501-m3.retail_sales.TABLE_FINAL`
GROUP BY data, venda, estoque, preco
HAVING count > 1;


CREATE OR REPLACE VIEW `arctic-nectar-443501-m3.retail_sales.view_base` AS
SELECT * 
FROM `arctic-nectar-443501-m3.retail_sales.TABLE_FINAL`;


SELECT 
    CASE 
        WHEN preco < 1 THEN 'Baixo'
        WHEN preco BETWEEN 1 AND 1.5 THEN 'Médio'
        ELSE 'Alto'
    END AS faixa_preco,
    AVG(venda) AS volume_medio_vendas
FROM `arctic-nectar-443501-m3.retail_sales.view_base`
GROUP BY faixa_preco
ORDER BY faixa_preco;

