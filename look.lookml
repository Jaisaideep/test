SELECT
Date(LogTime) as LogDate,
LogTime,
CONCAT(EXTRACT(Hour FROM LogTime),":",EXTRACT(MINUTE FROM LogTime),":",EXTRACT(SECOND FROM LogTime)) as Time
FROM `vz-it-np-jabv-dev-aidplt-0.AIDSRE.SRE_DA_Prod_Reliability_Ingress_CP`
ORDER BY 2 DESC

I am trying to extract time from timestamp.. I am able to do it in this way but the column Time is ending up as a string but I need the datatype to be time so that I can filter the data accordingly
