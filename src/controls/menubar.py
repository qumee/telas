import flet as ft
from .filter import FilterButton
from .access import AccessButton
from .mode import ModeButton
from .table import TableButton
from src.devices.pvt100 import UserPvt100, Pvt100
from asyncio import sleep


class MenuBar(ft.Container):
    """
    Меню-бар сверху страницы, содержащий в себе весь функционал управления
    Сам не меняется при смене режима или доступа, менюятся только атрибуты
    """

    def __init__(self) -> None:
        super().__init__() # Наследование

    def did_mount(self) -> None:
        """
        Метод-костыл для взаимодействия с объектом page
        """
        self.height: int = 50  # Высота
        self.bgcolor: str = "#FFFFFF"  # Цвет фона
        self.border_radius: int = 50  # Радиус скругления
        self.margin: int = 5  # Отступ внутрь
        self.padding: int = 0  # Отступ снаружи
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.BLACK,
            offset=ft.Offset(0, 2),
            blur_style=ft.ShadowBlurStyle.OUTER,
        )

        self.access_button: AccessButton = AccessButton()  # Кнопка смены доступа
        self.mode_button: ModeButton = ModeButton()  # Кнопка смены режима
        self.filter_button: FilterButton = FilterButton()  # Кнопка фильтра
        self.table_button: TableButton = TableButton()
        self.__pvt100: Pvt100 = UserPvt100()  # ПВТ100

        self.controls_row: ft.Row = ft.Row(  # Ряд слева: логотип-разблок, смена режима, фильтр
            [
                ft.Container(width=5),  # Отодвигает от края на 5 пикселей
                self.access_button,  # Кнопка (раз)блокировки в виде логотипа
                self.mode_button,  # Кнопка смены режима
                self.filter_button,  # Кнопка фильтра
                self.table_button
            ],
            alignment=ft.MainAxisAlignment.START,  # Горизонтальное выравнивание
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Вертикальное выравнивание
            width=220  # Ширина
        )

        self.kwargs: dict = {  # Словарь с аргументами для ft.Icon для изменения внешнего вида по наличию подключения
            True: {
                'color': "#20C997",
                "size": 30,
                'name': ft.icons.SIGNAL_CELLULAR_ALT
            },

            False: {
                'color': "#DC3545",
                "size": 30,
                'name': ft.icons.SIGNAL_CELLULAR_OFF
            }
        }

        self.connection_row: ft.Row = ft.Row(  # Ряд справа: статусы подключения
            [
                *[ft.Icon(
                    **self.kwargs[False],
                    tooltip=t
                ) for t in self.page.config.stands.titles],  # Генератор ft.Icons для каждого стенда

                ft.Container(width=5)  # Контейнер для отступа
            ],
            alignment=ft.MainAxisAlignment.END,  # Горизонтальное выравнивание
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Вертикальное выравнивание
            width=220  # Ширина
        )

        self.content: ft.Row = ft.Row(  # Содержание контейнера меню-бара
            [
                self.controls_row,  # Ряд слева: логотип-разблок, смена режима, фильтр
                self.__pvt100,  # Середина: ПВТ 100
                self.connection_row  # Ряд справа: статусы подключения
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Горизонтальное выравнивание
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Вертикальное выравнивание
            height=30,  # Высота
            expand=True  # Растяжка вдоль всего окна
        )
        self.update()
        self.mode = 'Пользовательский'
        self.page.run_task(self.check_connections)

    async def check_connections(self) -> None:
        while True:
            if self.mode == 'Пользовательский':
                statuses = {
                    0: self.page.socket.first_production_status,
                    1: self.page.socket.long_line_status,
                    2: self.page.socket.dct_status
                }
            elif self.mode == 'ТО':
                statuses = {
                    x: True for x in range(0, 3)
                }
            for n, s in enumerate(self.connection_row.controls[:-1]):
                for key, value in self.kwargs[statuses[n]].items():
                    setattr(s, key, value)
            self.update()
            await sleep(1)

    @property
    def pvt100(self):
        return self.content.controls[1]

    @pvt100.setter
    def pvt100(self, value: Pvt100) -> None:
        self.content.controls[1] = value
        self.__pvt100 = value
        self.update()