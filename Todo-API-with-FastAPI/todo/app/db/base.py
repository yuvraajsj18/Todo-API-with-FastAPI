# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.database import Base
from app.models.users import User
from app.models.todo import Todo
