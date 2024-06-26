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


SELECT 
  DATE(TIMESTAMP(datetime)) AS LogDate,
  FORMAT_TIMESTAMP('%H:%M:00', TIMESTAMP_TRUNC(TIMESTAMP(datetime), MINUTE) + INTERVAL 30 * (FLOOR(EXTRACT(MINUTE FROM TIMESTAMP(datetime)) / 30)) MINUTE) AS hour,
  resource_labels_location,
  resource_labels_project_id,
  resource_labels_cluster_name,
  resource_labels_node_name,
  AVG(node_cpu_allocatable_utilization) AS CPU,
  AVG(node_memory_allocatable_utilization) AS memory,
  AVG(node_cpu_core_usage_time) AS NodeUsage
FROM 
  `vz-it-pr-jabv-aidplt-0.AIDSRE.domino_node_metric1`
WHERE 
  DATE(TIMESTAMP(datetime)) = "2024-06-25"
GROUP BY 
  LogDate, hour, resource_labels_location, resource_labels_project_id, resource_labels_cluster_name, resource_labels_node
