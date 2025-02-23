import flet as ft
from src.devices import Dgs210, Dgs230, Advant, Dct, Xs

class Filter:
    """
    Фильтрует устройства по стэнду или по модели
    Берёт информацию из действия чекбокса
    """
    TYPES: list[type] = [
        Dgs210, Dgs230,
        Advant, Xs, Dct
    ]
    def __init__(self, page: ft.Page) -> None:
        self.config = page.config  # Ссылка на конфиг со страницы
        self.page = page

    async def filter(self, e) -> None:
        """
        Принимает действие с чекбокса и обрабатывает его
        В зависимости от надписи направляет на фильтрацию по стенду или по устройству
        """
        visible: bool = e.data  # Статус чекбокса
        label: str = e.control.label  # Надпись на чекбоксе, 1 в 1 как в конфиге и фильтре
        if label in self.config.stands.titles:  # Проверяет запрос на фильтрацию по устройству или по стенду
            await self.__filter_by_stand(visible, label)  # Фильтрует по стенду
        elif label in self.config.devices.titles:  # Проверяет запрос на фильтрацию по устройству или по стенду
            await self.__filter_by_device(visible, label)  # Фильтрует по устройству

    async def __filter_by_device(self, visible: bool, device: str) -> None:
        """
        Фильтрует по устройствам
        ПВТ100 должен быть всегда последним из добавленных девайсов
        """
        if device == self.config.devices.titles[-1]:  # Проверка на ПВТ100
            self.page.menubar.pvt100.visible = visible # Изменяет видимость
            self.page.menubar.update()  # Обновление
        else:
            devices: dict[str: type] = {  # Генератор словаря для фильтрации по устройствам
                self.config.devices.titles[i]: j for i, j in enumerate(self.TYPES) # Ссылка на все типы, допустимые для хранения в текущей области
            }
            for i in self.page.area.controls:
                for j in i.controls:
                    if isinstance(j, devices[device]):  # Проверка на соотвествия классу
                        j.visible: bool = visible  # Меняет атрибут видимости
            self.page.area.update()  # Обновление области для демонстрации изменений

    async def __filter_by_stand(self, visible: bool, stand: str) -> None:
        """
        Фильтрует по стенду
        """
        stands: dict[str: list[ft.Control]] = {  # Генератор словаря для фильтрации по стендам
            self.config.stands.titles[i]: j for i, j in enumerate(self.page.area.controls)  # Берёт названия стендов из конфига и соотносит с индексом в области
        }
        for i in stands[stand].controls:
            i.visible: bool = visible  # Меняет атрибут видимости

        self.page.area.update()  # Обновление области для демонстрации изменений


class FilterButton(ft.PopupMenuButton):
    """
    Класс выпадающее меню
    Показывает чекбоксы с фильтрами для устройств
    """
    def __init__(self) -> None:
        super().__init__()  # Наследование

    def did_mount(self):
        """
        Выполняет частично функции конструктора из-за
        отсутвия объекта page при инициализации
        """
        self.filter: Filter = Filter(self.page) # Иницилизация фильтра и передача в него page
        labels: list[str] = self.page.config.devices.titles + self.page.config.stands.titles  # Надписи для чекбоксов
        self.icon: str = ft.icons.FILTER_ALT  # Иконка из Flet
        self.icon_size: int = 30  # Размер
        self.menu_position: ft.PopupMenuPosition = ft.PopupMenuPosition.UNDER  # Положение меню
        self.icon_color: str = '#A9A9A9'   # Цвет иконки
        self.tooltip: str = "Фильтр"  # Надпись при наведении
        self.splash_radius: int = 0  # Радиус сплеша

        self.items: list[ft.PopupMenuItem] = [  # Добавления элементов меню с лэйблами из конфига
            ft.PopupMenuItem(content=ft.Checkbox(
                splash_radius=0,
                label=x,
                border_side=ft.BorderSide(color='#A9A9A9', width=0),
                fill_color={
                    ft.ControlState.PRESSED: '#096EFD',
                    ft.ControlState.SELECTED: '#096EFD',
                    ft.ControlState.DEFAULT: '#A9A9A9'
                },
                check_color='#FFFFFF',
                value=True,  # По умолчанию все устройства отображаются
                on_change=self.filter.filter  # Вызывает filter() и передаёт действие с чекбокса
            ),
            ) for x in labels  # Называет лэйблы у чекбоксов в соотвествии с названиями в конфигах
        ]

        self.items.insert(-3, ft.PopupMenuItem())  # Разделитель
        self.update()  # Обновление