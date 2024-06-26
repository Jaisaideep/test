select  
A.LogDate, 
ROUND(100 - SAFE_DIVIDE(count(*), (select TotalQueries from AIDSRE.TD_ACTIVE_USERS_QUERIES_COUNT WHERE LogDate = A.LogDate)), 2)/100 as UII_Percent
from `AIDSRE.TD_UII_SQL_DETAILS` A
Group by 1

Scalar subquery produced more than one element
