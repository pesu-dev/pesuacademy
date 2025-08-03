"""Model for student profile in the PESU Academy system."""

from pydantic import BaseModel


class PersonalDetails(BaseModel):
    """Represents personal details of a user in the PESU Academy system.

    Attributes:
        name (str): Full name of the user.
        pesu_id (str): PESU ID of the user. (PRN or similar)
        srn (str): SRN of the user.
        program (str): Program enrolled in by the user.
        branch (str): Branch of study.
        semester (str): Current semester.
        section (str): Section of the user.
        email_id (str): Email address of the user.
        contact_no (str): Contact number of the user.
        name_as_in_aadhar (str): Name as per Aadhar card.
        image (Optional[str]): Base64 encoded profile image, if available.
    """

    name: str
    pesu_id: str
    srn: str
    program: str
    branch: str
    semester: str
    section: str
    email_id: str
    contact_no: str
    aadhar_no: str | None = None
    name_as_in_aadhar: str | None = None
    image: str | None = None


class OtherInformation(BaseModel):
    """Represents other personal information of a user in the PESU Academy system.

    Attributes:
        sslc_marks (str): Marks obtained in SSLC.
        puc_marks (str): Marks obtained in PUC.
        date_of_birth (str): Date of birth of the user.
        blood_group (str): Blood group of the user.
    """

    sslc_marks: str
    puc_marks: str
    date_of_birth: str
    blood_group: str


class QualifyingExamination(BaseModel):
    """Represents details of a qualifying examination in the PESU Academy system.

    Attributes:
        exam (str): The qualifying examination.
        rank (str): Rank obtained in the examination.
        score (str): Score obtained in the examination.
    """

    exam: str
    rank: str
    score: str | None = None


class ParentDetails(BaseModel):
    """Represents details of a parent in the PESU Academy system.

    Attributes:
        name (str): Full name of the parent.
        mobile (str): Mobile number of the parent.
        email (str): Email address of the parent.
        occupation (str): Occupation of the parent.
        qualification (str): Qualification of the parent.
        designation (str): Designation of the parent.
        employer (str): Employer of the parent.
    """

    name: str
    mobile: str
    email: str
    occupation: str
    qualification: str
    designation: str
    employer: str


class ParentInformation(BaseModel):
    """Represents information about parents in the PESU Academy system.

    Attributes:
        father (ParentDetails): Details of the father.
        mother (ParentDetails): Details of the mother.
    """

    father: ParentDetails
    mother: ParentDetails


class AddressDetails(BaseModel):
    """Represents address details in the PESU Academy system.

    Attributes:
        present (str): Present address of the user.
        permanent (str): Permanent address of the user.
    """

    present: str
    permanent: str


class Profile(BaseModel):
    """Represents a user's profile in the PESU Academy system.

    Attributes:
        personal (PersonalDetails): Personal details of the user.
        other_info (OtherInformation): Other personal information of the user.
        qualifying_exam (QualifyingExamination): Details of the qualifying examination.
        parents (ParentInformation): Information about the user's parents.
        address (AddressDetails): Address details of the user.
    """

    personal: PersonalDetails
    other_info: OtherInformation
    qualifying_exam: QualifyingExamination
    parents: ParentInformation
    address: AddressDetails
