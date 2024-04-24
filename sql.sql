SELECT LogDate, sum(AggAvg) as Agg_CPU_Usage
FROM

(SELECT date(t1.Timestamp) as LogDate,
Application,
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
GROUP BY 1,2)

GROUP BY 1

-----------------
SELECT  
date(t1.Timestamp) as LogDate,
(
  0.1 * AVG(CASE WHEN (t1.Application = "SmartDQ") THEN t1.CPU_Usage ELSE 0 END) +
  0.05 * AVG(CASE WHEN(t1.Application = "RedisLabs") THEN t1.CPU_Usage ELSE 0 END) +
  0.1 * AVG(CASE WHEN(t1.Application = "VZOS") THEN t1.CPU_Usage ELSE 0 END) +
  0.1 * AVG(CASE WHEN(t1.Application = "ML") THEN t1.CPU_Usage ELSE 0 END) +
  0.1 * AVG(CASE WHEN(t1.Application = "CDP") THEN t1.CPU_Usage ELSE 0 END) +
  0.05 * AVG(CASE WHEN(t1.Application = "MDE") THEN t1.CPU_Usage ELSE 0 END) +
  0.25 * AVG(CASE WHEN(t1.Application = "DataMarketplace") THEN t1.CPU_Usage ELSE 0 END) 
  #0.25 * AVG(CASE WHEN(t2.Cluster = "OCP-JFXV-DGA-PROD") THEN t2.Cpu_Util_percent ELSE 0 END)
) as Agg_CPU_Usage
FROM `vz-it-pr-jabv-aidplt-0.AIDSRE.infra_dgs` as t1
where date(t1.Timestamp) = "2024-04-22"
GROUP BY 1
