# lets create a schema for our data using Pydantic
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int = Field(..., description="The unique identifier for the user",minimum=1)
    name: str = Field(..., description="The name of the user",min_length=1, max_length=50)
    email: str = Field(..., description="The email address of the user",min_length=5, max_length=100)
    is_active: bool = Field(default=True, description="Indicates if the user is active")

