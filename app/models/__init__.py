from .project import Project as Project
from .user import User as User

User.model_rebuild()
Project.model_rebuild()
