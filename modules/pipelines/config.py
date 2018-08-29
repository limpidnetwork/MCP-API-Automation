import os

# Postgres
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', "mcp_db_pg")
POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME', "limpid")
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', "limpid@123")
POSTGRES_DB = os.environ.get('POSTGRES_DB', "mcp")


# Blue Planet Configuration

# Path Map
PATH_MAP = {
	'active_alarms' : ('/nsa/api/v1/alarms/filter/activeAlarms', 'data'),
	'device_types' : ('/nsa/api/v1/alarms/device-types', 'data'),
	'deviceAttributes' : ('/nsa/api/v1/alarms/deviceAttributes/{params}', 'data'),
	'networkConstructs' : ('/nsi/api/networkConstructs', 'data'),
	'tpes' : ('/nsi/api/tpes', 'data'),
	'fres' : ('/nsi/api/fres', 'data'),
	'physicalLocations' : ('/nsi/api/physicalLocations', 'data'),
	'equipment' : ('/nsi/api/equipment', 'data'),
	'managementSessions' : ('/discovery/api/managementSessions', 'data'),
	'HeatDissipationReport' : ('/equipmenttopologyplanning/api/v1/HeatDissipationReport', 'sites'),
	'policyTypes' : ('/commissioning/api/v1/policyTypes/', 'data'),
	'policy' : ('/commissioning/api/v1/policy/', 'data'),
	'policyDefaults' : ('/commissioning/api/v1/policyDefaults/', 'data'),
	'equipment_v4' : ('/nsi/api/v4/equipment', 'data'),
	'relationships' : ('/bpocore/market/api/v1/relationships', 'items'),
	'resource_types' : ('/bpocore/market/api/v1/resource-types', 'items'),
	'products' : ('/bpocore/market/api/v1/products', 'items'),
	'channelmargin' : ('/perfg/api/v1/channelmargin', 'services'),
	'config_templates' : ('/pm/api/v1/configs', 'data'),
	'nodes' : ('/pm/api/v1/nodes', 'data'),
	'resource_profiles' : ('/pmprocessor/api/v1/resource_profiles', 'data'),
	# These three seems to be a POST request, we might need to provide additional params
	'services' : ('/commissiong/api/v1/services', 'data'),
	'ipsubnet' : ('/commissioning/api/v1/ipsubnet/', 'shelfIP'),
	'scripts' :  ('/commissioning/api/v1/scripts/', 'data')
}

