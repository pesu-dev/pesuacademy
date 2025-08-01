from typing import Optional
from pydantic import BaseModel


class Attendance(BaseModel):
    """ Represents attendance information for a course.
    Attributes:
        attended (Optional[int]): Number of classes attended by the student.
        total (Optional[int]): Total number of classes for the course.
        percentage (Optional[float]): Attendance percentage calculated from attended and total classes.
    """
    attended: Optional[int] = None
    total: Optional[int] = None
    percentage: Optional[float] = None


class Course(BaseModel):
    """ Represents a course in the PESU Academy system.
    Attributes:
        code (str): Unique identifier for the course.
        title (str): Title of the course.
        type (Optional[str]): Type of the course (e.g., FC, CC).
        status (Optional[str]): Current status of the course (e.g., Enrolled).
        attendance (Optional[Attendance]): Attendance information for the course.
        course_id (Optional[str]): Unique identifier for the course instance.
    """
    code: str
    title: str
    type: Optional[str] = None
    status: Optional[str] = None
    attendance: Optional[Attendance] = None
    course_id: Optional[str] = None

