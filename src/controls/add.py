import flet as ft


class AddButton(ft.FloatingActionButton):
    """
    Кнопка добавления устройства на страницу
    Отображается при разрешённом доступе
    """
    def __init__(self) -> None:
        super().__init__() # Наследование
        self.icon: str = ft.icons.ADD  # Иконка плюсика в кнопке
        self.visible: bool = False  # По умолчанию отключает видимость
        self.bgcolor = "#A9A9A9"

    def did_mount(self) -> None:
        """
        Наследуемая функция от Flet
        Костыль для получения page после иницилизации оной
        """
        self.on_click = lambda e: self.page.open(self.dialog)  # Открывает диалог по клику
        self.factory_number_text_field: ft.TextField = ft.TextField( # Поле ввода завномера
            width=250,
            value='',
            border_color="#A9A9A9",
            text_size=19,
            text_vertical_align=0.0,
            height=50,
            on_change=self.check,
            show_cursor=False,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=2, size=42, color="#000000"),
            border_width=3.5,
            border_radius=28,
            label='Заводской номер',
            label_style=ft.TextStyle(weight=ft.FontWeight.W_700, color='#000000'),
        )
        self.device_dropdown: ft.Dropdown = ft.Dropdown(  # Дропдаун выбора устройства
            width=250,
            border_radius=28,
            border_width=3.5,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_700, size=14, color="#000000"),
            height=50,
            border_color="#A9A9A9",
            label='Продукт',
            label_style=ft.TextStyle(weight=ft.FontWeight.W_700, color='#000000'),
            options=[
                ft.dropdown.Option(x) for x in self.page.config.devices.titles[:-1]
            ]
        )
        self.stand_dropdown: ft.Dropdown = ft.Dropdown(  # Дропдаун выбора стенда
            width=250,
            border_radius=28,
            border_width=3.5,
            height=50,
            border_color="#A9A9A9",
            label_style=ft.TextStyle(weight=ft.FontWeight.W_700, color='#000000'),
            text_style=ft.TextStyle(weight=ft.FontWeight.W_700, size=14, color="#000000"),
            on_change=lambda e: (  # При выборе стенда DCT запрещает добавлять любое другое устройство
                setattr(self.device_dropdown, 'value', 'DCT' if e.data == 'Ресурсные испытания DCT' else self.device_dropdown.value),
                setattr(self.device_dropdown, 'disabled', True if e.data == 'Ресурсные испытания DCT' else False),
                self.dialog.update()
            ),
            label='Стенд',
            options=[
                ft.dropdown.Option(x) for x in self.page.config.stands.titles
            ]
        )
        self.dialog: ft.AlertDialog = ft.AlertDialog(  # Диалог, открывающийся по нажатию
            title=ft.Row( # Напись добавить и плюсик в заголовке
                [
                    ft.Text('Добавить', style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="#000000")),
                    ft.Icon(ft.icons.ADD, size=30, color='#000000')
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=200
            ),
            content=ft.Column(  # Содержимое
                [
                    self.stand_dropdown,
                    self.device_dropdown,
                    self.factory_number_text_field
                ],
                width=250,
                height=230,
                spacing=28,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            modal=True,
            actions=[  # Действия, доступные из диалога
                ft.FilledButton(
                    "Подтвердить",
                    on_click=self.add,
                    disabled=True,
                    color='#FFFFFF',
                    bgcolor='#000000'
                ),
                ft.FilledButton(
                    "Отмена",
                    on_click=self.close_dialog,
                    color='#FFFFFF',
                    bgcolor='#6C757D'
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    async def close_dialog(self, e):
        """
        Закрывает диалог и подчищает предыдущие вводы
        и выбранные в дропдаунах строки
        """
        self.page.close(self.dialog)  # Закрытие самого диалога
        self.stand_dropdown.value = ''  # Очищает поле выбора стенда
        self.factory_number_text_field.value = ''  # Очищает поле ввода серийного номера
        self.device_dropdown.value = ''  # Очищает поле выбора устройства
        self.dialog.actions[0].disabled = True  # Отключает кнопку добавления


    async def check(self, e):
        """
        Проверяет поле ввода на наличие символов
        При отсутствии оных выключает кликабельность кнопки добавления
        """
        if e.data != '':  # Проверка
            self.dialog.actions[0].disabled = False # Отключает, если пусто
        else:
            self.dialog.actions[0].disabled = True  # Включает, если есть символы
        self.dialog.update()  # Обновление


    async def add(self, e):
        """
        Передаёт в область указ о добавление нового устройства
        После вызывает функцию закрытия, которая всё подчищает
        """
        stand = self.stand_dropdown.value # Сохрание информации о стенда
        factory_number = self.factory_number_text_field.value  # Сохрание информации о завномере
        device = self.device_dropdown.value if stand != 'Ресурсные испытания DCT' else 'DCT'  # Сохранение информации о типе устройства
        dialog = self.page.area.info(device).add_dialog
        self.page.open(dialog(stand, factory_number, device))
        await self.close_dialog(e)