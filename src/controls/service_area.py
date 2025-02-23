import flet as ft
from sqlalchemy import select
from src.database import *


class ActionButton(ft.Container):
    def __init__(
            self,
            icon,
            icon_color,
            text,
            area
    ):
        super().__init__()
        self.area = area
        self.text = ft.Text(
            value=text,
            style=ft.TextStyle(
                weight=ft.FontWeight.W_600,
                size=17
            )
        )
        self.icon = ft.Icon(color=icon_color, name=icon)
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.text,
                self.icon
            ]
        )
        self.padding = 5
        self.border = ft.border.all(2, "#A9A9A9")
        self.border_radius = 20
        self.height = 50
        self.width = 150
        self.ink = True
        self.on_click = lambda _: None



class ReloadButton(ActionButton):
    def __init__(self, area):
        super().__init__(
            ft.icons.CACHED,
            "009AFF",
            'Ещё',
            area
        )
        self.on_click = area.reload

class SendButton(ActionButton):
    def __init__(self, area):
        super().__init__(
            ft.icons.SEND,
            "#00FF33",
            'Отправить',
            area
        )
        self.on_click = area.send

class TerminateButton(ActionButton):
    def __init__(self, area):
        super().__init__(
            ft.icons.CANCEL,
            "#FF0000",
            'Сброс',
            area
        )
        self.on_click = area.terminate


class ParameterTextField(ft.TextField):
    def __init__(self, area):
        super().__init__()
        self.area = area
        self.disabled = True
        self.label = 'Конц. коррект. газа'
        self.width = 180
        self.value = ''
        self.border_color = "#A9A9A9"
        self.text_size = 19
        self.text_vertical_align = 0.0
        self.height = 50
        self.text_align = ft.TextAlign.CENTER
        self.text_style = ft.TextStyle(weight=ft.FontWeight.W_600, size=19)
        self.border_width = 2
        self.border_radius = 20
        self.label_style = ft.TextStyle(weight=ft.FontWeight.W_600)


class ActionDropdown(ft.Dropdown):
    def __init__(self, button_row, area):
        super().__init__()
        self.area = area
        self.button_row = button_row
        self.width = 320
        self.value = 'Вход в сервисный режим'
        self.alignment = ft.alignment.center
        self.text_vertical_align = ft.VerticalAlignment.CENTER
        self.border_radius = 20
        self.border_width = 2
        self.text_style = ft.TextStyle(weight=ft.FontWeight.W_600, size=19, color='#000000')
        self.height = 50
        self.border_color = "#A9A9A9"
        self.label_style = ft.TextStyle(weight=ft.FontWeight.W_600)
        self.options = [
            ft.dropdown.Option("Вход в сервисный режим"),
            ft.dropdown.Option("Выход из сервисного режима"),
            #ft.dropdown.Option("Выход в рабочий режим"),
            ft.dropdown.Option("Корректировка нуля"),
            ft.dropdown.Option("Корректировка концентрации"),
            # ft.dropdown.Option("Корректировка точки 4мА"),
            # ft.dropdown.Option("Корректировка точки 20 мА"),
            # ft.dropdown.Option("Тестирование токового выхода"),
            ft.dropdown.Option("Cохранение изменений")
        ]
        self.on_change = self.check

    async def check(self, e):
        if e.data == 'Корректировка концентрации':
            status = False
        else:
            status = True
        self.button_row.parameter_text_field.disabled = status
        self.button_row.update()


class ButtonRow(ft.Row):
    def __init__(self, area):
        super().__init__()
        self.area = area
        self.action_dropdown = ActionDropdown(self, area)
        self.parameter_text_field = ParameterTextField(area)
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.send_button = SendButton(area)
        self.reload_button = ReloadButton(area)
        self.terminate_button = TerminateButton(area)
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            self.action_dropdown,
            self.parameter_text_field,
            self.send_button,
            self.reload_button,
            self.terminate_button,
        ]

base_gradient =  ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    "0xdddddd",
                    "0xa5a5a5"
                ],
                tile_mode=ft.GradientTileMode.MIRROR
        )
class DgsLine(ft.Container):
    def __init__(
            self,
            factory_number,
            slave_id,
            area
    ):
        super().__init__()
        self.area = area
        self.height = 35
        self.width = 210
        self.padding = 5
        style = ft.TextStyle(
            color="#FFFFFF",
            size=19,
            weight=ft.FontWeight.W_700
        )
        self.slave_id_text = ft.Text(
            slave_id,
            style=style,
        )
        self.factory_number_text = ft.Text(
            factory_number,
            style=style,
        )
        self.gradient = base_gradient
        self.checkbox = ft.Checkbox(
            value=False,
            border_side=ft.BorderSide(color='#A9A9A9', width=0),
            fill_color={
                ft.ControlState.PRESSED: '#096EFD',
                ft.ControlState.SELECTED: '#096EFD',
                ft.ControlState.DEFAULT: '#A9A9A9'
            }
        )
        self.border_radius = 10
        self.content = ft.Row(
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.slave_id_text,
                self.factory_number_text,
                self.checkbox
            ]
        )


class DeviceContainer(ft.Container):
    def __init__(self, title: str, area):
        super().__init__()
        self.area = area
        self.width = self.area.width
        self.title = ft.Text(
            title,
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=20,
                weight=ft.FontWeight.W_800,
                color="#A9A9A9"
            ))
        self.device_row = ft.Row(
            spacing=15,
            wrap=True,
            expand=True
        )
        self.content = ft.Column(
            spacing=12,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                self.title,
                self.device_row
            ]
        )
        self.padding = 10
        self.border_radius = 20
        self.border = ft.border.all(3, '#A9A9A9')


class DeviceColumn(ft.Column):
    def __init__(self, area):
        super().__init__()
        self.expand = True
        self.area = area
        self.spacing = 20
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.dgs_210_container = DeviceContainer('ЭРИС ДГС-210', area)
        self.dgs_230_container = DeviceContainer('ЭРИС ДГС-230', area)
        #self.advant_container = DeviceContainer('Advant 2')
        self.controls = [
            self.dgs_210_container,
            self.dgs_230_container,
           # self.advant_container
        ]


class ServiceArea(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 20
        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.button_row = ButtonRow(self)
        self.device_column = DeviceColumn(self)
        self.controls = [
            self.button_row,
            self.device_column
        ]

    def did_mount(self):
        self.page.run_task(self.run)

    async def fill_device_row(self, row: ft.Row, title):
        models = {
            'ЭРИС ДГС-210': Dgs210User,
            'ЭРИС ДГС-230': Dgs230User,
        }
        devices = []
        async with self.page.db() as session:
            result = await session.execute(select(models[title]))
            devices += result.scalars().all()
        row.controls = [DgsLine(x.factory_number, x.slave_id, self) for x in devices]
        row.update()


    async def send(self, e):
        actions = {
            "Вход в сервисный режим": [3, 128],
            "Выход из сервисного режима": [3, 0],
            #"Выход в рабочий режим": [12, 0],
            "Корректировка нуля": [12, 6237],
            "Корректировка концентрации": [12, 25796],
            # "Корректировка точки 4мА": [12, 21808],
            # "Корректировка точки 20 мА": [12, 21955],
            # "Тестирование токового выхода": [12, 13621],
            "Cохранение изменений": [12, 29332]
        }
        for x in self.params['dgs210'] + self.params['dgs230']:
            x.disabled = True
        self.params['action'].disabled = True
        self.params['data'].disabled = True
        dgs210 = [x for x in self.params['dgs210'] if x.checkbox.value]
        dgs230 = [x for x in self.params['dgs230'] if x.checkbox.value]
        all_devices = dgs210+dgs230
        action = self.params['action'].value
        data = self.params['data'].value
        self.button_row.terminate_button.disabled = True
        self.button_row.reload_button.disabled = True
        self.button_row.send_button.disabled = True
        self.update()
        devices = [x.slave_id_text.value for x in all_devices]
        result = await self.page.socket.set(devices, *actions[action])
        error_gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                "0xf5404b",
                "0xb6133a"
            ],
            tile_mode=ft.GradientTileMode.MIRROR
        )
        for d in all_devices:
            if result['status'] == 200:
                try:
                    if result[str(d.slave_id_text.value)] == 200:
                        d.gradient = ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=[
                                "0x4fe39c",
                                "0x1bbdb3"
                            ],
                            tile_mode=ft.GradientTileMode.MIRROR
                    )
                    else:
                        d.gradient = error_gradient
                except Exception as e:
                    d.bgcolor = error_gradient
            else:
                d.bgcolor = error_gradient
        self.button_row.terminate_button.disabled = False
        self.button_row.reload_button.disabled = False
        self.button_row.send_button.disabled = False
        self.update()

    async def reload(self, e):
        for x in self.params['dgs210'] + self.params['dgs230']:
            x.disabled = False
            x.bgcolor = base_gradient
        self.params['data'].disabled = False if self.params['action'].value == 'Корректировка концентрации' else True
        self.params['action'].disabled = False
        self.update()

    async def terminate(self, e):
        for x in self.params['dgs210'] + self.params['dgs230']:
            x.disabled = False
            x.bgcolor = base_gradient
            x.checkbox.value = False
        self.params['data'].disabled = True
        self.params['data'].value = ''
        self.params['action'].disabled = False
        self.params['action'].value = 'Вход в сервисный режим'
        self.update()

    async def run(self):
        for container in self.device_column.controls:
            await self.fill_device_row(container.device_row, container.title.value)

    @property
    def params(self):
        return {
            'dgs210': self.device_column.dgs_210_container.device_row.controls,
            'dgs230': self.device_column.dgs_230_container.device_row.controls,
            'action': self.button_row.action_dropdown,
            'data': self.button_row.parameter_text_field
        }