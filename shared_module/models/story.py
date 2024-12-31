from typing import List, Dict, Optional
from pydantic import BaseModel
from models.action import Action

class Story(BaseModel):
    id: str
    session_id: str  
    title: str
    startTimestamp: str
    endTimestamp: str
    initialState: Dict[str, str]
    finalState: Dict[str, str]
    actions: List[Action]
    networkRequests: List[Dict[str, Optional[str]]]

    def __init__(self, **data):
        super().__init__(**data)
        self.actions = [Action(**action) if isinstance(action, dict) else action for action in self.actions]
        