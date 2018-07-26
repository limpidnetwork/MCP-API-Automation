drop table if exists alarms;
create table alarms(
	`id` varchar(256),
	`type` varchar(256),
	`attributes_id` varchar(256),
    `attributes_node_id` varchar(256),
    `attributes_node_type` varchar(256),
    `attributes_resource` varchar(256),
    `attributes_native_condition_type` varchar(256),
    `attributes_condition_severity` varchar(256),
    `attributes_manual_clearable` varchar(256),
    `attributes_additional_text` varchar(256),
    `attributes_first_raise_time` timestamp,
    `attributes_last_raise_time` timestamp,
    `attributes_number_of_occurrences` varchar(256),
    `attributes_acknowledge_state` varchar(256),
    `attributes_device_name` varchar(256),
    `attributes_ip_address` varchar(256),
    `attributes_mac_address` varchar(256)
);

