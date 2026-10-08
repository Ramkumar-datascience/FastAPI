# This file contains our SQLAlchemy database model.
# The model describes what our database table should look like.
from sqlalchemy import Column, Integer, String

# Import Base from database.py
from db_connection import Base

# ---------------------------------------------------------
# Student Database Model
# ---------------------------------------------------------
# This Python class represents the "students" table
# inside our SQLite database.
class Student(Base):

    # Name of the database table
    __tablename__ = "students"
    
    # -----------------------------------------------------
    # ID Column
    # -----------------------------------------------------
    # primary_key=True means this is the unique ID
    # for every student.
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(String,nullable=False)
    # unique=True means two students cannot have
    # the same email.
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    course = Column(
        String,
        nullable=False
    )