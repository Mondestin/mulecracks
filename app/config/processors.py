"""
MuleSoft processor definitions and configurations
"""
from typing import Dict, List, Any

# Comprehensive list of MuleSoft processors with their display names and categories
MULESOFT_PROCESSORS = {
    # HTTP & API Processors
    'http:listener': {'name': 'HTTP Listener', 'category': 'HTTP'},
    'http:request': {'name': 'HTTP Request', 'category': 'HTTP'},
    'http:response': {'name': 'HTTP Response', 'category': 'HTTP'},
    'api-gateway:listener': {'name': 'API Gateway Listener', 'category': 'API Gateway'},
    'api-gateway:request': {'name': 'API Gateway Request', 'category': 'API Gateway'},
    'apikit:router': {'name': 'APIkit Router', 'category': 'APIkit'},
    'apikit:console': {'name': 'APIkit Console', 'category': 'APIkit'},
    'websocket:listener': {'name': 'WebSocket Listener', 'category': 'WebSocket'},
    'websocket:send': {'name': 'WebSocket Send', 'category': 'WebSocket'},
    
    # Data Manipulation Processors
    'set-payload': {'name': 'Set Payload', 'category': 'Data Manipulation'},
    'set-variable': {'name': 'Set Variable', 'category': 'Data Manipulation'},
    'set-session-variable': {'name': 'Set Session Variable', 'category': 'Data Manipulation'},
    'remove-variable': {'name': 'Remove Variable', 'category': 'Data Manipulation'},
    'remove-session-variable': {'name': 'Remove Session Variable', 'category': 'Data Manipulation'},
    'message-enricher': {'name': 'Message Enricher', 'category': 'Data Manipulation'},
    'ee:transform': {'name': 'DataWeave Transform', 'category': 'Data Manipulation'},
    # Note: ee:message, ee:set-payload, ee:variables, ee:set-variable are NOT processors
    # They are structural elements within ee:transform
    
    # Flow Control Processors
    'flow': {'name': 'Flow', 'category': 'Flow Control'},
    'sub-flow': {'name': 'Sub-flow', 'category': 'Flow Control'},
    'flow-ref': {'name': 'Flow Reference', 'category': 'Flow Control'},
    'choice': {'name': 'Choice Router', 'category': 'Flow Control'},
    'foreach': {'name': 'For Each', 'category': 'Flow Control'},
    'filter': {'name': 'Filter', 'category': 'Flow Control'},
    'scatter-gather': {'name': 'Scatter‑Gather', 'category': 'Flow Control'},
    'until-successful': {'name': 'Until Successful', 'category': 'Flow Control'},
    'poll': {'name': 'Poll', 'category': 'Flow Control'},
    'scheduler': {'name': 'Scheduler', 'category': 'Flow Control'},
    'quartz:inbound-endpoint': {'name': 'Quartz Inbound Endpoint', 'category': 'Flow Control'},
    
    # Note: 'when' and 'otherwise' are NOT processors - they are structural elements
    # Note: ee:message, ee:set-payload, ee:variables, ee:set-variable are NOT processors
    # They are structural elements within ee:transform (DataWeave transformations)
    # Note: 'error-handler' is NOT a processor - it's a structural element that contains error handling logic
    # Note: 'http:response' inside 'http:listener' is NOT a processor - it's a structural configuration element
    
    # Error Handling Processors
    'raise-error': {'name': 'Raise Error', 'category': 'Error Handling'},
    'on-error-continue': {'name': 'On Error Continue', 'category': 'Error Handling'},
    'on-error-propagate': {'name': 'On Error Propagate', 'category': 'Error Handling'},
    'circuit-breaker': {'name': 'Circuit Breaker', 'category': 'Error Handling'},
    
    # Database Processors
    'db:select': {'name': 'Database Select', 'category': 'Database'},
    'db:insert': {'name': 'Database Insert', 'category': 'Database'},
    'db:update': {'name': 'Database Update', 'category': 'Database'},
    'db:delete': {'name': 'Database Delete', 'category': 'Database'},
    'mongodb:find': {'name': 'MongoDB Find', 'category': 'Database'},
    'mongodb:insert': {'name': 'MongoDB Insert', 'category': 'Database'},
    'mongodb:update': {'name': 'MongoDB Update', 'category': 'Database'},
    'mongodb:delete': {'name': 'MongoDB Delete', 'category': 'Database'},
    
    # File Operations Processors
    'file:read': {'name': 'File Read', 'category': 'File Operations'},
    'file:write': {'name': 'File Write', 'category': 'File Operations'},
    'file:list': {'name': 'File List', 'category': 'File Operations'},
    'file:delete': {'name': 'File Delete', 'category': 'File Operations'},
    'file:create-directory': {'name': 'File Create Directory', 'category': 'File Operations'},
    'file:move': {'name': 'File Move', 'category': 'File Operations'},
    'file:copy': {'name': 'File Copy', 'category': 'File Operations'},
    'file:append': {'name': 'File Append', 'category': 'File Operations'},
    'ftp:read': {'name': 'FTP Read', 'category': 'File Operations'},
    'ftp:write': {'name': 'FTP Write', 'category': 'File Operations'},
    'sftp:read': {'name': 'SFTP Read', 'category': 'File Operations'},
    'sftp:write': {'name': 'SFTP Write', 'category': 'File Operations'},
    
    # Cloud & External Services
    'aws:s3-get-object': {'name': 'AWS S3 Get Object', 'category': 'Cloud Services'},
    'aws:s3-list-objects': {'name': 'AWS S3 List Objects', 'category': 'Cloud Services'},
    'aws:s3-put-object': {'name': 'AWS S3 Put Object', 'category': 'Cloud Services'},
    'salesforce:query': {'name': 'Salesforce Query', 'category': 'Cloud Services'},
    'salesforce:create': {'name': 'Salesforce Create', 'category': 'Cloud Services'},
    'salesforce:update': {'name': 'Salesforce Update', 'category': 'Cloud Services'},
    'salesforce:delete': {'name': 'Salesforce Delete', 'category': 'Cloud Services'},
    'google-sheets:create-spreadsheet': {'name': 'Google Sheets Create Spreadsheet', 'category': 'Cloud Services'},
    'google-sheets:read-spreadsheet': {'name': 'Google Sheets Read Spreadsheet', 'category': 'Cloud Services'},
    'google-sheets:append-spreadsheet-row': {'name': 'Google Sheets Append Spreadsheet Row', 'category': 'Cloud Services'},
    
    # Messaging Processors
    'jms:publish': {'name': 'JMS Publish', 'category': 'Messaging'},
    'jms:subscribe': {'name': 'JMS Consume (Subscribe)', 'category': 'Messaging'},
    'amqp:publish': {'name': 'AMQP Publish', 'category': 'Messaging'},
    'amqp:subscribe': {'name': 'AMQP Subscribe', 'category': 'Messaging'},
    'rabbitmq:basic-publish': {'name': 'RabbitMQ Publish', 'category': 'Messaging'},
    'rabbitmq:basic-consume': {'name': 'RabbitMQ Consume', 'category': 'Messaging'},
    'mqtt:publish': {'name': 'MQTT Publish', 'category': 'Messaging'},
    'mqtt:subscribe': {'name': 'MQTT Subscribe', 'category': 'Messaging'},
    
    # Batch Processing
    'batch:job': {'name': 'Batch Job', 'category': 'Batch Processing'},
    'batch:step': {'name': 'Batch Step', 'category': 'Batch Processing'},
    'batch:input': {'name': 'Batch Input', 'category': 'Batch Processing'},
    'batch:record': {'name': 'Batch Record', 'category': 'Batch Processing'},
    'batch:commit': {'name': 'Batch Commit', 'category': 'Batch Processing'},
    'batch:on-complete': {'name': 'Batch On Complete', 'category': 'Batch Processing'},
    
    # Validation Processors
    'validation:is-not-null': {'name': 'Validate Is Not Null', 'category': 'Validation'},
    'validation:is-equal': {'name': 'Validate Is Equal', 'category': 'Validation'},
    'validation:is-true': {'name': 'Validate Is True', 'category': 'Validation'},
    'validation:is-false': {'name': 'Validate Is False', 'category': 'Validation'},
    
    # Security Processors
    'secure:encrypt': {'name': 'Secure Encrypt', 'category': 'Security'},
    'secure:decrypt': {'name': 'Secure Decrypt', 'category': 'Security'},
    'secure:hash': {'name': 'Secure Hash', 'category': 'Security'},
    
    # Communication Protocols
    'tcp:listener': {'name': 'TCP Listener', 'category': 'Communication'},
    'tcp:send': {'name': 'TCP Send', 'category': 'Communication'},
    'udp:listen': {'name': 'UDP Listen', 'category': 'Communication'},
    'udp:send': {'name': 'UDP Send', 'category': 'Communication'},
    'ws:consumer': {'name': 'Web Service Consumer', 'category': 'Communication'},
    
    # Data Format Processors
    'xml:validate': {'name': 'XML Validate', 'category': 'Data Format'},
    'xml:transform': {'name': 'XML Transform', 'category': 'Data Format'},
    'csv:read': {'name': 'CSV Read', 'category': 'Data Format'},
    'csv:write': {'name': 'CSV Write', 'category': 'Data Format'},
    'excel:read': {'name': 'Excel Read', 'category': 'Data Format'},
    'excel:write': {'name': 'Excel Write', 'category': 'Data Format'},
    'mime:multipart-assembler': {'name': 'Multipart Assembler', 'category': 'Data Format'},
    'mime:multipart-disassembler': {'name': 'Multipart Disassembler', 'category': 'Data Format'},
    'stream:splitter': {'name': 'Stream Splitter', 'category': 'Data Format'},
    'stream:assembler': {'name': 'Stream Assembler', 'category': 'Data Format'},
    
    # Directory Services
    'ldap:search': {'name': 'LDAP Search', 'category': 'Directory Services'},
    'ldap:create-entry': {'name': 'LDAP Create Entry', 'category': 'Directory Services'},
    'ldap:modify-entry': {'name': 'LDAP Modify Entry', 'category': 'Directory Services'},
    'ldap:delete-entry': {'name': 'LDAP Delete Entry', 'category': 'Directory Services'},
    
    # Social Media & Communication
    'twitter:search-tweets': {'name': 'Twitter Search Tweets', 'category': 'Social Media'},
    'twitter:post-tweet': {'name': 'Twitter Post Tweet', 'category': 'Social Media'},
    'slack:send-message': {'name': 'Slack Send Message', 'category': 'Social Media'},
    'smtp:send-email': {'name': 'Send Email (SMTP)', 'category': 'Communication'},
    
    # Caching
    'cache:retrieve': {'name': 'Cache Retrieve', 'category': 'Caching'},
    'cache:evict-by-key': {'name': 'Cache Evict By Key', 'category': 'Caching'},
    'cache:update': {'name': 'Cache Update', 'category': 'Caching'},
    'cache:invalidate-cache': {'name': 'Invalidate Cache', 'category': 'Caching'},
    
    # Other Processors
    'logger': {'name': 'Logger', 'category': 'Utility'},
    'scripting:execute-script': {'name': 'Execute Script', 'category': 'Utility'},
    'metrics:report': {'name': 'Metrics Report', 'category': 'Monitoring'},
    'transform': {'name': 'Transform', 'category': 'Data Manipulation'},
}

# Get all processor keys
PROCESSOR_KEYS = list(MULESOFT_PROCESSORS.keys())

# Get processors by category
def get_processors_by_category() -> Dict[str, List[str]]:
    """Get processors grouped by category"""
    categories = {}
    for processor, info in MULESOFT_PROCESSORS.items():
        category = info['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(processor)
    return categories

# Get processor info by key
def get_processor_info(processor_key: str) -> Dict[str, str]:
    """Get processor information by key"""
    return MULESOFT_PROCESSORS.get(processor_key, {
        'name': processor_key,
        'category': 'Unknown'
    })

# Get processor name by key
def get_processor_name(processor_key: str) -> str:
    """Get processor display name by key"""
    return MULESOFT_PROCESSORS.get(processor_key, {}).get('name', processor_key)

# Get processor category by key
def get_processor_category(processor_key: str) -> str:
    """Get processor category by key"""
    return MULESOFT_PROCESSORS.get(processor_key, {}).get('category', 'Unknown') 