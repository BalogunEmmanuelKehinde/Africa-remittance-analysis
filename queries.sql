-- Africa Remittance Analysis: Key Queries i used in 
-- Source: World Bank Remittance Prices Worldwide (2016-2025)

-- 1. Average cost by flow type
SELECT flow_type, 
       ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost,
       COUNT(*) as total_observations
FROM africa_remittances
GROUP BY flow_type
ORDER BY avg_cost DESC;

-- 2. Top 5 cheapest providers by destination country
SELECT firm_name, total_cost_pct, flow_type, source_country
FROM africa_remittances
WHERE destination_country ILIKE '%Nigeria%' 
AND total_cost_pct > 0 
ORDER BY total_cost_pct ASC
LIMIT 5;

-- 3. Bank vs MTO vs Hybrid comparison
SELECT 
    CASE 
        WHEN firm_type ILIKE '%Bank%' AND firm_type ILIKE '%Operator%' THEN 'Hybrid (Bank + MTO)'
        WHEN firm_type ILIKE '%Bank%' THEN 'Traditional Bank'
        WHEN firm_type ILIKE '%MTO%' OR firm_type ILIKE '%Operator%' THEN 'Digital/MTO'
        ELSE 'Other'
    END as simplified_type,
    flow_type,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_fee_pct,
    COUNT(*) as record_count
FROM africa_remittances
WHERE total_cost_pct > 0
GROUP BY 1, 2 
ORDER BY simplified_type ASC, flow_type ASC;

-- 4. Cost trend over time
SELECT 
    period,
    flow_type,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost
FROM africa_remittances
WHERE total_cost_pct > 0
GROUP BY period, flow_type
ORDER BY period ASC;

-- 5. Most expensive corridors
SELECT 
    source_country,
    destination_country,
    flow_type,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost,
    COUNT(*) as observations
FROM africa_remittances
WHERE total_cost_pct > 0
GROUP BY source_country, destination_country, flow_type

-- 6. Quarterly trend 2023-2025 by flow type
SELECT 
    period,
    flow_type,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost,
    COUNT(*) as observations
FROM africa_remittances
WHERE (period LIKE '2023%' OR period LIKE '2024%' OR period LIKE '2025%')
AND total_cost_pct > 0
GROUP BY period, flow_type
ORDER BY period ASC, flow_type ASC;

-- 7. Who is driving Intra-Africa costs in 2025
SELECT 
    firm_name,
    firm_type,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost,
    COUNT(*) as observations
FROM africa_remittances
WHERE flow_type = 'Intra-Africa'
AND period LIKE '2025%'
AND total_cost_pct > 0
GROUP BY firm_name, firm_type
ORDER BY avg_cost DESC
LIMIT 10;

-- 8. The smoking gun — Tanzania to Uganda provider breakdown
SELECT 
    firm_name,
    firm_type,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost
FROM africa_remittances
WHERE source_country = 'Tanzania'
AND destination_country = 'Uganda'
AND period LIKE '2025%'
AND total_cost_pct > 0
GROUP BY firm_name, firm_type
ORDER BY avg_cost DESC;

-- 9. Provider count vs avg cost per corridor (monopoly check)
SELECT 
    source_country,
    destination_country,
    COUNT(DISTINCT firm_name) as num_providers,
    ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost
FROM africa_remittances
WHERE flow_type = 'Intra-Africa'
AND period LIKE '2025%'
AND total_cost_pct > 0
GROUP BY source_country, destination_country
ORDER BY avg_cost DESC
LIMIT 10;
ORDER BY avg_cost DESC
LIMIT 10;
