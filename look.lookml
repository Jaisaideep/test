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