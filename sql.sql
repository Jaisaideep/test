SELECT date(t1.Timestamp) as LogDate,
#Application,
#avg(CPU_Usage) as AVG_CPU_Usge,
(CASE
   WHEN t1.Application = 'CDP' THEN 0.1*(avg(t1.CPU_Usage))
   WHEN t1.Application = 'DataMarketplace' THEN 0.25*(avg(t1.CPU_Usage))
   WHEN t1.Application = 'VZOS' THEN 0.1*(avg(t1.CPU_Usage))
   WHEN t1.Application = 'RedisLabs' THEN 0.05 *(avg(t1.CPU_Usage))
   WHEN t1.Application = 'ML' THEN 0.1*(avg(t1.CPU_Usage))
   WHEN t1.Application = 'SmartDQ' THEN 0.1*(avg(t1.CPU_Usage))
   WHEN t1.Application = 'MDE' THEN 0.05*(avg(t1.CPU_Usage))
  ELSE 0
END) AS AggAvg
FROM `vz-it-pr-jabv-aidplt-0.AIDSRE.infra_dgs` as t1
where date(t1.Timestamp) = '2024-04-22'
GROUP BY 1

SELECT list expression references t1.Application which is neither grouped nor aggregated at [8:9]
