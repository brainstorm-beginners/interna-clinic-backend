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


class PatientUpdate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
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


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: GenderEnum
    age: int
    qualification: DoctorQualificationEnum


class DoctorUpdate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: GenderEnum
    age: int

    doctor_id: int


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


class AdminUpdate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str
    password: str
