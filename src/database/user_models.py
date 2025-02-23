from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Model(DeclarativeBase):
    """
    Наследник шаблона для таблицы в SQL
    """
    pass


class DevicesUser(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя всех устройств
    """
    __tablename__ = 'devices_user'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]
    device: Mapped[str]

class Dgs210User(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя
    ДГС ЭРИС-210
    """
    __tablename__ = 'dgs210_user'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    unit: Mapped[str]
    gas: Mapped[str]
    comment: Mapped[str]
    discreteness: Mapped[int]

    slave_id: Mapped[int]

    owen_id: Mapped[int]
    owen_channel: Mapped[int]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    amperage_low: Mapped[float]
    amperage_high: Mapped[float]
    amperage_threshold1: Mapped[float]
    amperage_threshold2: Mapped[float]


class Dgs230User(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя
    ДГС ЭРИС-230
    """
    __tablename__ = 'dgs230_user'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    unit: Mapped[str]
    gas: Mapped[str]
    comment: Mapped[str]
    discreteness: Mapped[int]

    slave_id: Mapped[int]

    owen_id: Mapped[int]
    owen_channel: Mapped[int]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    amperage_low: Mapped[float]
    amperage_high: Mapped[float]
    amperage_threshold1: Mapped[float]
    amperage_threshold2: Mapped[float]


class AdvantUser(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя
    Advant
    """
    __tablename__ = 'advant_user'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]


    slave_id: Mapped[int]
    comment: Mapped[str]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    unit_ch1: Mapped[str]
    gas_ch1: Mapped[str]
    discreteness_ch1: Mapped[int]

    unit_ch2: Mapped[str]
    gas_ch2: Mapped[str]
    discreteness_ch2: Mapped[int]
    
    owen_id_ch1: Mapped[int]
    owen_number_ch1: Mapped[int]

    owen_id_ch2: Mapped[int]
    owen_number_ch2: Mapped[int]

    amperage_low_ch1: Mapped[float]
    amperage_high_ch1: Mapped[float]
    amperage_threshold1_ch1: Mapped[float]
    amperage_threshold2_ch1: Mapped[float]

    amperage_low_ch2: Mapped[float]
    amperage_high_ch2: Mapped[float]
    amperage_threshold1_ch2: Mapped[float]
    amperage_threshold2_ch2: Mapped[float]


class XsUser(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя
    ERIS XS
    """
    __tablename__ = 'xs_user'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    unit: Mapped[str]
    gas: Mapped[str]
    comment: Mapped[str]
    slave_id: Mapped[int]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]

    amperage_low: Mapped[float]
    amperage_high: Mapped[float]
    amperage_threshold1: Mapped[float]
    amperage_threshold2: Mapped[float]


class DctUser(Model):
    """
    Класс-модель таблицы для хранения в режиме пользователя
    DCT
    """
    __tablename__ = 'dct_user'

    factory_number: Mapped[str] = mapped_column(primary_key=True)
    stand: Mapped[str]

    unit: Mapped[str]
    gas: Mapped[str]
    comment: Mapped[str]
        
    channel: Mapped[int]

    show_rs485: Mapped[bool]
    show_modified_amperage: Mapped[bool]
    show_amperage: Mapped[bool]


class Pvt100User(Model):
    """
    Класс-модель таблицы для хранения в режиме ТО
    ОВЕН ПВТ100
    """
    __tablename__: str = 'pvt100_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    slave_id: Mapped[int]


class StandsService(Model):
    """
    Класс-модель таблицы для хранения таблицы с информацией о техобслуживании
    """
    __tablename__: str = 'stands_service'

    id: Mapped[int] = mapped_column(primary_key=True)
    stand: Mapped[str]
    year: Mapped[int]
    month: Mapped[str]
    action: Mapped[str]