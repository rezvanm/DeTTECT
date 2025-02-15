import re

APP_NAME = 'DeTT&CT'
APP_DESC = 'Detect Tactics, Techniques & Combat Threats'
VERSION = '1.4.4'

EXPIRE_TIME = 60 * 60 * 24

# MITRE ATT&CK data types for custom schema and STIX
DATA_TYPE_CUSTOM_TECH_BY_GROUP = 'mitre_techniques_used_by_group'
DATA_TYPE_CUSTOM_TECH_BY_SOFTWARE = 'mitre_techniques_used_by_software'
DATA_TYPE_CUSTOM_SOFTWARE_BY_GROUP = 'mitre_software_used_by_group'
DATA_TYPE_STIX_ALL_TECH = 'mitre_all_techniques'
DATA_TYPE_STIX_ALL_TECH_ENTERPRISE = 'mitre_all_techniques_enterprise'
DATA_TYPE_STIX_ALL_GROUPS = 'mitre_all_groups'
DATA_TYPE_STIX_ALL_SOFTWARE = 'mitre_all_software'
DATA_TYPE_STIX_ALL_RELATIONSHIPS = 'mitre_all_relationships'
DATA_TYPE_STIX_ALL_ENTERPRISE_MITIGATIONS = 'mitre_all_mitigations_enterprise'
DATA_TYPE_STIX_ALL_MOBILE_MITIGATIONS = 'mitre_all_mitigations_mobile'

# Group colors
COLOR_GROUP_OVERLAY_MATCH = '#f9a825'            # orange
COLOR_GROUP_OVERLAY_NO_MATCH = '#ffee58'         # yellow
COLOR_SOFTWARE = '#0d47a1 '                      # dark blue
COLOR_GROUP_AND_SOFTWARE = '#64b5f6 '            # light blue
COLOR_GRADIENT_DISABLE = '#ffffff'               # white
COLOR_GRADIENT_MIN = '#ffcece'                   # light red
COLOR_GRADIENT_MAX = '#ff0000'                   # red
COLOR_TACTIC_ROW_BACKGRND = '#dddddd'            # light grey
COLOR_GROUP_OVERLAY_ONLY_DETECTION = '#8BC34A'   # green
COLOR_GROUP_OVERLAY_ONLY_VISIBILITY = '#1976D2'  # blue

# data source colors (purple range)
COLOR_DS_25p = '#E1BEE7'
COLOR_DS_50p = '#CE93D8'
COLOR_DS_75p = '#AB47BC'
COLOR_DS_99p = '#7B1FA2'
COLOR_DS_100p = '#4A148C'

# data source colors HAPPY (green range)
COLOR_DS_25p_HAPPY = '#DCEDC8'
COLOR_DS_50p_HAPPY = '#AED581'
COLOR_DS_75p_HAPPY = '#8BC34A'
COLOR_DS_99p_HAPPY = '#689F38'
COLOR_DS_100p_HAPPY = '#33691E'

# Detection colors (green range)
COLOR_D_0 = '#9C27B0'  # Purple: Forensics/Context
COLOR_D_1 = '#DCEDC8'
COLOR_D_2 = '#AED581'
COLOR_D_3 = '#8BC34A'
COLOR_D_4 = '#689F38'
COLOR_D_5 = '#33691E'

# Visibility colors (blue range)
COLOR_V_1 = '#BBDEFB'
COLOR_V_2 = '#64B5F6'
COLOR_V_3 = '#1976D2'
COLOR_V_4 = '#0D47A1'

# Orange overlay colors
COLOR_O_0 = '#FFECB7'
COLOR_O_1 = '#FFE07A'
COLOR_O_2 = '#FFCA28'
COLOR_O_3 = '#FFAE00'
COLOR_O_4 = '#FF8F00'
COLOR_O_5 = '#FF6F00'

COLOR_WHITE = '#FFFFFF'

# Detection and visibility overlay color:
COLOR_OVERLAY_VISIBILITY = COLOR_V_3
COLOR_OVERLAY_DETECTION = COLOR_D_3
COLOR_OVERLAY_BOTH = COLOR_GROUP_OVERLAY_MATCH

# Overlay types as used within the group functionality
OVERLAY_TYPE_GROUP = 'group'
OVERLAY_TYPE_VISIBILITY = 'visibility'
OVERLAY_TYPE_DETECTION = 'detection'

FILE_TYPE_DATA_SOURCE_ADMINISTRATION = 'data-source-administration'
FILE_TYPE_TECHNIQUE_ADMINISTRATION = 'technique-administration'
FILE_TYPE_GROUP_ADMINISTRATION = 'group-administration'

# YAML administration file versions
FILE_TYPE_DATA_SOURCE_ADMINISTRATION_VERSION = 1.0
FILE_TYPE_TECHNIQUE_ADMINISTRATION_VERSION = 1.2
FILE_TYPE_GROUP_ADMINISTRATION_VERSION = 1.0

# YAML file upgrade text
FILE_TYPE_TECHNIQUE_ADMINISTRATION_UPGRADE_TEXT = {
    1.1: "   * Adding new key 'technique_name' containing the ATT&CK technique name.\n"
         "   * Adding new key 'applicable_to' for both detection and visibility. Default value is ['all'].",
    1.2: "   * Detection: removing the key-value pair 'date_registered'.\n"
         "     You will be asked if you still want to keep this key-value pair even though DeTT&CT no longer makes use of it.\n"
         "   * Detection: the key-value pair 'date_implemented' will be renamed to 'date'.\n"
         "   * Visibility: adding a new key-value pair 'date'. You will be asked on what date to fill in for the visibility scores already present.\n"
         "   * Detection and visibility: the key-value pairs 'score' and 'date' are moved into a 'score_logbook'.\n"
         "     The primary purpose of doing this is to allow you to keep track of changes in the score."}

# visibility update questions and answers
V_UPDATE_Q_ALL_MANUAL = 'For all most recent visibility score objects that are eligible for an update, the key-value pair \'auto-generated\' is set to \'false\' or is not present.\n' \
                        'This implies that these scores are manually assigned. How do you want to proceed?:'
V_UPDATE_Q_ALL_AUTO = 'For all most recent visibility score objects that are eligible for an update, the key-value pair \'auto-generated\' is set to \'true\'. \n' \
                      'This implies that these scores are auto-generated. How do you want to proceed?:'
V_UPDATE_Q_MIXED = 'You have visibility scores that are eligible for an update, which are manually assigned and which are calculated based on the nr. of data sources (i.e. auto-generated = true)\n' \
                   'How do you want to proceed?'
V_UPDATE_ANSWER_1 = 'Update all visibility scores that have changed.'
V_UPDATE_ANSWER_2 = 'Decide per visibility score, that has changed if you want to update or not.\n' \
                    'Both the current and new visibility score will be printed.'
V_UPDATE_ANSWER_3 = 'Only auto-update the visibility scores, that have changed, which have \'auto-generated = true\''
V_UPDATE_ANSWER_4 = '- Auto-update the visibility scores, that have changed, which have \'auto-generated = true\'.\n' \
                    '- And decide per manually assigned visibility score, that has changed, if you want to update or not.\n' \
                    '  Both the current and new visibility score will be printed.'
V_UPDATE_ANSWER_CANCEL = 'Cancel.'

# update actions for visibility scores
V_UPDATE_ACTION_AUTO = 'auto update'
V_UPDATE_ACTION_DIFF = 'the user decides to update or not'

# YAML regex
REGEX_YAML_VERSION_10 = re.compile(r'^\s*version:\s+1\.0\s*$', re.IGNORECASE)
REGEX_YAML_TECHNIQUE_ID = re.compile(r'^-\s+technique_id:\s+T\d{4}(\.\d{3}|)\s*$', re.IGNORECASE)
REGEX_YAML_TECHNIQUE_ID_FORMAT = re.compile(r'T\d{4}(\.\d{3}|)', re.IGNORECASE)
REGEX_YAML_DETECTION = re.compile(r'^\s+detection:\s*$', re.IGNORECASE)
REGEX_YAML_VISIBILITY = re.compile(r'^\s+visibility:\s*$', re.IGNORECASE)
REGEX_YAML_INDENT_CHARS = re.compile(r'(^[\s-]+).*', re.IGNORECASE)
REGEX_YAML_VALID_DATE = re.compile(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', re.IGNORECASE)
REGEX_YAML_DATE = re.compile(r'^[\s-]+date:.*$', re.IGNORECASE)
REGEX_YAML_TECHNIQUE_ID_GROUP = re.compile(r'^-\s+technique_id:\s+(T\d{4})\s*$', re.IGNORECASE)

# YAML objects
YAML_OBJ_VISIBILITY = {'applicable_to': ['all'],
                       'comment': '',
                       'score_logbook':
                           [
                               {'date': None,
                                'score': 0,
                                'comment': '',
                                'auto_generated': True}
                           ]
                       }

YAML_OBJ_DETECTION = {'applicable_to': ['all'],
                      'location': [''],
                      'comment': '',
                      'score_logbook':
                          [
                              {'date': None,
                               'score': -1,
                               'comment': ''}
                      ]}

YAML_OBJ_TECHNIQUE = {'technique_id': '',
                      'technique_name': '',
                      'detection': YAML_OBJ_DETECTION,
                      'visibility': YAML_OBJ_VISIBILITY}

YAML_OBJ_DATA_SOURCE = {'data_source_name': '',
                        'date_registered': None,
                        'date_connected': None,
                        'products': [''],
                        'available_for_data_analytics': False,
                        'comment': '',
                        'data_quality': {
                            'device_completeness': 0,
                            'data_field_completeness': 0,
                            'timeliness': 0,
                            'consistency': 0,
                            'retention': 0}}

# Interactive menu
MENU_NAME_DATA_SOURCE_MAPPING = 'Data source mapping'
MENU_NAME_VISIBILITY_MAPPING = 'Visibility coverage mapping'
MENU_NAME_DETECTION_COVERAGE_MAPPING = 'Detection coverage mapping'
MENU_NAME_THREAT_ACTOR_GROUP_MAPPING = 'Threat actor group mapping'

# EQL
EQL_INVALID_RESULT_DS = '[!] Invalid data source administration content. Check your EQL query to return data_sources object(s):'
EQL_INVALID_RESULT_TECH = '[!] Invalid technique administration content. Check your EQL query to return '

# Health text
HEALTH_ERROR_TXT = '[!] The below YAML file contains possible errors. It\'s recommended to check via the ' \
                   '\'--health\' argument or using the option in the interactive menu: \n    - '

PLATFORMS = {'pre': 'PRE', 'windows': 'Windows', 'macos': 'macOS', 'linux': 'Linux', 'office 365': 'Office 365',
             'azure ad': 'Azure AD', 'google workspace': 'Google Workspace', 'iaas': 'IaaS', 'saas': 'SaaS',
             'network': 'Network', 'containers': 'Containers'}

DATA_SOURCES = {
                'PRE': ['Malware Metadata', 'Malware Content', 'Social Media', 'Response Metadata', 'Response Content', 'Certificate Registration', 'Passive DNS', 'Active DNS', 'Domain Registration'],

                'Windows': ['Firmware Modification', 'User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Scheduled Job Metadata', 'Scheduled Job Creation', 'Scheduled Job Modification', 'WMI Creation', 'Web Credential Creation', 'Web Credential Usage', 'Process Metadata', 'Process Creation', 'Process Termination', 'Process Modification', 'Process Access', 'OS API Execution', 'Module Load', 'Script Execution', 'Host Status', 'Application Log Content', 'Drive Creation', 'Drive Modification', 'Drive Access', 'Command Execution', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Service Metadata', 'Service Creation', 'Service Modification', 'File Metadata', 'File Creation', 'File Deletion', 'File Access', 'File Modification', 'Named Pipe Metadata', 'Windows Registry Key Creation', 'Windows Registry Key Deletion', 'Windows Registry Key Modification', 'Windows Registry Key Access', 'Active Directory Object Creation', 'Active Directory Object Deletion', 'Active Directory Object Modification', 'Active Directory Credential Request', 'Active Directory Object Access', 'Driver Metadata', 'Driver Load', 'Logon Session Metadata', 'Logon Session Creation', 'Network Traffic Flow', 'Network Traffic Content', 'Network Connection Creation', 'Network Share Access', 'Volume Creation', 'Volume Modification', 'Volume Deletion', 'Volume Metadata', 'Volume Enumeration', 'Group Metadata', 'Group Enumeration', 'Group Modification'],

                'macOS': ['Firmware Modification', 'User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Scheduled Job Metadata', 'Scheduled Job Creation', 'Scheduled Job Modification', 'Web Credential Creation', 'Web Credential Usage', 'Kernel Module Load', 'Process Metadata', 'Process Creation', 'Process Termination', 'Process Modification', 'Process Access', 'OS API Execution', 'Module Load', 'Host Status', 'Application Log Content', 'Drive Creation', 'Drive Modification', 'Drive Access', 'Command Execution', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Service Metadata', 'Service Creation', 'Service Modification', 'File Metadata', 'File Creation', 'File Deletion', 'File Access', 'File Modification', 'Named Pipe Metadata', 'Driver Metadata', 'Driver Load', 'Logon Session Metadata', 'Logon Session Creation', 'Network Traffic Flow', 'Network Traffic Content', 'Network Connection Creation', 'Network Share Access', 'Volume Creation', 'Volume Modification', 'Volume Deletion', 'Volume Metadata', 'Volume Enumeration'],

                'Linux': ['Firmware Modification', 'User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Scheduled Job Metadata', 'Scheduled Job Creation', 'Scheduled Job Modification', 'Web Credential Creation', 'Web Credential Usage', 'Kernel Module Load', 'Process Metadata', 'Process Creation', 'Process Termination', 'Process Modification', 'Process Access', 'OS API Execution', 'Module Load', 'Host Status', 'Application Log Content', 'Drive Creation', 'Drive Modification', 'Drive Access', 'Command Execution', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Service Metadata', 'Service Creation', 'Service Modification', 'File Metadata', 'File Creation', 'File Deletion', 'File Access', 'File Modification', 'Named Pipe Metadata', 'Driver Metadata', 'Driver Load', 'Logon Session Metadata', 'Logon Session Creation', 'Network Traffic Flow', 'Network Traffic Content', 'Network Connection Creation', 'Network Share Access', 'Volume Creation', 'Volume Modification', 'Volume Deletion', 'Volume Metadata', 'Volume Enumeration'],

                'Office 365': ['User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Web Credential Creation', 'Web Credential Usage', 'Application Log Content', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Cloud Service Metadata', 'Cloud Service Disable', 'Cloud Service Enumeration', 'Cloud Service Modification', 'Logon Session Metadata', 'Logon Session Creation', 'Group Metadata', 'Group Enumeration', 'Group Modification'],

                'Azure AD': ['User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Web Credential Creation', 'Web Credential Usage', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Cloud Service Metadata', 'Cloud Service Disable', 'Cloud Service Enumeration', 'Cloud Service Modification', 'Active Directory Object Creation', 'Active Directory Object Deletion', 'Active Directory Object Modification', 'Active Directory Credential Request', 'Active Directory Object Access', 'Logon Session Metadata', 'Logon Session Creation', 'Group Metadata', 'Group Enumeration', 'Group Modification'],

                'Google Workspace': ['User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Web Credential Creation', 'Web Credential Usage', 'Application Log Content', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Cloud Service Metadata', 'Cloud Service Disable', 'Cloud Service Enumeration', 'Cloud Service Modification', 'Logon Session Metadata', 'Logon Session Creation', 'Group Metadata', 'Group Enumeration', 'Group Modification'],

                'IaaS': ['User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Image Creation', 'Image Modification', 'Image Deletion', 'Image Metadata', 'Cloud Storage Creation', 'Cloud Storage Modification', 'Cloud Storage Deletion', 'Cloud Storage Metadata', 'Cloud Storage Enumeration', 'Cloud Storage Access', 'Application Log Content', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Snapshot Creation', 'Snapshot Modification', 'Snapshot Deletion', 'Snapshot Metadata', 'Snapshot Enumeration', 'Cloud Service Metadata', 'Cloud Service Disable', 'Cloud Service Enumeration', 'Cloud Service Modification', 'Logon Session Metadata', 'Logon Session Creation', 'Network Traffic Flow', 'Network Traffic Content', 'Network Connection Creation', 'Instance Creation', 'Instance Modification', 'Instance Deletion', 'Instance Metadata', 'Instance Enumeration', 'Instance Start', 'Instance Stop', 'Volume Creation', 'Volume Modification', 'Volume Deletion', 'Volume Metadata', 'Volume Enumeration', 'Group Metadata', 'Group Enumeration', 'Group Modification'],

                'SaaS': ['User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Web Credential Creation', 'Web Credential Usage', 'Application Log Content', 'Firewall Metadata', 'Firewall Disable', 'Firewall Rule Modification', 'Firewall Enumeration', 'Cloud Service Metadata', 'Cloud Service Disable', 'Cloud Service Enumeration', 'Cloud Service Modification', 'Logon Session Metadata', 'Logon Session Creation', 'Group Metadata', 'Group Enumeration', 'Group Modification'],

                'Network': ['Command Execution', 'File Metadata', 'File Creation', 'File Deletion', 'File Access', 'File Modification'],

                'Containers': ['User Account Metadata', 'User Account Creation', 'User Account Deletion', 'User Account Modification', 'User Account Authentication', 'Scheduled Job Metadata', 'Scheduled Job Creation', 'Scheduled Job Modification', 'Pod Creation', 'Pod Modification', 'Pod Metadata', 'Pod Enumeration', 'Command Execution', 'Cluster Metadata', 'Container Creation', 'Container Metadata', 'Container Enumeration', 'Container Start']
                }

DATA_SOURCES_ATTACK_V8 = set(['Access tokens', 'Anti-virus', 'API monitoring', 'Application logs', 'Asset management', 'Authentication logs', 'AWS CloudTrail logs', 'AWS OS logs', 'Azure activity logs', 'Azure OS logs', 'Binary file metadata', 'BIOS', 'Browser extensions', 'Component firmware', 'Data loss prevention', 'Detonation chamber', 'Digital certificate logs', 'Disk forensics', 'DLL monitoring', 'DNS records', 'Domain registration', 'EFI', 'Email gateway', 'Environment variable', 'File monitoring', 'GCP audit logs', 'Host network interface', 'Kernel drivers', 'Loaded DLLs', 'Mail server', 'Malware reverse engineering', 'MBR', 'Named Pipes', 'Netflow/Enclave netflow', 'Network device command history',
                              'Network device configuration', 'Network device logs', 'Network device run-time memory', 'Network intrusion detection system', 'Network protocol analysis', 'OAuth audit logs', 'Office 365 account logs', 'Office 365 audit logs', 'Office 365 trace logs', 'Packet capture', 'PowerShell logs', 'Process command-line parameters', 'Process monitoring', 'Process use of network', 'Sensor health and status', 'Services', 'Social media monitoring', 'SSL/TLS certificates', 'SSL/TLS inspection', 'Stackdriver logs', 'System calls', 'Third-party application logs', 'User interface', 'VBR', 'Web application firewall logs', 'Web logs', 'Web proxy', 'Windows Error Reporting', 'Windows event logs', 'Windows Registry', 'WMI Objects'])
