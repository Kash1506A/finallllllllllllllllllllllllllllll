import json
import os
from typing import List, Optional, Dict
from datetime import datetime

class ProjectDB:
    """Simple JSON-based database for projects"""
    
    def __init__(self, db_path: str = "data/projects.json"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        if not os.path.exists(db_path):
            self._save_db([])
    
    def _load_db(self) -> List[dict]:
        """Load database from JSON file"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_db(self, data: List[dict]):
        """Save database to JSON file"""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_project(self, project_data: dict) -> str:
        """Create new project and return ID"""
        projects = self._load_db()
        
        # Generate unique ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_id = f"proj_{len(projects) + 1}_{timestamp}"
        
        # Create project object
        project = {
            "id": project_id,
            "created_at": datetime.now().isoformat(),
            "status": "queued",
            **project_data
        }
        
        projects.append(project)
        self._save_db(projects)
        
        print(f"✅ Created project: {project_id}")
        return project_id
    
    def get_project(self, project_id: str) -> Optional[dict]:
        """Get project by ID"""
        projects = self._load_db()
        return next((p for p in projects if p["id"] == project_id), None)
    
    def update_project(self, project_id: str, updates: dict):
        """Update project with new data"""
        projects = self._load_db()
        
        for project in projects:
            if project["id"] == project_id:
                project.update(updates)
                project["updated_at"] = datetime.now().isoformat()
                break
        
        self._save_db(projects)
    
    def delete_project(self, project_id: str):
        """Delete a project"""
        projects = self._load_db()
        projects = [p for p in projects if p["id"] != project_id]
        self._save_db(projects)
    
    def get_all_projects(self) -> List[dict]:
        """Get all projects"""
        return self._load_db()
    
    def get_recent_projects(self, limit: int = 10) -> List[dict]:
        """Get recent projects"""
        projects = self._load_db()
        return sorted(
            projects,
            key=lambda p: p.get("created_at", ""),
            reverse=True
        )[:limit]