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


class PatientCreateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: GenderEnum
    age: int

    doctor_id: int


class PatientCreateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: GenderEnum
    age: int

    doctor_id: int


class PatientUpdate(BaseModel):
    id: int
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
    id: int
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


class AdminCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    username: str
    password: str


class AdminUpdate(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    username: str
    password: str
