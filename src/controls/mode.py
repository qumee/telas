import flet as ft
from .areas import UserArea, CustomerArea
from .service_area import ServiceArea
from src.devices.pvt100 import CustomerPvt100, UserPvt100


class Mode:
    def __init__(self, page: ft.Page) -> None:
        self.page = page  # Наследование

    async def change_mode(self, e):
        """
        Меняет режим на странице: у Menubar-a и Area
        """
        socket = {
            'ТО': self.page.socket.start,
            'Пользовательский': self.page.socket.start,
            'Сервисный': self.page.socket.stop
        }
        await socket[e.data]()
        pvt100 = {  # Словарь соотвествия классу ПВТ100 к режиму
            'ТО': CustomerPvt100,
            'Пользовательский': UserPvt100,
            'Сервисный': ft.Container
        }#
        self.page.menubar.pvt100 = pvt100[e.data]()  # Инициализация ПВТ100
        self.page.menubar.mode = e.data
        areas = {
            "Пользовательский": UserArea,
            'ТО': CustomerArea,
            'Сервисный': ServiceArea
        }
        self.page.area = areas[e.data]()
        self.page.controls[1].controls[1] = self.page.area
        for i in self.page.menubar.mode_button.items:  # Костыль для PopupMenu, дабы эстетично смотрелось
            i.value = e.data

        status = {  # Словарь соотвествия классу ПВТ100 к режиму
            'ТО': True,
            'Пользовательский': True,
            'Сервисный': False
        }

        self.page.floating_action_button.visible = status[e.data]
        self.page.menubar.filter_button.visible = status[e.data]
        self.page.menubar.connection_row.visible = status[e.data]
        self.page.menubar.table_button.visible = True if e.data == 'Пользовательский' else False

        self.page.update()


class ModeButton(ft.PopupMenuButton):
    """
    Кнопка для выбора режима работы ПО
    """
    def __init__(self):
        super().__init__()  # Наследование

    def did_mount(self):
        """
        Выполняет частично функции конструктора из-за
        отсутвия объекта page при инициализации
        """
        self.icon: str = ft.icons.SETTINGS # Иконка из Flet-а
        self.icon_size: int = 30  # Размер
        self.menu_position: ft.PopupMenuPosition = ft.PopupMenuPosition.UNDER  # Положение меню
        self.icon_color: str = '#A9A9A9' # Цвет иконки
        self.tooltip: str = "Настройки"  # Надпись при наведении
        self.splash_radius: int = 0  # Радиус сплеша
        self.disabled: bool = True  # Отключает по умолчанию
        self.mode: Mode = Mode(self.page)  # Объект Mode для измения режима работы ПО
        self.items = [ # Генерирует Radio-группы
            ft.RadioGroup(
                content=ft.Radio(
                    label=x,
                    value=x,
                    expand=True,
                    fill_color='#096EFD'
                ),
               value='Пользовательский',  # 'Пользовательский' по умолчанию
               on_change=self.mode.change_mode  # Метод смены режима
            ) for x in [ # Надписи для кнопок
                'Пользовательский',
                'ТО',
                'Сервисный'
            ]
        ]
        self.update()  # Обновление
