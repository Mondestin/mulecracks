"""
Service for scanning MuleSoft projects and extracting dependency information
"""
import os
import glob
import logging
from typing import List
from pathlib import Path

from app.models.dependencies import ProjectInfo, DependencyInfo, MuleDependencyScanResponse
from app.utils.xml_parser import XMLParser
from app.config.settings import settings

logger = logging.getLogger(__name__)


class MuleProjectScanner:
    """Service class for scanning MuleSoft projects"""
    
    def __init__(self, mule_directory: str = None):
        """
        Initialize the scanner with MuleSoft projects directory
        
        Args:
            mule_directory: Path to MuleSoft projects directory
        """
        self.mule_directory = mule_directory or settings.get_mule_directory()
        self.xml_parser = XMLParser()
    
    def scan_projects(self) -> MuleDependencyScanResponse:
        """
        Scan all MuleSoft projects and extract dependency information
        
        Returns:
            MuleDependencyScanResponse with project and dependency data
        """
        projects = []
        
        # Find all pom.xml files in the mule directory
        pom_files = self._find_pom_files()
        
        for pom_file in pom_files:
            project_info = self._process_project(pom_file)
            if project_info:
                projects.append(project_info)
        
        return MuleDependencyScanResponse(
            total_projects=len(projects),
            projects=projects
        )
    
    def _find_pom_files(self) -> List[str]:
        """
        Find all pom.xml files in the MuleSoft projects directory
        
        Returns:
            List of pom.xml file paths
        """
        pom_pattern = os.path.join(self.mule_directory, "*/pom.xml")
        return glob.glob(pom_pattern)
    
    def _process_project(self, pom_file: str) -> ProjectInfo:
        """
        Process a single MuleSoft project pom.xml file
        
        Args:
            pom_file: Path to the pom.xml file
            
        Returns:
            ProjectInfo object or None if processing fails
        """
        try:
            # Parse the pom.xml file
            pom_data = self.xml_parser.parse_pom_xml(pom_file)
            if not pom_data:
                return None
            
            # Extract project data
            project_data = self.xml_parser.extract_project_data(pom_data)
            
            # Extract project information
            project_name = os.path.basename(os.path.dirname(pom_file))
            project_path = os.path.dirname(pom_file)
            
            # Extract properties
            properties = project_data['properties']
            app_runtime = properties.get('app.runtime')
            mule_maven_plugin_version = properties.get('mule.maven.plugin.version')
            
            # Extract dependencies from dependencies
            dependencies = self._extract_dependencies(project_data['dependencies'])
            
            # Create project info
            return ProjectInfo(
                project_name=project_name,
                project_path=project_path,
                group_id=project_data['group_id'],
                artifact_id=project_data['artifact_id'],
                version=project_data['version'],
                packaging=project_data['packaging'],
                app_runtime=app_runtime,
                mule_maven_plugin_version=mule_maven_plugin_version,
                dependencies=dependencies
            )
            
        except Exception as e:
            logger.error(f"Error processing project {pom_file}: {str(e)}")
            return None
    
    def _extract_dependencies(self, dependencies_data: dict) -> List[DependencyInfo]:
        """
        Extract dependency information from dependencies
        
        Args:
            dependencies_data: Dependencies section from pom.xml
            
        Returns:
            List of DependencyInfo objects
        """
        dependencies = []
        dependency_list = self.xml_parser.extract_dependencies(dependencies_data)
        
        for dep in dependency_list:
            if self._is_valid_dependency(dep):
                dependency = DependencyInfo(
                    group_id=dep.get('groupId'),
                    artifact_id=dep.get('artifactId'),
                    version=dep.get('version'),
                    classifier=dep.get('classifier'),
                    scope=dep.get('scope')
                )
                dependencies.append(dependency)
        
        return dependencies
    
    def _is_valid_dependency(self, dependency: dict) -> bool:
        """
        Check if a dependency is valid
        
        Args:
            dependency: Dependency dictionary from pom.xml
            
        Returns:
            True if valid dependency, False otherwise
        """
        return (
            dependency.get('groupId') and 
            dependency.get('artifactId') and 
            dependency.get('version')
        ) 