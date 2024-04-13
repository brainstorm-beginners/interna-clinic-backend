from enum import Enum

from pydantic import BaseModel


class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"


class PatientRead(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    gender: GenderEnum
    age: int

    doctor_id: int


# This Pydantic model is needed for router, because we receive raw 'password' field there.
class PatientCreateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str  # <-- Raw password
    gender: GenderEnum
    age: int

    doctor_id: int


# This Pydantic model is needed for service and repository, because we convert raw 'password' field to the
# hashed 'hashed_password' field in the service layer.
class PatientCreateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str  # <-- Hashed password
    gender: GenderEnum
    age: int

    doctor_id: int


class PatientUpdateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: GenderEnum
    age: int

    doctor_id: int


class PatientUpdateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: GenderEnum
    age: int

    doctor_id: int


class DoctorQualificationEnum(str, Enum):
    Pediatrician = 'Pediatrician'
    Gynecologist = 'Gynecologist'
    Psychiatrist = 'Psychiatrist'
    Internists = 'Internists'
    Oncologist = 'Oncologist'
    Dermatologist = 'Dermatologist'


class DoctorRead(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    gender: GenderEnum
    age: int
    qualification: DoctorQualificationEnum


class DoctorReadFullName(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    qualification: DoctorQualificationEnum


class DoctorCreateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: GenderEnum
    age: int
    qualification: DoctorQualificationEnum


class DoctorCreateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: GenderEnum
    age: int
    qualification: DoctorQualificationEnum


class DoctorUpdateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: GenderEnum
    age: int


class DoctorUpdateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: GenderEnum
    age: int


class AdminRead(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str


class AdminCreateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str
    password: str


class AdminCreateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str
    hashed_password: str


class AdminUpdateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str
    password: str


class AdminUpdateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str
    hashed_password: str
