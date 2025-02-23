import flet as ft
from pyotp.totp import TOTP


class Access:
    def __init__(self, page: ft.Page):
        self.page = page
        self.__totp = TOTP(self.page.config.totp)

    async def block(self) -> None:
        self.page.floating_action_button.visible = False  # Убирает кнопку добавления девайсов
        self.page.menubar.pvt100.disabled = True  # Выключает возможность изменения ПВТ100
        self.page.menubar.mode_button.disabled = True  # Выключает возможность изменить режим

    async def unblock(self, data: str) -> bool:
        if self.__totp.verify(data):
            self.page.floating_action_button.visible = True  # Показывает кнопку добавления девайсов
            self.page.menubar.pvt100.disabled = False  # Выключает возможность изменения ПВТ100
            self.page.menubar.mode_button.disabled = False  # Выключает возможность изменить режим
            return True
        else:
            return False


class AccessButton(ft.IconButton):
    """Кнопка для (раз)блокировки в виде логотипа ГК ЭРИС"""

    def __init__(self):
        super().__init__()
        self.content = ft.Image(src='iconRed.png', height=32.5)  # Импорт логотипа

    def did_mount(self):
        """
        Выполняет частично функции конструктора из-за
        отсутвия объекта page при инициализации
        """
        self.on_click = lambda e: self.page.open(self.dialog)  # Действие по клику: открытие диалога
        self.tooltip = "Разблокировать"  # Надпись при наведении

        self.__access = Access(self.page) # Инициализация класса доступа

        self.dialog = ft.AlertDialog(  # Диалоговое окно с полем для ввода пароля
            content=ft.TextField(  # Поле ввода пароля
                border_color="#A9A9A9",
                width=150,
                height=110,
                text_size=42,
                text_vertical_align=0.0,
                show_cursor=False,
                text_align=ft.TextAlign.CENTER,
                text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=8, size=42, color='#A9A9A9'),
                value='',
                max_length=6,
                on_change=self.verify,
                input_filter=ft.NumbersOnlyInputFilter(),
                autofocus=True,
                border_width=3.5,
                border_radius=21,
                counter_text="Одноразовый код",
                counter_style=ft.TextStyle(weight=ft.FontWeight.W_900),
                expand=True
            ),
            actions_padding=0,  # Убирает все отступы
            title_padding=0,  # Убирает все отступы
            inset_padding=0,  # Убирает все отступы
            on_dismiss=lambda e: (setattr(self.dialog.content, 'value', ''), self.page.update())  # Делает поле пустым после скрытия
        )

    async def block(self, e):
        """
        Блокировка по нажатию
        Меняет иконку на красную
        Передаёт в класс Access команду блокировки
        """
        await self.__access.block()  # Вызов метода блокировки
        self.tooltip = "Разблокировать"  # Изменяет надпись
        self.on_click = lambda e: self.page.open(self.dialog)  # Переключает действие на открытие окна разблокировки
        self.dialog.content.value = ''  # Делает поле пустым после скрытия
        self.dialog.content.border_color = "#A9A9A9"  # Убирает зелёный окрас рамки после разблокировки
        self.content = ft.Image(src='iconRed.png', height=32.5)  # Импорт логотипа
        self.page.update()


    async def verify(self, e):
        """
        Разблокировка по нажатию и вводу кода
        Меняет иконку на зелёную, если успешно
        Передаёт в класс Access команду разблокировки
        """
        self.dialog.content.border_color = "#A9A9A9"  # Возвращает белый окрас
        if len(e.data) == 6:  # Не реагирует, пока не введены все 6 символов
            if await self.__access.unblock(e.data):  # Проверка кода через 2FA + вызов метода разблокировки
                self.tooltip = "Заблокировать"  # Изменяет надпись при наведении
                self.content = ft.Image(src='iconGreen.png', height=32.5)  # Импорт логотипа
                self.dialog.content.value = ''  # Делает поле пустым
                self.dialog.content.border_color = "#09FF00"  # Окрашивает в зелёный как индикатор успеха
                self.on_click = self.block  # Переключает функцию по клику на блокировку
                self.page.close(self.dialog)  # Закрывает диалоговое окно
                self.page.update() # Обновляет страницу
            else:
                self.dialog.content.border_color = '#FF0000'  # Окрашивает в красный как индикатор неудачи
        self.update()  # Обновление