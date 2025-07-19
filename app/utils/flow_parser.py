"""
Flow parsing utilities for MuleSoft flow files
"""
import os
import glob
import xmltodict
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from app.models.flows import FlowInfo, EndpointInfo, SubFlowInfo
from app.config.processors import PROCESSOR_KEYS, get_processor_info

logger = logging.getLogger(__name__)


class FlowParser:
    """Utility class for parsing MuleSoft flow files"""
    
    @staticmethod
    def find_flow_files(project_path: str) -> List[str]:
        """
        Find all flow files in a MuleSoft project
        
        Args:
            project_path: Path to the MuleSoft project
            
        Returns:
            List of flow file paths
        """
        flow_patterns = [
            os.path.join(project_path, "src/main/mule/*.xml"),
            os.path.join(project_path, "src/main/resources/*.xml"),
            os.path.join(project_path, "src/main/api/*.xml"),
            os.path.join(project_path, "src/main/flows/*.xml")
        ]
        
        flow_files = []
        for pattern in flow_patterns:
            flow_files.extend(glob.glob(pattern))
        
        return flow_files
    
    @staticmethod
    def parse_flow_file(file_path: str) -> Optional[FlowInfo]:
        """
        Parse a MuleSoft flow file and extract flow information
        
        Args:
            file_path: Path to the flow file
            
        Returns:
            FlowInfo object or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Parse XML to dictionary
            flow_data = xmltodict.parse(xml_content)
            
            # Extract flow information
            flow_info = FlowParser._extract_flow_info(flow_data, file_path)
            
            return flow_info
            
        except Exception as e:
            logger.error(f"Error parsing flow file {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def parse_flow_file_all_flows(file_path: str) -> List[FlowInfo]:
        """
        Parse a MuleSoft flow file and extract all flow information
        
        Args:
            file_path: Path to the flow file
            
        Returns:
            List of FlowInfo objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Parse XML to dictionary
            flow_data = xmltodict.parse(xml_content)
            
            # Extract all flow information
            flow_infos = FlowParser._extract_all_flows_info(flow_data, file_path)
            
            return flow_infos
            
        except Exception as e:
            logger.error(f"Error parsing flow file {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def _extract_all_flows_info(flow_data: Dict[str, Any], file_path: str) -> List[FlowInfo]:
        """
        Extract all flow information from parsed XML data
        
        Args:
            flow_data: Parsed flow XML data
            file_path: Path to the flow file
            
        Returns:
            List of FlowInfo objects
        """
        flow_infos = []
        
        # Check if we have a mule root element
        if 'mule' in flow_data:
            mule_data = flow_data['mule']
            if 'flow' in mule_data:
                flow_elements = mule_data['flow']
                if isinstance(flow_elements, list):
                    for flow_element in flow_elements:
                        flow_info = FlowParser._create_flow_info_from_element(flow_element, file_path, flow_data)
                        if flow_info:
                            flow_infos.append(flow_info)
                else:
                    flow_info = FlowParser._create_flow_info_from_element(flow_elements, file_path, flow_data)
                    if flow_info:
                        flow_infos.append(flow_info)
        else:
            # Direct flow elements (fallback)
            if 'flow' in flow_data:
                flow_elements = flow_data['flow']
                if isinstance(flow_elements, list):
                    for flow_element in flow_elements:
                        flow_info = FlowParser._create_flow_info_from_element(flow_element, file_path, flow_data)
                        if flow_info:
                            flow_infos.append(flow_info)
                else:
                    flow_info = FlowParser._create_flow_info_from_element(flow_elements, file_path, flow_data)
                    if flow_info:
                        flow_infos.append(flow_info)
        
        return flow_infos
    
    @staticmethod
    def _create_flow_info_from_element(flow_element: Dict[str, Any], file_path: str, flow_data: Dict[str, Any] = None) -> FlowInfo:
        """
        Create FlowInfo from a flow element
        
        Args:
            flow_element: Flow XML element
            file_path: Path to the flow file
            flow_data: Parsed flow XML data (optional, for sub-flow extraction)
            
        Returns:
            FlowInfo object
        """
        flow_name = flow_element.get('@name', os.path.basename(file_path))
        
        # Extract endpoints
        endpoints = FlowParser._extract_endpoints(flow_element, flow_name)
        
        # Count processors and collect their names
        processors_count, processors_found = FlowParser._count_processors(flow_element)
        
        # Extract error handlers
        error_handlers = FlowParser._extract_error_handlers(flow_element)
        
        # Extract flow-refs (references to other flows)
        flow_refs = FlowParser._extract_flow_refs(flow_element)
        
        # Extract sub-flows (sub-flows defined in this file)
        sub_flows = []
        if flow_data:
            sub_flows = FlowParser._extract_sub_flows_from_file(flow_data, file_path)
        
        return FlowInfo(
            name=flow_name,
            file_path=file_path,
            endpoints=endpoints,
            processors_count=processors_count,
            processors_found=processors_found,
            error_handlers=error_handlers,
            flow_refs=flow_refs,
            sub_flows=sub_flows
        )
    
    @staticmethod
    def _extract_flow_info(flow_data: Dict[str, Any], file_path: str) -> FlowInfo:
        """
        Extract flow information from parsed XML data
        
        Args:
            flow_data: Parsed flow XML data
            file_path: Path to the flow file
            
        Returns:
            FlowInfo object
        """
        # Find all flow elements in the mule configuration
        flows = []
        
        # Check if we have a mule root element
        if 'mule' in flow_data:
            mule_data = flow_data['mule']
            if 'flow' in mule_data:
                flow_elements = mule_data['flow']
                if isinstance(flow_elements, list):
                    flows.extend(flow_elements)
                else:
                    flows.append(flow_elements)
        else:
            # Direct flow elements (fallback)
            if 'flow' in flow_data:
                flow_elements = flow_data['flow']
                if isinstance(flow_elements, list):
                    flows.extend(flow_elements)
                else:
                    flows.append(flow_elements)
        
        # If no flows found, create basic flow info
        if not flows:
            return FlowInfo(
                name=os.path.basename(file_path),
                file_path=file_path,
                endpoints=[],
                processors_count=0,
                processors_found=[],
                error_handlers=[],
                flow_refs=[],
                sub_flows=[]
            )
        
        # For now, process the first flow (we can enhance this later to handle multiple flows)
        flow_element = flows[0]
        flow_name = flow_element.get('@name', os.path.basename(file_path))
        
        # Extract endpoints
        endpoints = FlowParser._extract_endpoints(flow_element, flow_name)
        
        # Count processors and collect their names
        processors_count, processors_found = FlowParser._count_processors(flow_element)
        
        # Extract error handlers
        error_handlers = FlowParser._extract_error_handlers(flow_element)
        
        # Extract flow-refs (references to other flows)
        flow_refs = FlowParser._extract_flow_refs(flow_element)
        
        # Extract sub-flows (sub-flows defined in this file)
        sub_flows = FlowParser._extract_sub_flows_from_file(flow_data, file_path)
        
        return FlowInfo(
            name=flow_name,
            file_path=file_path,
            endpoints=endpoints,
            processors_count=processors_count,
            processors_found=processors_found,
            error_handlers=error_handlers,
            flow_refs=flow_refs,
            sub_flows=sub_flows
        )
    
    @staticmethod
    def _extract_endpoints(flow_element: Dict[str, Any], flow_name: str = None) -> List[EndpointInfo]:
        """
        Extract endpoint information from flow element and flow name
        
        Args:
            flow_element: Flow XML element
            flow_name: Name of the flow (may contain method and endpoint info)
            
        Returns:
            List of EndpointInfo objects
        """
        endpoints = []
        
        # First, try to extract endpoint info from flow name
        if flow_name:
            flow_endpoint = FlowParser._extract_endpoint_from_flow_name(flow_name)
            if flow_endpoint:
                endpoints.append(flow_endpoint)
        
        # Then look for explicit http:listener, api-gateway:listener, etc.
        endpoint_types = [
            'http:listener',
            'api-gateway:listener',
            'http:request',
            'api-gateway:request',
            'listener'
        ]
        
        for endpoint_type in endpoint_types:
            if endpoint_type in flow_element:
                endpoint_data = flow_element[endpoint_type]
                if isinstance(endpoint_data, list):
                    for endpoint in endpoint_data:
                        endpoints.append(FlowParser._create_endpoint_info(endpoint, endpoint_type))
                else:
                    endpoints.append(FlowParser._create_endpoint_info(endpoint_data, endpoint_type))
        
        return endpoints
    
    @staticmethod
    def _create_endpoint_info(endpoint_data: Dict[str, Any], endpoint_type: str) -> EndpointInfo:
        """
        Create EndpointInfo from endpoint data
        
        Args:
            endpoint_data: Endpoint XML data
            endpoint_type: Type of endpoint
            
        Returns:
            EndpointInfo object
        """
        return EndpointInfo(
            name=endpoint_data.get('@name'),
            path=endpoint_data.get('@path'),
            method=endpoint_data.get('@method'),
            doc_id=endpoint_data.get('@doc:name'),
            config_ref=endpoint_data.get('@config-ref'),
            listener_config=endpoint_data
        )
    
    @staticmethod
    def _count_processors(flow_element: Dict[str, Any]) -> tuple[int, List[str]]:
        """
        Count processors in a flow element recursively and collect their names
        
        Args:
            flow_element: Flow XML element
            
        Returns:
            Tuple of (processor_count, list_of_processor_names)
        """
        processors_found = []
        count = FlowParser._count_processors_recursive(flow_element, processors_found)
        return count, processors_found
    
    @staticmethod
    def _count_processors_recursive(element: Any, processors_found: List[str], count: int = 0, parent_key: str = None) -> int:
        """
        Recursively count processors in an element and collect their names
        
        Args:
            element: XML element to search
            processors_found: List to collect processor names
            count: Current count of processors
            parent_key: Parent element key to check for structural exclusions
            
        Returns:
            Total number of processors found
        """
        if isinstance(element, dict):
            # Check if this element is a processor
            for key in element.keys():
                # Skip http:response when it's nested within http:listener (structural element)
                if key == 'http:response' and parent_key == 'http:listener':
                    # Don't count http:response as a processor when inside http:listener
                    pass
                elif key in PROCESSOR_KEYS:
                    count += 1
                    processors_found.append(key)
                
                # Always recursively search nested elements (even if current key is a processor)
                if isinstance(element[key], (dict, list)):
                    count = FlowParser._count_processors_recursive(element[key], processors_found, count, key)
        
        elif isinstance(element, list):
            # Handle lists of elements
            for item in element:
                count = FlowParser._count_processors_recursive(item, processors_found, count, parent_key)
        
        return count
    
    @staticmethod
    def _extract_error_handlers(flow_element: Dict[str, Any]) -> List[str]:
        """
        Extract error handler names from flow element
        
        Args:
            flow_element: Flow XML element
            
        Returns:
            List of error handler names
        """
        error_handlers = []
        
        if 'error-handler' in flow_element:
            error_handler_data = flow_element['error-handler']
            if isinstance(error_handler_data, list):
                for handler in error_handler_data:
                    if '@name' in handler:
                        error_handlers.append(handler['@name'])
            else:
                if '@name' in error_handler_data:
                    error_handlers.append(error_handler_data['@name'])
        
        return error_handlers
    
    @staticmethod
    def _extract_flow_refs(flow_element: Dict[str, Any]) -> List[str]:
        """
        Extract flow-ref references from flow element
        
        Args:
            flow_element: Flow XML element
            
        Returns:
            List of flow-ref names
        """
        flow_refs = []
        
        if 'flow-ref' in flow_element:
            flow_ref_data = flow_element['flow-ref']
            if isinstance(flow_ref_data, list):
                for flow_ref in flow_ref_data:
                    if '@name' in flow_ref:
                        flow_refs.append(flow_ref['@name'])
            else:
                if '@name' in flow_ref_data:
                    flow_refs.append(flow_ref_data['@name'])
        
        return flow_refs
    
    @staticmethod
    def _extract_sub_flows_from_file(flow_data: Dict[str, Any], file_path: str) -> List[SubFlowInfo]:
        """
        Extract sub-flows defined in the file
        
        Args:
            flow_data: Parsed flow XML data
            file_path: Path to the flow file
            
        Returns:
            List of SubFlowInfo objects
        """
        sub_flows = []
        
        # Check if we have a mule root element
        if 'mule' in flow_data:
            mule_data = flow_data['mule']
            if 'sub-flow' in mule_data:
                sub_flow_elements = mule_data['sub-flow']
                if isinstance(sub_flow_elements, list):
                    for sub_flow_element in sub_flow_elements:
                        sub_flow_info = FlowParser._create_sub_flow_info(sub_flow_element)
                        if sub_flow_info:
                            sub_flows.append(sub_flow_info)
                else:
                    sub_flow_info = FlowParser._create_sub_flow_info(sub_flow_elements)
                    if sub_flow_info:
                        sub_flows.append(sub_flow_info)
        
        return sub_flows
    
    @staticmethod
    def _create_sub_flow_info(sub_flow_element: Dict[str, Any]) -> SubFlowInfo:
        """
        Create SubFlowInfo from a sub-flow element
        
        Args:
            sub_flow_element: Sub-flow XML element
            
        Returns:
            SubFlowInfo object
        """
        sub_flow_name = sub_flow_element.get('@name', 'Unknown Sub-Flow')
        
        # Count processors and collect their names
        processors_count, processors_found = FlowParser._count_processors(sub_flow_element)
        
        return SubFlowInfo(
            name=sub_flow_name,
            processors_count=processors_count,
            processors_found=processors_found
        )
    
    @staticmethod
    def _extract_endpoint_from_flow_name(flow_name: str) -> Optional[EndpointInfo]:
        """
        Extract endpoint information from flow name pattern
        Pattern: "method:path:config" where everything after the second colon is ignored
        
        Args:
            flow_name: Flow name that may contain method and endpoint info
            
        Returns:
            EndpointInfo object or None if no pattern matches
        """
        try:
            # Split by colon to extract method and path
            parts = flow_name.split(':')
            
            if len(parts) >= 2:
                method = parts[0].strip().upper()
                path = parts[1].strip()
                
                # Clean up the path (handle Windows-style paths)
                if '\\' in path:
                    # Handle Windows-style paths in flow names
                    path = path.replace('\\', '/')
                
                # Remove any additional configuration parts (everything after the second colon)
                # For example: "post:\payments:application\json:apiConfig" -> path = "/payments"
                if len(parts) > 2:
                    # Everything after the first colon but before the second colon is the path
                    # The rest (application\json:apiConfig) is ignored
                    pass
                
                # Validate method
                valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
                if method in valid_methods:
                    # Clean up the path name for display
                    clean_name = path.replace('/', '-').replace('(', '').replace(')', '').replace('\\', '-')
                    
                    return EndpointInfo(
                        name=f"{method.lower()}-{clean_name}",
                        path=f"/{path}" if not path.startswith('/') else path,
                        method=method,
                        doc_id=f"{method.lower()}-{clean_name}",
                        config_ref=None,
                        listener_config=None
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting endpoint from flow name '{flow_name}': {str(e)}")
            return None 