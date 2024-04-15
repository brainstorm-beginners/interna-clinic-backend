from enum import Enum

from pydantic import BaseModel


class PatientRead(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    gender: str
    age: int
    ethnicity: str
    region: str
    height: int
    weight: int
    BMI: float
    education: str
    marital_status: str
    job_description: str
    driving_status: str
    was_involved_in_car_accidents: str
    cirrhosis: str
    duration_of_illness: int
    platelet_count: float
    hemoglobin_level: float
    ALT: float
    ALT_upper: float
    AAT: float
    AAT_upper: float
    bilirubin: float
    creatinine: float
    INA: float
    albumin: float
    sodium_blood_level: float
    potassium_ion: float
    blood_ammonia: float
    indirect_elastography_of_liver: float
    indirect_elastography_of_spleen: float
    EVV: str
    red_flags_EVV: str
    presence_of_ascites: str
    reitan_test: str
    view_ents: str
    comorbidities: str
    hepatocellular_carcinoma: str
    was_hospitalized: str
    was_injured: str
    GIB: str
    previous_infectious_diseases: str
    stool_character: str
    dehydration: str
    portosystemic_bypass_surgery: str
    thrombosis: str
    medicines: str
    renal_impairment: str
    bad_habits: str
    CPU: str
    accepted_PE_medications: str

    doctor_id: int


# This Pydantic model is needed for router, because we receive raw 'password' field there.
class PatientCreateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str  # <-- Raw password
    gender: str = "Мужской"
    age: int
    ethnicity: str = "Азиат"
    region: str = "Алматы"
    height: int
    weight: int
    BMI: float
    education: str = "Среднее"
    marital_status: str = "Не замужем/не женат"
    job_description: str = "Другое"
    driving_status: str = "Да"
    was_involved_in_car_accidents: str = "Нет"
    cirrhosis: str
    duration_of_illness: int
    platelet_count: float
    hemoglobin_level: float
    ALT: float
    ALT_upper: float
    AAT: float
    AAT_upper: float
    bilirubin: float
    creatinine: float
    INA: float
    albumin: float
    sodium_blood_level: float
    potassium_ion: float
    blood_ammonia: float
    indirect_elastography_of_liver: float
    indirect_elastography_of_spleen: float
    EVV: str = "Нет"
    red_flags_EVV: str = "Нет"
    presence_of_ascites: str = "Нет"
    reitan_test: str = "Нет данных"
    view_ents: str
    comorbidities: str
    hepatocellular_carcinoma: str = "Нет"
    was_hospitalized: str = "Нет"
    was_injured: str = "Нет"
    GIB: str = "Нет"
    previous_infectious_diseases: str = "Нет"
    stool_character: str = "Регулярный (1 раз в 1-2 дня)"
    dehydration: str
    portosystemic_bypass_surgery: str = "Нет"
    thrombosis: str = "Нет"
    medicines: str = "Другое"
    renal_impairment: str = "Нет"
    bad_habits: str = "Нет"
    CPU: str
    accepted_PE_medications: str

    doctor_id: int


# This Pydantic model is needed for service and repository, because we convert raw 'password' field to the
# hashed 'hashed_password' field in the service layer.
class PatientCreateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str  # <-- Hashed password
    gender: str
    age: int
    ethnicity: str
    region: str
    height: int
    weight: int
    BMI: float
    education: str
    marital_status: str
    job_description: str
    driving_status: str
    was_involved_in_car_accidents: str
    cirrhosis: str
    duration_of_illness: int
    platelet_count: float
    hemoglobin_level: float
    ALT: float
    ALT_upper: float
    AAT: float
    AAT_upper: float
    bilirubin: float
    creatinine: float
    INA: float
    albumin: float
    sodium_blood_level: float
    potassium_ion: float
    blood_ammonia: float
    indirect_elastography_of_liver: float
    indirect_elastography_of_spleen: float
    EVV: str
    red_flags_EVV: str
    presence_of_ascites: str
    reitan_test: str
    view_ents: str
    comorbidities: str
    hepatocellular_carcinoma: str
    was_hospitalized: str
    was_injured: str
    GIB: str
    previous_infectious_diseases: str
    stool_character: str
    dehydration: str
    portosystemic_bypass_surgery: str
    thrombosis: str
    medicines: str
    renal_impairment: str
    bad_habits: str
    CPU: str
    accepted_PE_medications: str

    doctor_id: int


class PatientUpdateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: str = "Мужской"
    age: int
    ethnicity: str = "Азиат"
    region: str = "Алматы"
    height: int
    weight: int
    BMI: float
    education: str = "Среднее"
    marital_status: str = "Не замужем/не женат"
    job_description: str = "Другое"
    driving_status: str = "Да"
    was_involved_in_car_accidents: str = "Нет"
    cirrhosis: str
    duration_of_illness: int
    platelet_count: float
    hemoglobin_level: float
    ALT: float
    ALT_upper: float
    AAT: float
    AAT_upper: float
    bilirubin: float
    creatinine: float
    INA: float
    albumin: float
    sodium_blood_level: float
    potassium_ion: float
    blood_ammonia: float
    indirect_elastography_of_liver: float
    indirect_elastography_of_spleen: float
    EVV: str = "Нет"
    red_flags_EVV: str = "Нет"
    presence_of_ascites: str = "Нет"
    reitan_test: str = "Нет данных"
    view_ents: str
    comorbidities: str
    hepatocellular_carcinoma: str = "Нет"
    was_hospitalization: str = "Нет"
    was_injured: str = "Нет"
    GIB: str = "Нет"
    previous_infectious_diseases: str = "Нет"
    stool_character: str = "Регулярный (1 раз в 1-2 дня)"
    dehydration: str
    portosystemic_bypass_surgery: str = "Нет"
    thrombosis: str = "Нет"
    medicines: str = "Другое"
    renal_impairment: str = "Нет"
    bad_habits: str = "Нет"
    CPU: str
    accepted_PE_medications: str

    doctor_id: int


class PatientUpdateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: str
    age: int
    ethnicity: str
    region: str
    height: int
    weight: int
    BMI: float
    education: str
    marital_status: str
    job_description: str
    driving_status: str
    was_involved_in_car_accidents: str
    cirrhosis: str
    duration_of_illness: int
    platelet_count: float
    hemoglobin_level: float
    ALT: float
    ALT_upper: float
    AAT: float
    AAT_upper: float
    bilirubin: float
    creatinine: float
    INA: float
    albumin: float
    sodium_blood_level: float
    potassium_ion: float
    blood_ammonia: float
    indirect_elastography_of_liver: float
    indirect_elastography_of_spleen: float
    EVV: str
    red_flags_EVV: str
    presence_of_ascites: str
    reitan_test: str
    view_ents: str
    comorbidities: str
    hepatocellular_carcinoma: str
    was_hospitalized: str
    was_injured: str
    GIB: str
    previous_infectious_diseases: str
    stool_character: str
    dehydration: str
    portosystemic_bypass_surgery: str
    thrombosis: str
    medicines: str
    renal_impairment: str
    bad_habits: str
    CPU: str
    accepted_PE_medications: str

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
    gender: str = "Мужской"
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
    gender: str = "Мужской"
    age: int
    qualification: DoctorQualificationEnum


class DoctorCreateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: str = "Мужской"
    age: int
    qualification: DoctorQualificationEnum


class DoctorUpdateRawPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    password: str
    gender: str = "Мужской"
    age: int


class DoctorUpdateHashedPassword(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    IIN: str
    hashed_password: str
    gender: str = "Мужской"
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
