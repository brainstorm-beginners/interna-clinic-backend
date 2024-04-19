"""empty message

Revision ID: 9eb70d981ddd
Revises: 
Create Date: 2024-04-18 22:53:07.906380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9eb70d981ddd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=False),
    sa.Column('last_name', sa.String(length=256), nullable=False),
    sa.Column('middle_name', sa.String(length=256), nullable=False),
    sa.Column('username', sa.String(length=256), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.create_table('doctors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=False),
    sa.Column('last_name', sa.String(length=256), nullable=False),
    sa.Column('middle_name', sa.String(length=256), nullable=False),
    sa.Column('IIN', sa.String(length=12), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('gender', sa.Enum('Мужской', 'Женский', name='genderEnum'), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('qualification', sa.Enum('Гастроэнтеролог', name='doctorQualificationEnum'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('IIN')
    )
    op.create_index(op.f('ix_doctors_id'), 'doctors', ['id'], unique=False)
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=False),
    sa.Column('last_name', sa.String(length=256), nullable=False),
    sa.Column('middle_name', sa.String(length=256), nullable=False),
    sa.Column('IIN', sa.String(length=12), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('gender', sa.Enum('Мужской', 'Женский', name='genderEnum'), nullable=False),
    sa.Column('is_on_controlled', sa.Enum('Да', 'Нет', 'Нет данных', name='is_on_controlledEnum'), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('ethnicity', sa.Enum('Азиат', 'Европеец', name='ethnicityEnum'), nullable=False),
    sa.Column('region', sa.String(length=256), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('BMI', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('education', sa.Enum('Не оконченное среднее', 'Среднее', 'Высшее', name='educationEnum'), nullable=False),
    sa.Column('marital_status', sa.Enum('Не замужем/не женат', 'Замужем/Женат', 'Разведен/вдова/вдовец', name='marital_statusEnum'), nullable=False),
    sa.Column('job_description', sa.Enum('С точными физическими нагрузками', 'Офисная', 'Не работаю', 'С активной физ. нагрузкой', 'Другое', name='job_descriptionEnum'), nullable=False),
    sa.Column('driving_status', sa.Enum('Да', 'Нет', name='driving_statusEnum'), nullable=False),
    sa.Column('was_involved_in_car_accidents', sa.Enum('Да', 'Нет', name='was_involved_in_car_accidentsEnum'), nullable=False),
    sa.Column('cirrhosis', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('duration_of_illness', sa.Integer(), nullable=False),
    sa.Column('platelet_count', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('hemoglobin_level', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('ALT', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('ALT_unit', sa.Enum('ЕД/Л', 'МККАТ/Л', name='ALT_unitEnum'), nullable=False),
    sa.Column('AAT', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('AAT_unit', sa.Enum('ЕД/Л', 'МККАТ/Л', name='AAT_unit'), nullable=False),
    sa.Column('bilirubin', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('creatinine', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('INA', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('albumin', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('sodium_blood_level', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('potassium_ion', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('blood_ammonia', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('indirect_elastography_of_liver', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('indirect_elastography_of_spleen', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('EVV', sa.Enum('1 степень', '2 степень', '3 степень', '4 степень', 'Нет', 'Нет данных', name='EVVEnum'), nullable=False),
    sa.Column('red_flags_EVV', sa.Enum('Да', 'Нет', 'Нет данных', name='red_flags_EVVEnum'), nullable=False),
    sa.Column('presence_of_ascites', sa.Enum('Нет', 'Контролируемый', 'Рефракетерный', 'Нет данных', name='presence_of_ascitesEnum'), nullable=False),
    sa.Column('reitan_test', sa.Enum('<40 сек', '41-60 сек', '61-90 сек', '91-120 сек', '>120 сек', name='reitan_testEnum'), nullable=False),
    sa.Column('type_of_encephalopathy', sa.String(length=256), nullable=False),
    sa.Column('degree_of_encephalopathy', sa.String(length=256), nullable=False),
    sa.Column('process_of_encephalopathy', sa.Enum('Эпизодическая', 'Рецидивирующая', 'персистирующая', 'Нет данных', name='progress_of_encephalopathyEnum'), nullable=False),
    sa.Column('presence_of_precipitating_factors', sa.Enum('Спровоцированная', 'Неспровоцированная', 'Нет данных', name='presence_of_precipitating_factorsEnum'), nullable=False),
    sa.Column('comorbidities', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('hepatocellular_carcinoma', sa.Enum('Да', 'Нет', 'Нет данных', name='hepatocellular_carcinomaEnum'), nullable=False),
    sa.Column('was_planned_hospitalized_with_liver_diseases', sa.Enum('Да', 'Нет', 'Нет данных', name='was_planned_hospitalized_with_liver_diseasesEnum'), nullable=True),
    sa.Column('number_of_planned_hospitalizations_with_liver_diseases', sa.Integer(), nullable=False),
    sa.Column('was_planned_hospitalized_without_liver_diseases', sa.Enum('Да', 'Нет', 'Нет данных', name='was_planned_hospitalized_without_liver_diseasesEnum'), nullable=True),
    sa.Column('number_of_planned_hospitalizations_without_liver_diseases', sa.Integer(), nullable=False),
    sa.Column('was_emergency_hospitalized_with_liver_diseases', sa.Enum('Да', 'Нет', 'Нет данных', name='was_emergency_hospitalized_with_liver_diseasesEnum'), nullable=False),
    sa.Column('number_of_emergency_hospitalizations_with_liver_diseases', sa.Integer(), nullable=False),
    sa.Column('was_emergency_hospitalized_without_liver_diseases', sa.Enum('Да', 'Нет', 'Нет данных', name='was_emergency_hospitalized_with_liver_diseasesEnum'), nullable=False),
    sa.Column('number_of_emergency_hospitalizations_without_liver_diseases', sa.Integer(), nullable=False),
    sa.Column('was_injured', sa.Enum('Да', 'Нет', name='was_injuredEnum'), nullable=False),
    sa.Column('GIB', sa.Enum('Да', 'Нет', name='GIBEnum'), nullable=False),
    sa.Column('previous_infectious_diseases', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('stool_character', sa.Enum('Регулярный (1 раз в 1-2 дня)', 'Запор', 'Диарея', name='stool_characterEnum'), nullable=False),
    sa.Column('dehydration', sa.String(length=256), nullable=False),
    sa.Column('portosystemic_bypass_surgery', sa.String(length=256), nullable=False),
    sa.Column('thrombosis', sa.Enum('Тромбоз воротной вены', 'Тромбоз печеночных вен', 'Оба варианта', 'Нет', name='thrombosisEnum'), nullable=False),
    sa.Column('medicines', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('renal_impairment', sa.Enum('Да', 'Нет', name='renal_impairmentEnum'), nullable=False),
    sa.Column('bad_habits', sa.Enum('Табакокурение', 'Злоупотреблением алкоголя', 'Оба варианта', 'Нет', name='bad_habitsEnum'), nullable=False),
    sa.Column('CP', sa.Enum('Имелась', 'Отсутствовала', name='CPUEnum'), nullable=False),
    sa.Column('accepted_PE_medications', sa.String(length=256), nullable=False),
    sa.Column('accepted_medications_at_the_time_of_inspection', sa.String(length=256), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('IIN')
    )
    op.create_index(op.f('ix_patients_id'), 'patients', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_patients_id'), table_name='patients')
    op.drop_table('patients')
    op.drop_index(op.f('ix_doctors_id'), table_name='doctors')
    op.drop_table('doctors')
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_table('admins')
    # ### end Alembic commands ###
