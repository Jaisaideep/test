WITH QueriesCount AS (
  SELECT 
    LogDate, 
    TotalQueries 
  FROM 
    AIDSRE.TD_ACTIVE_USERS_QUERIES_COUNT
)
SELECT  
  A.LogDate, 
  ROUND(100 - SAFE_DIVIDE(COUNT(*), QC.TotalQueries), 2) / 100 AS UII_Percent
FROM 
  `AIDSRE.TD_UII_SQL_DETAILS` A
JOIN 
  QueriesCount QC 
ON 
  A.LogDate = QC.LogDate
GROUP BY 
  A.LogDate, QC.TotalQueries
ORDER BY 
  A.LogDate;