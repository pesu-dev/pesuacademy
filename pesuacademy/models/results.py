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


class CourseResult(BaseModel):
    """Represents the result of a course in the PESU Academy system.

    Attributes:
        code (str): Unique identifier for the course.
        title (str): Title of the course.
        credits_earned (str): Credits earned for the course.
        credits_total (str): Total credits available for the course.
        assessments (List[Assessment]): List of assessments associated with the course.
    """

    code: str
    title: str
    credits_earned: str
    credits_total: str
    assessments: list[Assessment]


class SemesterResult(BaseModel):
    """Represents the result of a semester in the PESU Academy system.

    Attributes:
        semester (str): Semester number.
        sgpa (str): Semester Grade Point Average.
        credits_earned (str): Total credits earned in the semester.
        credits_total (str): Total credits available in the semester.
        courses (List[CourseResult]): List of course results for the semester.
    """

    sgpa: str
    credits_earned: str
    credits_total: str
    courses: list[CourseResult]
