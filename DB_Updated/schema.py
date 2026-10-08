# This is where we define the data coming into and going out of our API.
# We use Pydantic here.

from pydantic import BaseModel

# ---------------------------------------------------------
# Student Create Schema
# ---------------------------------------------------------
# This defines what data the client must send
# when creating a student.
class StudentCreate(BaseModel):

    name: str
    email: str
    course: str


# ---------------------------------------------------------
# Student Response Schema
# ---------------------------------------------------------
# This defines what data our API will return.
class StudentResponse(BaseModel):

    id: int
    name: str
    email: str
    course: str

    # -----------------------------------------------------
    # Important
    # -----------------------------------------------------
    # SQLAlchemy returns an object.
    #
    # Pydantic normally expects a dictionary-like object.
    #
    # from_attributes=True allows Pydantic to read
    # data directly from the SQLAlchemy object.
    class Config:
        from_attributes = True