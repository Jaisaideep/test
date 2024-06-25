select queuedTime from `vz-it-pr-jabv-aidplt-0.AIDSRE.SRE_ML_Prod_GCPDomino_Ingress_API`
where date(queuedTime) = "2024-06-25"
GROUP BY 1
having count(queuedTime) >1 
order by 1 DESC
