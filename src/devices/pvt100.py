import asyncio
from src.database import Pvt100User, Pvt100Customer
from sqlalchemy import select, update
import flet as ft
from random import uniform
from ctypes import c_int16


class Pvt100(ft.PopupMenuButton):
    """
    Родительский класс для ПВТ100 разных режимов
    """

    def __init__(self):
        super().__init__()  # Наследование

        self.width: int = 220  # Ширина
        self.height: int= 40  # Высота
        self.visible: bool = True  # Видимость
        self.menu_position: ft.PopupMenuPosition = ft.PopupMenuPosition.UNDER  # Позиция меню
        self.disabled: bool = True  # Отключено взаимодействие по умолчанию
        self.on_cancel = self.cancel  # Функция по закрытию
        self.splash_radius: int = 0  # Радуис сплеша при наведении и клике
        self.enable_feedback: bool = False  # Убирает обратную связь

        self.content: ft.Row = ft.Row(
            [
                ft.Icon(  # Красная иконка термостата
                    name=ft.icons.THERMOSTAT,
                    color='#FF6666',
                    size=30
                ),
                ft.Text(  # Обновляемое текстовое поле для отображения температуры
                    '00.0°',
                    size=19,
                    weight=ft.FontWeight.BOLD,
                    color='#707477',
                    #opacity=0.7
                ),
                ft.Container(width=12.5), # Разделитель
                ft.Icon(  # Синяя иконка капли
                    name=ft.icons.WATER_DROP,
                    color='#00D5FF',
                    size=30
                ),
                ft.Text(  # Обновляемое текстовое поле для отображения влажности
                    '00.0%',
                    size=19,
                    weight=ft.FontWeight.BOLD,
                    color='#707477',
                    #opacity=0.7
                ),
            ],
            spacing=5,  # Расстояние между содержимым колонны
            alignment=ft.MainAxisAlignment.CENTER,  # Основное позиционирование по центру
            vertical_alignment=ft.CrossAxisAlignment.CENTER  # Вертикальное позиционирование по центру
        )

    def did_mount(self) -> None:
        """
        Наследуемая функция от Flet для запуска потока
        """
        self.running = True  # Запуск
        self.tooltip = self.page.config.devices.pvt100.title  # Надпись при наведении
        self.page.run_task(self.run)  # Запуск run(), который у наследников разный

    def will_unmount(self) -> None:
        """
        Наследуемая функция от Flet для заверешения потока
        """
        self.running = False

    @property
    def temperature(self) -> float:
        """
        Геттер температуры
        Обрезает сам знак градуса
        """
        return float(self.content.controls[1].value[:-1])

    @temperature.setter
    def temperature(self, value: float) -> None:
        """
        Сеттер температуры
        """
        self.content.controls[1].value = str(round(value, 1)) + '°'

    @property
    def humidity(self):
        """
        Геттер влажности
        """
        return float(self.content.controls[4].value[:-1])

    @humidity.setter
    def humidity(self, value: float):
        """
        Сеттер влажности
        """
        self.content.controls[4].value = str(round(value, 1)) + '%'


class UserPvt100(Pvt100):
    """
    ПВТ100 в пользовательском режиме
    Собирает данные в реальном времени и отрисовывает
    """
    def __init__(self):
        super().__init__()  # Наследование

    async def __get_slave_id(self) -> int:
        """
        Получает Modbus Slave ID из базы данных
        """
        async with self.page.db() as session:
            result = await session.execute(select(Pvt100User.slave_id).where(Pvt100User.id == 1))
            return result.scalar()

    async def __set_slave_id(self, slave_id: int) -> None:
        """
        Записывает Modbus Slave ID в базу данных
        """
        async with self.page.db() as session:
            await session.execute(update(Pvt100User).where(Pvt100User.id==1).values(slave_id=slave_id))
            await session.commit()

    async def cancel(self, e) -> None:
        """
        Метод вызывается после закрытия менюшки
        Собирает введённые данные и заносит в БД и атрибуты
        """
        self.slave_id = int(self.items[0].content.value)
        await self.__set_slave_id(self.slave_id)


    async def run(self) -> None:
        """
        Запускается из did_mount
        Выполняет частично функции конструктора из-за отсутвия в оном асинхронности
        Извлекает slave_id и передаёт в PopupMenuItem для отрисовки
        После в потоке собирает данные и отрисовывает в контейнере
        """
        self.slave_id = await self.__get_slave_id()  # Получение slave id
        self.items = [
            ft.PopupMenuItem(  # Кнопка меню с полем для ввода Modbus Slave id
                content=ft.TextField(
                    width=200,
                    label='Modbus ID',
                    value=self.slave_id,
                    border_width=3.5,
                    border_radius=21,
                    height=50,
                    text_vertical_align=0.0,
                    text_align=ft.TextAlign.CENTER,
                    text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=5, size=16),
                    text_size=19,
                    expand=True,
                    input_filter=ft.NumbersOnlyInputFilter(),
                    label_style=ft.TextStyle(weight=ft.FontWeight.W_700)
                ),
                height=50
            )
        ]
        while self.running:  #  Цикл в фоне, собирающий данные и обновляющий
            try:
                reply = (await self.page.socket.get_ws_data())['rs']['pvt100']
                self.content.controls[1].value = str(round(reply['temperature'] / 100, 1)) + '°'
                self.content.controls[4].value = str(round(reply['humidity'] / 100, 1)) + '%'
                self.update()  # Обновление
            except Exception as e:
                print('pvt100', e)
            finally:
                await asyncio.sleep(10)  # Частота обновления



class CustomerPvt100(Pvt100):
    """
    ПВТ100 в режиме ТО
    Обновляет данные на случайно сгенерированные из диапазона
    """
    def __init__(self):
        super().__init__()  # Наследование

    async def __get_data(self) -> Pvt100Customer:
        """
        Получает данные из БД
        """
        async with self.page.db() as session:
            result = await session.execute(select(Pvt100Customer).where(Pvt100Customer.id == 1))
            return result.scalar()

    async def __set_data(self, **kwargs) -> None:
        """
        Записывает данные в БД
        """
        async with self.page.db() as session:
            await session.execute(update(Pvt100Customer).where(Pvt100Customer.id==1).values(**kwargs))
            await session.commit()

    async def cancel(self, e) -> None:
        """
        Метод вызывается по закрытию менюшки
        Собирает введённые данные и заносит в БД и атрибуты
        """
        kwargs: dict[str:float] = {  # Собирает данные из полей ввода на страничке
            "delay":  float(self.items[0].content.value),
            "max_temperature": float(self.items[1].content.controls[1].controls[0].value),
            "min_temperature": float(self.items[1].content.controls[1].controls[1].value),
            "max_humidity":  float(self.items[2].content.controls[1].controls[0].value),
            "min_humidity":  float(self.items[2].content.controls[1].controls[1].value)
        }
        await self.__set_data(**kwargs)  # Внос в БД
        for key, value in kwargs.items(): # Присваивание атрибутов
            self.__dict__[key] = value


    async def run(self):
        """
        Запускается из did_mount
        Выполняет частично функции конструктора из-за отсутвия в оном асинхронности
        Извлекает данные и передаёт в PopupMenuItem для отрисовки
        После в потоке рандомно меняет температуру и влажность в диапазоне
        """
        result = await self.__get_data()  # Данные из БД
        self.max_temperature: float = result.max_temperature  # Максимальная температура
        self.min_temperature: float = result.min_temperature  # Минимальная температура
        self.max_humidity: float = result.max_humidity  # Максимальная влажность
        self.min_humidity: float = result.min_humidity  # Минимальная влажность
        self.delay: float = result.delay  # Частота обновления

        self.items = [
            ft.PopupMenuItem(  # Поле ввода частоты обновления
                content=ft.TextField(
                    icon=ft.icons.LOCK_CLOCK,
                    width=200,
                    label='Частота',
                    value=self.delay,
                    border_width=3.5,
                    border_radius=21,
                    height=70,
                    text_vertical_align=0.0,
                    text_align=ft.TextAlign.CENTER,
                    text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=5, size=16),
                    text_size=19,
                    expand=True,
                    label_style=ft.TextStyle(weight=ft.FontWeight.W_700)
                ),
                height=70
            ),
            ft.PopupMenuItem( # Содержит столбец для температуры
                content=ft.Row(
                    [
                        ft.Icon(  # Иконка термостата
                            ft.icons.THERMOSTAT,
                            size=35,
                            color='#FF6666'
                        ),
                        ft.Row([  # Ряд с полями ввода
                            ft.TextField( # Поле ввода минимальной температуры
                                width=75,
                                value=self.min_temperature,
                                border_width=3.5,
                                border_radius=21,
                                height=70,
                                text_vertical_align=0.0,
                                text_align=ft.TextAlign.CENTER,
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=2, size=15),
                                text_size=15,
                                label_style=ft.TextStyle(weight=ft.FontWeight.W_700),
                                label='Min',
                            ),
                            ft.TextField(  # Поле ввода максимальной температуры
                                width=75,
                                value=self.max_temperature,
                                border_width=3.5,
                                border_radius=21,
                                height=70,
                                text_vertical_align=0.0,
                                text_align=ft.TextAlign.CENTER,
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=2, size=15),
                                text_size=15,
                                label_style=ft.TextStyle(weight=ft.FontWeight.W_700),
                                label='Max',
                            ),
                        ],
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                height=70,
            ),
            ft.PopupMenuItem(  # Содержит ряд для влажности
                content=ft.Row(
                    [
                        ft.Icon(  # Синяя иконка капли
                            ft.icons.WATER_DROP,
                            size=35,
                            color='#00D5FF'
                        ),
                        ft.Row([  # Ряд с полями ввода
                            ft.TextField(  # Поле ввода минимальной влажности
                                width=75,
                                value=self.min_humidity,
                                border_width=3.5,
                                border_radius=21,
                                height=70,
                                text_vertical_align=0.0,
                                text_align=ft.TextAlign.CENTER,
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=2, size=15),
                                text_size=15,
                                label_style=ft.TextStyle(weight=ft.FontWeight.W_700),
                                label='Min',
                            ),
                            ft.TextField(  # Поле ввода максимальной влажности
                                width=75,
                                value=self.max_humidity,
                                border_width=3.5,
                                border_radius=21,
                                height=70,
                                text_vertical_align=0.0,
                                text_align=ft.TextAlign.CENTER,
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=2, size=15),
                                text_size=15,
                                label_style=ft.TextStyle(weight=ft.FontWeight.W_700),
                                label='Max',
                            ),
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                height=70
            )
        ]
        self.disabled = False  # По умолчанию кликабельно, т.к. всегда иниицилизируется при включённой админке
        while self.running:  # Цикл обновления
            self.temperature = uniform(self.min_temperature, self.max_temperature)  # Генерация температуры
            self.humidity = uniform(self.min_humidity, self.max_humidity)  # Генерация влажности
            self.update()  # Обновление
            await asyncio.sleep(self.delay)  # Задержка
