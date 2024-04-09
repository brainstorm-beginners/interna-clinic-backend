from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import declarative_base, relationship

models_metadata = MetaData()
Base = declarative_base(metadata=models_metadata)


class Patient(Base):
    __tablename__ = 'users'
    metadata = models_metadata

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    middle_name = Column(String(256), nullable=False)
    IIN = Column(String(12), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False, default=False)
    gender = Column(Enum('Male', 'Female', name='genderEnum'), nullable=False, default=False)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 120'), nullable=False)

    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    doctor = relationship("Doctor", back_populates="patients")


class Doctor(Base):
    __tablename__ = 'doctors'
    metadata = models_metadata

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    middle_name = Column(String(256), nullable=False)
    IIN = Column(String(12), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False, default=False)
    gender = Column(Enum('Male', 'Female', name='genderEnum'), nullable=False, default=False)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 120'), nullable=False)
    qualification = Column(Enum(
        'Pediatrician',
        'Gynecologist',
        'Psychiatrist',
        'Internists',
        'Oncologist',
        'Dermatologist',
        name='doctorQualificationEnum'), nullable=False, default=False)
    patients = relationship("Patient", back_populates="doctor")


class Admin(Base):
    __tablename__ = 'admins'
    metadata = models_metadata

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    middle_name = Column(String(256), nullable=False)
    username = Column(String(12), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False, default=False)
