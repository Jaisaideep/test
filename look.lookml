we have a table in which we have below columns
datetime
resource_labels_location
resource_labels_project_id
resource_labels_cluster_name
resource_labels_node_name
CPU
memory
NodeUsgae

The datetime has the values in "2024-06-25T12:42:28" format. Now I need to group the data for each day per hour wise. Meaning the data from 10:01:00 to 11:00:00 should be aggerated by taking average of CPU,memory,NodeUsage
So my output should have date, Hour, and rest of the data from above table where date will be date(datetime) and Hour will be 11:00:00 in this aspect of aggegration. 
Hope you got the logic and implemt the same for 24 hours of data
