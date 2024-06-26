SELECT
  DATE(datetime) AS date,
  FORMAT_TIMESTAMP('%H:00:00', TIMESTAMP_TRUNC(PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', datetime), HOUR)) AS hour,
  resource_labels_location,
  resource_labels_project_id,
  resource_labels_cluster_name,
  resource_labels_node_name,
  AVG(CPU) AS avg_CPU,
  AVG(memory) AS avg_memory,
  AVG(NodeUsage) AS avg_NodeUsage
FROM
  your_table_name
GROUP BY
  date,
  hour,
  resource_labels_location,
  resource_labels_project_id,
  resource_labels_cluster_name,
  resource_labels_node_name
ORDER BY
  date,
  hour;


No matching signature for function PARSE_TIMESTAMP for argument types: STRING, DATETIME. Supported signature: PARSE_TIMESTAMP(STRING, STRING, [STRING]) at [6:46]

select 
date(datetime) as LogDate,
FORMAT_TIMESTAMP('%H:%M:00', TIMESTAMP_TRUNC(TIMESTAMP(datetime), MINUTE)+INTERVAL 30 * (FLOOR(EXTRACT(MINUTE FROM TIMESTAMP(DATETIME))/30))MINUTE) AS hour,
resource_labels_location,resource_labels_project_id,resource_labels_cluster_name,resource_labels_node_name,avg(node_cpu_allocatable_utilization)as CPU,avg(node_memory_allocatable_utilization) as memory,avg(node_cpu_core_usage_time) as NodeUsage
from `vz-it-pr-jabv-aidplt-0.AIDSRE.domino_node_metric1`
where date(datetime) = "2024-06-25"
GROUP BY 1,2,3,4,5,6
order by 2
Invalid interval literal. Expected INTERVAL keyword to be followed by an INT64 expression or STRING literal at [3:84]
