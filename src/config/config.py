from dataclasses import dataclass
from json import load


@dataclass
class Postgres:
    """
    Датакласс, хранящий данные от PostgreSQL
    """
    database: str
    host: str
    user: str
    password: str
    port: int

    @property
    def url(self):
        """
        Возвращает ссылку для SQLAlchemy
        """
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


@dataclass
class Connection:
    """
    Датакласс, хранящий данные для подключения к стендам
    """
    name: str = 'null'
    host: str = '127.0.0.1'
    port: int = 502
    timeout: float = 1


class Device:
    """
    Класс для хранения устройств
    В атрибутах хранит юридическое название устройства
    и таблицы с которыми данное устройство ассоциировано
    """
    def __init__(self, title: str, table: str) -> None:
        self.title: str = title  # Наименование модели
        self.user_tablename: str = table + '_user'  # Название SQL-таблицы режима пользователя
        self.customer_tablename: str = table + '_customer'  # Название SQL-таблицы режима ТО


class Devices:
    """
    Класс-хранилище для Device
    """
    def __init__(self, **kwargs) -> None:
        for title, table in kwargs.items():
            self.__dict__[table]: dict[str:str] = Device(title, table)  # Инициализация атрибутов
    
    @property
    def titles(self) -> list[str]:
        return [i.title for i in self.__dict__.values()]  # Наименования всех моделей устройств
    
    @property
    def user_tablesnames(self) -> list[str]:
        return [i.user_tablename for i in self.__dict__.values()]  # Названия SQL-таблиц режима пользователя

    @property
    def customer_tablesnames(self) -> list[str]:
        return [i.customer_tablesnames for i in self.__dict__.values()]  # Названия SQL-таблиц режима ТО


class Stands:
    """
    Класс для хранения информации о стендах
    """
    def __init__(self, stands: dict[str:str]) -> None:
        self.titles: list[str] = list(stands.keys())  # Наименования стендов
        self.to_row: dict[str:str] = stands


class Connections:
    def __init__(self, *args) -> None:
        for arg in args:
            setattr(self, arg['name'], Connection(**arg))


class Config:
    """
    Класс конфига для удобного считывания json и обращения
    к содержимому через точечную нотацию
    """
    def __init__(self, path: str) -> None:

        with open(path, encoding='utf-8') as file:
            config: dict = load(file)  # Чтение JSON

        self.totp: str = config['totp']  # Ключ для генерации TOTP-кода
        self.postgres: Postgres= Postgres(**config['postgres'])  # Конфиг Postgres
        self.colors: dict = config['colors']  # Словарь с цветом и строкой для статуса
        self.devices: Devices = Devices(**config['devices'])  # Информация о моделях устройст
        self.stands: Stands = Stands(config['stands'])  # Информация о стендах
        self.connections: Connections = Connections(*config['connections'])
        self.customer = config['customer']