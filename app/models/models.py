from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, CheckConstraint, Enum, Numeric, ARRAY
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
    is_on_controlled = Column(Enum('Да', 'Нет', 'Нет данных', name="is_on_controlledEnum"), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 120'), nullable=False)
    ethnicity = Column(Enum('Азиат', 'Европеец', name="ethnicityEnum"), nullable=False, default=False)
    region = Column(String(256), nullable=False)
    height = Column(Integer, CheckConstraint('height > 0'), nullable=False)
    weight = Column(Integer, CheckConstraint('weight > 0'), nullable=False)
    # BMI - ИМТ(Индекс массы тела)
    BMI = Column(Numeric(precision=5, scale=2), CheckConstraint("BMI > 0.00"), nullable=False)
    education = Column(Enum('Не оконченное среднее', 'Среднее', 'Высшее', name="educationEnum"), nullable=False,
                       default=False)
    marital_status = Column(
        Enum('Не замужем/не женат', 'Замужем/Женат', 'Разведен/вдова/вдовец', name="marital_statusEnum"),
        nullable=False, default=False)
    job_description = Column(Enum('С точными механизмами', 'Офисная', 'Не работаю',
                                  'С активной физ. нагрузкой', 'Другое', name="job_descriptionEnum"), nullable=False,
                             default=False)
    driving_status = Column(Enum('Да', 'Нет', name="driving_statusEnum"), nullable=False, default=False)
    # For the last year only
    was_involved_in_car_accidents = Column(Enum('Да', 'Нет', name="was_involved_in_car_accidentsEnum"), nullable=False,
                                           default=False)
    cirrhosis = Column(ARRAY(String), nullable=False, default=[])
    duration_of_illness = Column(Integer, nullable=False, default=False)
    platelet_count = Column(Numeric(precision=5, scale=2), CheckConstraint("platelet_count >= 0.00"), nullable=False,
                            default=0.00)
    hemoglobin_level = Column(Numeric(precision=5, scale=2), CheckConstraint("hemoglobin_level >= 0.00"), nullable=False,
                              default=0.00)
    ALT = Column(Numeric(precision=5, scale=2), CheckConstraint("ALT >= 0.00"), nullable=False, default=0.00)
    # ALT_unit - АЛТ единица измерения
    ALT_unit = Column(Enum('ЕД/Л', 'МККАТ/Л', name="ALT_unitEnum"), nullable=False, default=False)
    # AAT - АСТ(Аспартатаминотрансфераза)
    AAT = Column(Numeric(precision=5, scale=2), CheckConstraint("AAT >= 0.00"), nullable=False, default=0.00)
    # AAT_unit - АCТ единица измерения
    AAT_unit = Column(Enum('ЕД/Л', 'МККАТ/Л', name="AAT_unit"), nullable=False, default=False)
    bilirubin = Column(Numeric(precision=5, scale=2), CheckConstraint("bilirubin >= 0.00"), nullable=False, default=0.00)
    creatinine = Column(Numeric(precision=5, scale=2), CheckConstraint("creatinine >= 0.00"), nullable=False,
                        default=0.00)
    # INA - MНО(Международное нормализованное отношение)
    INA = Column(Numeric(precision=5, scale=2), CheckConstraint("INA >= 0.00"), nullable=False, default=0.00)
    albumin = Column(Numeric(precision=5, scale=2), CheckConstraint("albumin >= 0.00"), nullable=False, default=0.00)
    # Sodium - Натрий
    sodium_blood_level = Column(Numeric(precision=5, scale=2), CheckConstraint("sodium_blood_level >= 0.00"), nullable=False,
                                default=0.00)
    # Patassium ion - Калий
    potassium_ion = Column(Numeric(precision=5, scale=2), CheckConstraint("potassium_ion >= 0.00"), nullable=False,
                           default=0.00)
    # Result express test(Blood ammonia) - Результат экспресс теста(Аммиак крови)
    blood_ammonia = Column(Numeric(precision=5, scale=2), CheckConstraint("blood_ammonia >= 0.00"), nullable=False,
                           default=0.00)
    # indirect_elastography_of_liver - Результат непрямой эластографии печени, стадия фиброза
    indirect_elastography_of_liver = Column(Numeric(precision=5, scale=2), CheckConstraint("indirect_elastography_of_liver >= 0.00"),
                                            nullable=False, default=0.00)
    # indirect_elastography_of_spleen - Результат непрямой эластографии селезенки
    indirect_elastography_of_spleen = Column(Numeric(precision=5, scale=2), CheckConstraint("indirect_elastography_of_spleen >= 0.00"),
                                            nullable=False, default=0.00)
    # EVV - Варикозное расширение вен пищевода
    EVV = Column(Enum('1 степень', '2 степень', '3 степень', '4 степень', 'Нет', 'Нет данных', name="EVVEnum"), nullable=False, default=False)
    # red_flagg_EVV - Красные знаки ВРВ
    red_flags_EVV = Column(Enum('Да', 'Нет', 'Нет данных', name="red_flags_EVVEnum"), nullable=False, default=False)
    presence_of_ascites = Column(Enum('Нет', 'Контролируемый', 'Рефракетерный', 'Нет данных', name="presence_of_ascitesEnum"), nullable=False,
                                 default=False)
    reitan_test = Column(Enum('<40 сек', '41-60 сек', '61-90 сек', '91-120 сек', '>120 сек', name="reitan_testEnum"),
                         nullable=False, default=False)
    type_of_encephalopathy = Column(String(256), nullable=False, default=False)
    degree_of_encephalopathy = Column(String(256), nullable=False, default=False)
    # process_of_encephalopathy - Течение энцефалопатии
    process_of_encephalopathy = Column(Enum('Эпизодическая', 'Рецидивирующая', 'персистирующая', 'Нет данных', name="progress_of_encephalopathyEnum"),
                                       nullable=False, default=False)
    presence_of_precipitating_factors = Column(Enum('Спровоцированная', 'Неспровоцированная', 'Нет данных', name="presence_of_precipitating_factorsEnum"),
                                               nullable=False, default=False)
    comorbidities = Column(ARRAY(String), nullable=False, default=False)
    # hepatocellular_carcinoma - Наличие гепатоцеллюлярной карциномы
    hepatocellular_carcinoma = Column(Enum('Да', 'Нет', 'Нет данных', name="hepatocellular_carcinomaEnum"), nullable=False, default=False)
    # was_planned_hospitalized_WITH_liver_diseases - Была ли планновая госпитализация связанная с заболеваниями печени за поселдний год
    was_planned_hospitalized_with_liver_diseases = Column(Enum('Да', 'Нет', 'Нет данных', name='was_planned_hospitalized_with_liver_diseasesEnum',
                                                               nullable=False, default=False))
    # number_of_planned_hospitalizations_WITH_liver_deseases - Количество плановых госпитализация связанных с заболеваниями печени
    number_of_planned_hospitalizations_with_liver_diseases = Column(Integer, nullable=False)
    # was_planned_hospitalized_WITHOUT_liver_diseases - Была ли планновая госпитализация не связанная с заболеваниями печени за последний год
    was_planned_hospitalized_without_liver_diseases = Column(Enum('Да', 'Нет', 'Нет данных', name='was_planned_hospitalized_without_liver_diseasesEnum',
                                                                  nullable=False, default=False))
    # number_of_planned_hospitalizations_WITHOUT_liver_diseases - Количество плановых госпитализаций не связанных с заболеваниями печени
    number_of_planned_hospitalizations_without_liver_diseases = Column(Integer, nullable=False)
    # was_emergency_hospitalized_WITH_liver_diseases - Была ли экстренная госпитализация связанная с заболеваниями печени за последний год
    was_emergency_hospitalized_with_liver_diseases = Column(Enum('Да', 'Нет', 'Нет данных', name="was_emergency_hospitalized_with_liver_diseasesEnum"),
                                                            nullable=False, default=False)
    # number_of_emergency_hospitalizations_WITH_liver_diseases - Количество экстренных госпитализаций сввязанных с заболеваниями печени
    number_of_emergency_hospitalizations_with_liver_diseases = Column(Integer, nullable=False)
    # was_emergency_hospitalized_WITHOUT_liver_diseases - Была ли экстренная госпитализация не связанная с заболеваниями печени за последний год
    was_emergency_hospitalized_without_liver_diseases = Column(Enum('Да', 'Нет', 'Нет данных', name="was_emergency_hospitalized_with_liver_diseasesEnum"),
                                                               nullable=False, default=False)
    # number_of_emergency_hospitalizations_WITHOUT_liver_diseases - Количество экстеренных госпитализаций не связанных с заболеваниями печени
    number_of_emergency_hospitalizations_without_liver_diseases = Column(Integer, nullable=False)
    # For the last year only
    was_injured = Column(Enum('Да', 'Нет', name="was_injuredEnum"), nullable=False, default=False)
    # GIB - ЖКК(Желудочно-кишечное кровотечение) За последний год
    GIB = Column(Enum('Да', 'Нет', name="GIBEnum"), nullable=False, default=False)
    # For the last year only
    previous_infectious_diseases = Column(ARRAY(String), nullable=False, default=[])
    stool_character = Column(Enum('Регулярный (1 раз в 1-2 дня)', 'Запор', 'Диарея', name="stool_characterEnum"), nullable=False,
                             default=False)
    dehydration = Column(String(256), nullable=False, default=False)
    portosystemic_bypass_surgery = Column(String(256), nullable=False, default=False)
    thrombosis = Column(Enum('Тромбоз воротной вены', 'Тромбоз печеночных вен', 'Оба варианта', 'Нет', name="thrombosisEnum"),
                        nullable=False, default=False)
    # Medicines - ЛП(Лекарсвтенные препараты)
    medicines = Column(ARRAY(String), nullable=False, default=False)
    renal_impairment = Column(Enum('Да', 'Нет', name="renal_impairmentEnum"), nullable=False, default=False)
    bad_habits = Column(Enum('Табакокурение', 'Злоупотреблением алкоголя', 'Оба варианта', 'Нет', name="bad_habitsEnum"), nullable=False, default=False)
    # TODO rename the field
    CP = Column(Enum('Имелась', 'Отсутствовала', name="CPUEnum"), nullable=False, default=False)
    # accepted_PE_medications - Лекарственные препараты, принимаемые ранее по ПЭ
    accepted_PE_medications = Column(String(256), nullable=False)
    # accepted_medications_at_the_time_of_inspection - Лекарственные препараты, принимаемые на момент осмотра
    accepted_medications_at_the_time_of_inspection = Column(String(256), nullable=False)

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
    qualification = Column(Enum('Гастроэнтеролог', name='doctorQualificationEnum'), nullable=False, default=False)
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
