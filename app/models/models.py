from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, CheckConstraint, Enum, Numeric
from sqlalchemy.orm import declarative_base, relationship

models_metadata = MetaData()
Base = declarative_base(metadata=models_metadata)


class Patient(Base):
    __tablename__ = 'patients'
    metadata = models_metadata

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    middle_name = Column(String(256), nullable=False)
    IIN = Column(String(12), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False, default=False)
    gender = Column(Enum('Мужской', 'Женский', name="genderEnum"), nullable=False, default=False)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 120'), nullable=False)
    ethnicity = Column(Enum('Азиат', 'Европеец', name="ethnicityEnum"), nullable=False, default=False)
    region = Column(String(256), nullable=False)
    height = Column(Integer, CheckConstraint('height > 0'), nullable=False)
    weight = Column(Integer, CheckConstraint('weight > 0'), nullable=False)
    # BMI - ИМТ(Индекс массы тела)
    BMI = Column(Numeric(precision=5, scale=2), CheckConstraint("BMI > 0.00"), nullable=False)
    education = Column(Enum('Не оконченное среднее', 'Среднее', 'Высшие', name="educationEnum"), nullable=False,
                       default=False)
    marital_status = Column(
        Enum('Незамужем/неженат', 'Замужем/женат', 'Разведен/вдова/вдовец', name="marital_statusEnum"),
        nullable=False, default=False)
    job_description = Column(Enum('Требующая большой концентрации', 'Офисная', 'Не работаю',
                                  'С активной физ нагрузкой', 'Другое', name="job_descriptionEnum"), nullable=False,
                             default=False)
    driving_status = Column(Enum('Да', 'Нет', name="driving_statusEnum"), nullable=False, default=False)
    # For the last year only
    was_involved_in_car_accidents = Column(Enum('Да', 'Нет', name="was_involved_in_car_accidentsEnum"), nullable=False,
                                           default=False)
    # Cirrhosis of the liver in outcome
    cirrhosis = Column(Enum('ХГС', 'ХГВ', 'ХГД', 'НАЖБП/МАЖБП', 'Алкогольный стеатогепатит', 'Аутоиммунный гепатит',
                            'ПБХ', 'ПСХ', 'ПБХ + АИГ', 'ПСХ + АИГ', 'БВК', 'Гемохроматоз', 'Другое', name="cirrhosisEnum"), nullable=False,
                       default=False)
    duration_of_illness = Column(Integer, nullable=False, default=False)
    platelet_count = Column(Numeric(precision=3, scale=2), CheckConstraint("platelet_count > 0.00"), nullable=False,
                            default=0.00)
    hemoglobin_level = Column(Numeric(precision=3, scale=2), CheckConstraint("hemoglobin_level > 0.00"), nullable=False,
                              default=0.00)
    ALT = Column(Numeric(precision=3, scale=2), CheckConstraint("ALT > 0.00"), nullable=False, default=0.00)
    ALT_upper = Column(Numeric(precision=3, scale=2), CheckConstraint("ALT_upper > 0.00"), nullable=False, default=0.00)
    # AAT - АСТ(Аспартатаминотрансфераза)
    AAT = Column(Numeric(precision=3, scale=2), CheckConstraint("AAT > 0.00"), nullable=False, default=0.00)
    AAT_upper = Column(Numeric(precision=3, scale=2), CheckConstraint("AAT_upper > 0.00"), nullable=False, default=0.00)
    bilirubin = Column(Numeric(precision=3, scale=2), CheckConstraint("bilirubin > 0.00"), nullable=False, default=0.00)
    creatinine = Column(Numeric(precision=3, scale=2), CheckConstraint("creatinine > 0.00"), nullable=False,
                        default=0.00)
    # INA - MНО(Международное нормализованное отношение)
    INA = Column(Numeric(precision=3, scale=2), CheckConstraint("INA > 0.00"), nullable=False, default=0.00)
    albumin = Column(Numeric(precision=3, scale=2), CheckConstraint("albumin > 0.00"), nullable=False, default=0.00)
    # Sodium - Натрий
    sodium_blood_level = Column(Numeric(precision=3, scale=2), CheckConstraint("sodium_blood_level > 0.00"), nullable=False,
                                default=0.00)
    # Patassium ion - Калий
    potassium_ion = Column(Numeric(precision=3, scale=2), CheckConstraint("potassium_ion > 0.00"), nullable=False,
                           default=0.00)
    # Result express test(Blood ammonia) - Результат экспресс теста(Аммиак крови)
    blood_ammonia = Column(Numeric(precision=3, scale=2), CheckConstraint("blood_ammonia > 0.00"), nullable=False,
                           default=0.00)
    # indirect_elastography - Результат непрямой эластографии печени, стадия фиброза
    indirect_elastography_of_liver = Column(Numeric(precision=3, scale=2), CheckConstraint("indirect_elastography_of_liver > 0.00"),
                                            nullable=False, default=0.00)
    indirect_elastography_of_spleen = Column(Numeric(precision=3, scale=2), CheckConstraint("indirect_elastography_of_spleen > 0.00"),
                                            nullable=False, default=0.00)
    # EVV - Варикозное расширение вен пищевода
    EVV = Column(Enum('1 степень', '2 степень', '3 степень', '4 степень', name="EVVEnum"), nullable=False, default=False)
    # red_flagg_EVV - Красные знаки ВРВ
    red_flags_EVV = Column(Enum('Да', 'Нет', name="red_flags_EVVEnum"), nullable=False, default=False)
    presence_of_ascites = Column(Enum('Нет', 'Контролируемый', 'Рефракетерный', name="presence_of_ascitesEnum"), nullable=False,
                                 default=False)
    reitan_test = Column(Enum('<40 сек', '41-60 сек', '61-90 сек', '91-120 сек', '>120 сек', name="reitan_testEnum"),
                         nullable=False, default=False)
    # TODO rename the field and enum value and comment if needed
    view_ents = Column(Enum('АВС', 'скрытая свная', 'итд', name="view_entsEnum"), nullable=False, default=False)
    comorbidities = Column(String(256), nullable=False, default=False)
    # hepatocellular_carcinoma - Наличие гепатоцеллюлярной карциномы
    hepatocellular_carcinoma = Column(Enum('Да', 'Нет', name="hepatocellular_carcinomaEnum"), nullable=False, default=False)
    # For the last year only
    was_hospitalization = Column(Enum('Плановая', 'Экстренная', name="was_hospitalizationEnum"), nullable=False, default=False)
    # For the last year only
    was_injured = Column(Enum('Да', 'Нет', name="was_injuredEnum"), nullable=False, default=False)
    # GIB - ЖКК(Желудочно-кишечное кровотечение) За последний год
    GIB = Column(Enum('Да', 'Нет', name="GIBEnum"), nullable=False, default=False)
    # For the last year only
    previous_infectious_diseases = Column(Enum('Да', 'Нет', name="previous_infectious_diseasesEnum"), nullable=False,
                                          default=False)
    stool_character = Column(Enum('регулярный (1 раз в 1-2 дня)', 'запор', 'диарея', name="stool_characterEnum"), nullable=False,
                             default=False)
    dehydration = Column(String(256), nullable=False, default=False)
    portosystemic_bypass_surgery = Column(Enum('шунтирующие операции', 'спонтанные шунты', name="portosystemic_bypass_surgeryEnum"),
                                          nullable=False, default=False)
    thrombosis = Column(Enum('Нет', 'тромбоз воротной вены', 'тромбоз печеночных вен', name="thrombosisEnum"), nullable=False,
                        default=False)
    # TODO rename the field if neede
    # Medicines - ЛП(Лекарсвтенные препараты)
    medicines = Column(Enum('прием бензодиазепин', 'прием опиодов', 'ИПП', name="medicinesEnum"), nullable=False, default=False)
    renal_impairment = Column(Enum('Да', 'Нет', name="renal_impairmentEnum"), nullable=False, default=False)
    bad_habits = Column(Enum('Табакокурение', 'Злоупотребление алкоголем', name="bad_habitsEnum"), nullable=False, default=False)
    # TODO rename the field
    CPU = Column(Enum('Имелась', 'Отсутствовала', name="CPUEnum"), nullable=False, default=False)
    # accepted_PE_medications - Список принимаемых ЛС по ПЭ
    accepted_PE_medications = Column(String(256), nullable=False)

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
    gender = Column(Enum('Мужской', 'Женский', name='genderEnum'), nullable=False, default=False)
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
    username = Column(String(256), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False, default=False)
