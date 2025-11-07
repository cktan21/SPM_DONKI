from dataclasses import dataclass
from typing import Optional, List

@dataclass
class TaskDetails:
    """Encapsulates task information"""
    task_id: str
    project_id: Optional[str]
    owner: Optional[str]
    collaborators: List[str]