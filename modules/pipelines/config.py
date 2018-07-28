
# Blue Planet Configuration

# Path Map

PATH_MAP = {
	'active_alarms' : '/nsa/api/v1/alarms/filter/activeAlarms',
	'device_types' : '/nsa/api/v1/alarms/device-types'
}


# Column Mapping for data transformation and data storage
COLUMN_MAP = {
	'active_alarms' : {
		'id' : ['id'],
	 	'type' : ['type'],
	 	'attributes_id' : ['attributes', 'id'],
	 	'attributes_node_id' : ['attributes', 'node-id'],
	 	'attributes_node_type' : ['attributes', 'node-type'],
	 	'attributes_resource' : ['attributes', 'resource'],
	 	'attributes_native_condition_type' : ['attributes', 'native-condition-type'],
	 	'attributes_condition_severity' : ['attributes', 'condition-severity'],
	 	'attributes_manual_clearable' : ['attributes', 'manual-clearable'],
	 	'attributes_additional_text' : ['attributes', 'additional-text'],
	 	'attributes_first_raise_time' : ['attributes', 'first-raise-time'],
	 	'attributes_last_raise_time' : ['attributes', 'last-raise-time'],
	 	'attributes_number_of_occurrences' : ['attributes', 'number-of-occurrences'],
	 	'attributes_acknowledge_state' : ['attributes', 'acknowledge-state'],
	 	'attributes_device_name' : ['attributes', 'device-name'],
	 	'attributes_ip_address' : ['attributes', 'ip-address'],
	 	'attributes_mac_address' : ['attributes', 'mac-address'],
	},
	'device_types' : {
		'id' : ['id'],
		'type' : ['type'],
		'attributes_id' : ['attributes', 'id'],
		'attributes_value' : ['attributes', 'value']
	}
}

