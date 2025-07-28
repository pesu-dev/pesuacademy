from pydantic import BaseModel


class PersonalDetails(BaseModel):
    """ Represents personal details of a user in the PESU Academy system.
    Attributes:
        name (str): Full name of the user.
        pesu_id (str): Unique identifier for the user in the PESU system.
        srn (str): Student Registration Number.
        program (str): Program in which the user is enrolled.
        branch (str): Branch of study.
        semester (str): Current semester of the user.
        section (str): Section of the class.
        email_id (str): Email address of the user.
        contact_no (str): Contact number of the user.
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


class ParentDetails(BaseModel):
    """ Represents details of a parent in the PESU Academy system.
    Attributes:
        name (str): Full name of the parent.
        mobile (str): Mobile number of the parent.
        email (str): Email address of the parent.
        occupation (str): Occupation of the parent.
    """
    name: str
    mobile: str
    email: str
    occupation: str


class ParentInformation(BaseModel):
    """ Represents information about parents in the PESU Academy system.
    Attributes:
        father (ParentDetails): Details of the father.
        mother (ParentDetails): Details of the mother.
    """
    father: ParentDetails
    mother: ParentDetails


class AddressDetails(BaseModel):
    """ Represents address details in the PESU Academy system.
    Attributes:
        present (str): Present address of the user.
        permanent (str): Permanent address of the user.
    """
    present: str
    permanent: str


# Need to add Other details like profile picture, date of birth, Blood Group, etc. in the future.
class Profile(BaseModel):
    """ Represents a user's profile in the PESU Academy system.
    Attributes:
        personal (PersonalDetails): Personal details of the user.
        parents (ParentInformation): Information about the user's parents.
        address (AddressDetails): Address details of the user.
    """
    personal: PersonalDetails
    parents: ParentInformation
    address: AddressDetails