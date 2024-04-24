SELECT 
  DATE(t1.Timestamp) AS LogDate,
  AVG(t1.CPU_Usage) AS AVG_CPU_Usage,
  SUM(
    CASE
      WHEN t1.Application = 'CDP' THEN 0.1 * t1.CPU_Usage
      WHEN t1.Application = 'DataMarketplace' THEN 0.25 * t1.CPU_Usage
      WHEN t1.Application = 'VZOS' THEN 0.1 * t1.CPU_Usage
      WHEN t1.Application = 'RedisLabs' THEN 0.05 * t1.CPU_Usage
      WHEN t1.Application = 'ML' THEN 0.1 * t1.CPU_Usage
      WHEN t1.Application = 'SmartDQ' THEN 0.1 * t1.CPU_Usage
      WHEN t1.Application = 'MDE' THEN 0.05 * t1.CPU_Usage
      ELSE 0
    END
  ) AS AggAvg
FROM 
  `vz-it-pr-jabv-aidplt-0.AIDSRE.infra_dgs` AS t1
WHERE 
  DATE(t1.Timestamp) = '2024-04-22'
GROUP BY 
  LogDate