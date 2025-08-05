"""Model for results in the PESU Academy system."""

from pydantic import BaseModel


class Assessment(BaseModel):
    """Represents an assessment(e.g., ISA1, MATLAB) in the PESU Academy system.

    Attributes:
        name (str): Name of the assessment.
        marks (Optional[str]): Marks obtained in the assessment, if applicable. (e.g., 72)
        total (Optional[str]): Total marks for the assessment, if applicable. (e.g., 100)
    """

    name: str
    marks: str | None = None
    total: str | None = None


class Credits(BaseModel):
    """Represents credits information for a course in the PESU Academy system.

    Attributes:
        earned (str): Credits earned for the course.
        total (str): Total credits available for the course.
    """

    earned: str
    total: str


class CourseResult(BaseModel):
    """Represents the result of a course in the PESU Academy system.

    Attributes:
        code (str): Unique identifier for the course.
        title (str): Title of the course.
        credits (Optional[Credits]): Credits information for the course, if available.
        assessments (List[Assessment]): List of assessments associated with the course.
    """

    code: str
    title: str
    credits: Credits | None = None
    assessments: list[Assessment]


class SemesterResult(BaseModel):
    """Represents the result of a semester in the PESU Academy system.

    Attributes:
        semester (str): Semester number.
        sgpa (str): Semester Grade Point Average.
        credits (Optional[Credits]): Credits information for the semester, if available.
        courses (List[CourseResult]): List of course results for the semester.
    """

    sgpa: str
    credits: Credits | None = None
    courses: list[CourseResult]
