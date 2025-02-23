from sqlalchemy.orm import Mapped, mapped_column
from .user_models import Model


class DevicesCustomer(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя всех устройств
    """
    __tablename__ = 'devices_customer'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]
    device: Mapped[str]


class Dgs210Customer(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    ДГС ЭРИС-210
    """
    __tablename__: Mapped[str] = 'dgs210_customer'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    unit: Mapped[str]
    gas: Mapped[str]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    concentration: Mapped[float]
    amperage: Mapped[float]
    modified_amperage: Mapped[float]

    status: Mapped[str]



class Dgs230Customer(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    ДГС ЭРИС-230
    """
    __tablename__: Mapped[str] = 'dgs230_customer'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    unit: Mapped[str]
    gas: Mapped[str]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    concentration: Mapped[float]
    amperage: Mapped[float]
    modified_amperage: Mapped[float]

    status: Mapped[str]



class AdvantCustomer(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    Advant
    """
    __tablename__: Mapped[str] = 'advant_customer'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    unit_ch1: Mapped[str]
    gas_ch1: Mapped[str]
    amperage_ch1: Mapped[float]
    modified_amperage_ch1: Mapped[float]
    concentration_ch1: Mapped[float]
    status_ch1: Mapped[str]
    unit_ch2: Mapped[str]
    gas_ch2: Mapped[str]
    amperage_ch2: Mapped[float]
    modified_amperage_ch2: Mapped[float]
    concentration_ch2: Mapped[float]
    status_ch2: Mapped[str]


class XsCustomer(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    ERIS XS
    """
    __tablename__: Mapped[str] = 'xs_customer'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    
    stand: Mapped[str]
    unit: Mapped[str]
    gas: Mapped[str]
    status: Mapped[str]

    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]
    show_rs485: Mapped[bool]

    concentration: Mapped[float]
    modified_amperage: Mapped[float]
    amperage: Mapped[float]


class DctCustomer(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    DCT
    """
    __tablename__: Mapped[str] = 'dct_customer'

    factory_number: Mapped[str] = mapped_column(primary_key=True)

    stand: Mapped[str]
    unit: Mapped[str]
    gas: Mapped[str]
    status: Mapped[str]

    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]
    show_rs485: Mapped[bool]

    concentration: Mapped[float]
    modified_amperage: Mapped[float]
    amperage: Mapped[float]


class Pvt100Customer(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    ОВЕН ПВТ100
    """
    __tablename__: Mapped[str] = 'pvt100_customer'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    max_temperature: Mapped[float]
    min_temperature: Mapped[float]

    max_humidity: Mapped[float]
    min_humidity: Mapped[float]

    delay: Mapped[float]