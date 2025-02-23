import flet as ft
from math import pi

class Device(ft.Container):
    """
    Абстрактный класс устройства
    """
    def __init__(
            self,
            factory_number: str,
    ) -> None:
        super().__init__()  # Наследования
        self.factory_number: str = factory_number  # Завномер
        self.type_text: ft.Text = ft.Text(  # Текст типа прибора
            value='N/A',
            width=145,
            height=18,
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=14,
                weight=ft.FontWeight.W_800,
                color="#FFFFFF"
            )
        )
        self.factory_number_text: ft.Text = ft.Text(  # Текст заводского номера
            value=self.factory_number,
            width=145,
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=16,
                weight=ft.FontWeight.W_800,
                color="#FFFFFF"
            )
        )

    def did_mount(self):
        """
        Костыль, наследуемый из Flet
        Служит для работы с page после инициализации оной
        """
        types = self.page.menubar.filter_button.filter.TYPES  # Путь к массиву с классами
        titles = self.page.config.devices.titles[:-1]  # Массив с названиями устройств
        self.on_click = self.edit
        self.type_text.value = dict(zip(types, titles))[type(self)]  # Словарь соответсвия класса к названию

    async def edit(self, e):
        if self.page.floating_action_button.visible:
            data = await self.page.area.collect_device(self.factory_number, type(self))
            dialog = self.page.area.info(type(self)).edit_dialog
            self.page.open(dialog(data))


class Channel(ft.Container):
    def __init__(self) -> None:
        super().__init__()  # Наследование
        self.width: int = 145  # Ширина
        self.height: int = 180 # Высота
        self.margin: int = 5  # Края
        self.padding: int = 5  # Края
        self.gradient:  ft.LinearGradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    "0xdddddd",
                    "0xa5a5a5"
                ],
                tile_mode=ft.GradientTileMode.MIRROR
        )
        self.blur: int = 10  # Блюр
        self.border_radius: int = 15  # Радиус скгруления
        self.ink: bool = True  # "Волна" при наведении
        self.gas_text: ft.Text = ft.Text(  # Текст газа
                value="N/A",
                text_align=ft.TextAlign.START,
                style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.W_900,
                    color="#FFFFFF"
                )
        )
        self.rs_485_row: ft.Row = ft.Row(  # Значение и измеряемые единицы
            [
                ft.Text(
                    value='XX.X',  # Коцентрация
                    style=ft.TextStyle(
                        size=23,
                        weight=ft.FontWeight.W_800,
                        color="#FFFFFF")
                ),
                ft.Text(
                    value="N/A",  # Единицы измерения
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_700,
                        color="#FFFFFF")
                )
            ]
        )
        self.amperage_row: ft.Row = ft.Row(  # Значение и измеряемые единицы
            [
                ft.Text(
                    value='XX.X',  # Коцентрация
                    style=ft.TextStyle(
                        size=23,
                        weight=ft.FontWeight.W_800,
                        color="#FFFFFF")
                ),
                ft.Text(
                    value='mA',  # Единицы измерения
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_700,
                        color="#FFFFFF")
                )
            ]
        )
        self.modified_amperage_row: ft.Row = ft.Row(  # Значение и измеряемые единицы
            [
                ft.Text(
                    value='XX.X',  # Коцентрация
                    style=ft.TextStyle(
                        size=23,
                        weight=ft.FontWeight.W_800,
                        color="#FFFFFF")
                ),
                ft.Text(
                    value="N/A",  # Единицы измерения
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_700,
                        color="#FFFFFF")
                )
            ],
        )
        self.status_container: ft.Container = ft.Container( # Статус
            content=ft.Text(
                value="НЕТ СВЯЗИ",
                text_align=ft.TextAlign.CENTER,
                style=ft.TextStyle(
                    size=10,
                    weight=ft.FontWeight.W_900,
                    color="#FFFFFF"
                )
            ),
            #bgcolor="#FFFFFF",
            width=145,
            height=15,
            alignment=ft.alignment.center,
            border_radius=10
        )

        self.content: ft.Column = ft.Column( # Содержимое по умолчанию
            width=120,
            height=140,
            spacing=7,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                    self.gas_text,
                    self.rs_485_row,
                    self.amperage_row,
                    self.modified_amperage_row,
                    self.status_container
                ],
        )

    @staticmethod
    async def format_gas(gas: str) -> str:
        """
        Форматирует мелкие индексы у газа
        возвращает газ с индексами
        """
        formats: dict = {  # Словарь по декодировки символов
            'x': 'x', 'y': 'y', '0': '₀',
            '1': '₁', '2': '₂', '3': '₃',
            '4': '₄', '5': '₅', '6': '₆',
            '7': '₇', '8': '₈', '9': '₉'
        }
        for i in formats:  # Поочерёдно заменяет их все
            gas: str = gas.replace(i, formats[i])
        return gas.upper()

    async def set_status(self, status: str) -> None:
        """
        Изменяет статус канала/одноканального девайса
        Меняет цвет и надпись в статус-контейнере
        """
        self.gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=self.page.config.colors[status],
                tile_mode=ft.GradientTileMode.MIRROR
        )
        #self.bgcolor: str = self.page.config.colors[status]  # Смена цвета
        self.status_container.content.value: str = status  # Смена надписи статуса

    async def change_visibility(
            self,
            amperage: bool,
            modified_amperage: bool,
            rs: bool
    ) -> None:
        """
        Изменяет отображение токового выхода, концентраций
        У девайсов, где нет RS будет отключено отображение по умолчанию
        """
        self.amperage_row.visible = amperage  # Меняет отображение токовому выходу
        self.modified_amperage_row.visible = modified_amperage  # Меняет отображение перечитанной по потоковому выходу концентрации
        self.rs_485_row.visible = rs  # Меняет отображение концентрации по RS
        self.height: int = self.height - [amperage, modified_amperage, rs].count(False)*40
        self.update()

    async def set_gas(self, value: str) -> None:
        """
        Меняет отрисовывающийся текст газа
        """
        self.gas_text.value = await self.format_gas(value)
        self.update()

    async def set_unit(self, value: str) -> None:
        """
        Меняет отрисовывающийся текст единицы измерения
        """
        self.rs_485_row.controls[1].value = value
        self.modified_amperage_row.controls[1].value = value
        self.update()

    async def set_rs(self, value: float):
        """
        Изменяет строку с концетрацией по RS
        Нет обновления, т.к. всегда будет обновляться с остальной концентрацией
        """
        self.rs_485_row.controls[0].value = str(round(value, 2)) if value >= 0 else '00.0'

    async def set_amperage(self, value: float) -> None:
        """
        Изменяет строку с токовым выходом
        Нет обновления, т.к. всегда будет обновляться с остальной концентрацией
        """
        self.amperage_row.controls[0].value = str(round(value, 3)) if value >= 0 else '00.0'

    async def set_modified_amperage(self, value: float) -> None:
        """
        Изменяет строку с пересчитанным токовым
        Нет обновления, т.к. всегда будет обновляться с остальной концентрацией
        """
        self.modified_amperage_row.controls[0].value = str(round(value, 2)) if value >= 0 else '00.0'


class SingleChannelDevice(Device, Channel):
    """
    Абстрактный класс для одноканального устройства
    """
    def __init__(self,factory_number: str) -> None:
        super().__init__(factory_number)  # Наследование
        Channel.__init__(self)  # Наследование 2
        self.height: int = 235  # Высота по умолчанию


class Dgs(SingleChannelDevice):
    def __init__(self, factory_number: str) -> None:
        super().__init__(factory_number)  # Наследование

        self.content: ft.Column = ft.Column(  # Колонна с содержимым
            width=120,
            height=140,
            spacing=7,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                self.type_text,
                self.factory_number_text,
                self.gas_text,
                self.rs_485_row,
                self.amperage_row,
                self.modified_amperage_row,
                self.status_container
            ]
        )


class Dgs210(Dgs):
    """
    Класс устройства ДГС ЭРИС-210
    """
    def __init__(self, factory_number: str,) -> None:
        super().__init__(factory_number)  # Наследование


class Dgs230(Dgs):
    """
    Класс устройства ДГС ЭРИС-230
    """
    def __init__(self, factory_number: str) -> None:
        super().__init__(factory_number)  # Наследование


class Xs(SingleChannelDevice):
    """
    Класс устройства ERIS XS
    Собирает данные с СГМ через RS
    """
    def __init__(self, factory_number: str):
        super().__init__(factory_number)  # Наследование
        self.content: ft.Column = ft.Column(  # Колонна с содержимым
            width=120,
            height=140,
            spacing=7,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                self.type_text,
                self.factory_number_text,
                self.gas_text,
                self.amperage_row,
                self.modified_amperage_row,
                self.status_container
            ]
        )


class Dct(SingleChannelDevice):
    """
    Класс устройства DCT
    Добавляется только на один стенд
    Ресурсных испытаний DCT
    """
    def __init__(self, factory_number: str) -> None:
        super().__init__(factory_number)  # Наследование
        self.content = ft.Column(  # Колонна с содержимым
            width=120,
            height=140,
            spacing=7,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                self.type_text,
                self.factory_number_text,
                self.gas_text,
                self.amperage_row,
                self.modified_amperage_row,
                self.status_container
            ]
        )


class DoubleChannelDevice(Device):
    """
    Абстрактный класс для двухканального устройства
    Пока что это только Advant
    """
    def __init__(self, factory_number: str) -> None:
        super().__init__(factory_number)  # Наследование
        self.margin: int = 5  # Края
        self.padding: int = 5  # Края
        #self.bgcolor: str = '#A9A9A9'  # Цвет заднего фона
        self.gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    "0xdddddd",
                    "0xa5a5a5"
                ],
                tile_mode=ft.GradientTileMode.MIRROR
        )
        self.blur: int = 10  # Блюр
        self.width: int = 360  # Ширина
        self.border_radius: int = 15  # Радиус скгруления
        self.ink = True  # "Волна" при наведении
        self.height: int = 260  # Высота
        self.first_channel: Channel = Channel()  # Первый канал
        self.second_channel: Channel = Channel()  # Второй канал


class Advant(DoubleChannelDevice):
    """
    Класс Advant-a, единственный двухканальный
    Почти полностью копия родительского класса за
    исключением расположения элементов внутри контейнера
    """
    def __init__(self, factory_number: str) -> None:
        super().__init__(factory_number) # Наследование
        self.content: ft.Column = ft.Column(  # Колонна с содержимым
            width=120,
            height=138,
            spacing=3,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.type_text,
                self.factory_number_text,
                ft.Row(
                    [
                        self.first_channel,
                        self.second_channel
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=3
                ),
            ]
        )