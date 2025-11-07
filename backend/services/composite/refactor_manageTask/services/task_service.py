"""
Task Service Client
Handles all HTTP operations with the task service.
Implements the Facade pattern — provides a single, unified interface for
task-related operations while hiding internal service details (e.g., API version,
authentication, or data source changes) from its consumers.
"""

import httpx
from typing import Optional, Dict
from fastapi import HTTPException

from models.enums import HttpStatus
from models.task_models import TaskDetails


def _safe_json(response: httpx.Response) -> any:
    """Safely extract JSON from response, return raw text if JSON parsing fails"""
    try:
        return response.json()
    except Exception:
        return response.text


class TaskServiceClient:
    """Handles all task service HTTP operations"""

    """
    Facade for the Task Service.
    --------------------------------------------------
    - Provides a stable interface (get_task, delete_task)
      to all consumers (e.g., workflows, APIs).
    - Internally manages HTTP details, URLs, error handling,
      and schema variations.
    - If the underlying task service is refactored, migrated,
      or replaced, consumers continue to call the same methods
      without knowing anything changed.
    --------------------------------------------------
    Example benefit:
      -> The task service could move from REST to gRPC or change
         its endpoint paths, but this client adapts internally.
         All workflows using TaskServiceClient remain unchanged.
    """
    
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url
        self.timeout = timeout
    
    async def get_task(self, task_id: str) -> Optional[TaskDetails]:
        """
        Fetch task details by ID.
        Returns None if task not found (404), raises HTTPException for other errors.
        """
        """
        Fetch task details by ID.
        Facade hides:
          - Exact endpoint path (/tid/{id})
          - Response schema differences
          - HTTP error translation to consistent exceptions
        Consumers just get a `TaskDetails` object or None.
        """
        get_task_url = f"{self.base_url}/tid/{task_id}"
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout)) as client:
            try:
                response = await client.get(get_task_url)
                
                if response.status_code == HttpStatus.OK.value:
                    get_json = response.json()
                    if get_json is None:
                        get_json = {}
                    task_data = get_json.get("task", {}) or {}
                    
                    return TaskDetails(
                        task_id=task_id,
                        project_id=task_data.get("pid"),
                        owner=task_data.get("created_by_uid"),
                        collaborators=task_data.get("collaborators") or []
                    )
                elif response.status_code == HttpStatus.NOT_FOUND.value:
                    return None
                else:
                    raise HTTPException(
                        status_code=HttpStatus.BAD_GATEWAY.value,
                        detail={
                            "message": "Task service get failed",
                            "status_code": response.status_code,
                            "body": _safe_json(response),
                            "url": get_task_url,
                        },
                    )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=HttpStatus.SERVICE_UNAVAILABLE.value,
                    detail=f"Task service unavailable: {str(e)}"
                )
    
    async def delete_task(self, task_id: str) -> Dict:
        """
        Delete task by ID.
        Returns response details.
        Raises HTTPException if deletion fails (non-2xx/404 status).

        Facade hides:
          - API URL structure
          - HTTP response variations (200 vs 204 vs 404)
          - Conversion to unified response dict
        This ensures consumers (like workflows) always receive
        the same shape of result, even if the backend changes.
        """
        delete_task_url = f"{self.base_url}/{task_id}"
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout)) as client:
            try:
                response = await client.delete(delete_task_url)
                
                # 404 means already deleted - return special response
                if response.status_code == HttpStatus.NOT_FOUND.value:
                    return {
                        "url": delete_task_url,
                        "status_code": HttpStatus.NOT_FOUND.value,
                        "result": "already_deleted",
                        "already_deleted": True,
                    }
                
                accepted_statuses = (
                    HttpStatus.OK.value,
                    HttpStatus.NO_CONTENT.value,
                )
                
                if response.status_code not in accepted_statuses:
                    raise HTTPException(
                        status_code=HttpStatus.BAD_GATEWAY.value,
                        detail={
                            "message": "Task service delete failed",
                            "status_code": response.status_code,
                            "body": _safe_json(response),
                            "url": delete_task_url,
                        },
                    )
                
                return {
                    "url": delete_task_url,
                    "status_code": response.status_code,
                    "result": _safe_json(response),
                    "already_deleted": False,
                }
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=HttpStatus.SERVICE_UNAVAILABLE.value,
                    detail=f"Task service unavailable: {str(e)}"
                )