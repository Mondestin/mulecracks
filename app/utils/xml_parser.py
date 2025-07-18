"""
XML parsing utilities for MuleSoft pom.xml files
"""
import xmltodict
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class XMLParser:
    """Utility class for parsing XML files"""
    
    @staticmethod
    def parse_pom_xml(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse a pom.xml file and return the parsed data
        
        Args:
            file_path: Path to the pom.xml file
            
        Returns:
            Parsed XML data as dictionary or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            return xmltodict.parse(xml_content)
        except Exception as e:
            logger.error(f"Error parsing XML file {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def extract_project_data(pom_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract project information from parsed pom.xml data
        
        Args:
            pom_data: Parsed pom.xml data
            
        Returns:
            Dictionary containing project information
        """
        project_data = pom_data.get('project', {})
        
        return {
            'group_id': project_data.get('groupId', 'Unknown'),
            'artifact_id': project_data.get('artifactId', 'Unknown'),
            'version': project_data.get('version', 'Unknown'),
            'packaging': project_data.get('packaging', 'Unknown'),
            'properties': project_data.get('properties', {}),
            'dependencies': project_data.get('dependencies', {})
        }
    
    @staticmethod
    def extract_dependencies(dependencies_data: Dict[str, Any]) -> list:
        """
        Extract dependencies from pom.xml dependencies section
        
        Args:
            dependencies_data: Dependencies section from pom.xml
            
        Returns:
            List of dependency dictionaries
        """
        dependency_list = dependencies_data.get('dependency', [])
        
        # Handle single dependency case
        if not isinstance(dependency_list, list):
            dependency_list = [dependency_list]
        
        return dependency_list 