import flet as ft


class DialogTextField(ft.TextField):
    def __init__(self, **kwargs):
        super().__init__()
        self.width = 135
        self.value = ''
        self.border_color = "#A9A9A9"
        self.text_size = 19
        self.text_vertical_align = 0.0
        self.height = 50
        self.text_align = ft.TextAlign.CENTER
        self.text_style = ft.TextStyle(weight=ft.FontWeight.W_600, size=19, color='#000000')
        self.border_width = 2
        self.border_radius = 28
        self.label_style = ft.TextStyle(weight=ft.FontWeight.W_600, color='#000000')

        for key, value in kwargs.items():
            setattr(self, key, value)


class RsTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            input_filter=ft.NumbersOnlyInputFilter(),
            label='Modbus ID RS485',
            **kwargs
        )

class ConcentrationTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            label='Концентрация',
            **kwargs
        )

class OwenIdTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            input_filter=ft.NumbersOnlyInputFilter(),
            label='Modbus ID OWEN',
            **kwargs
        )


class OwenChannelTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            input_filter=ft.NumbersOnlyInputFilter(),
            label='Номер в OWEN',
            **kwargs
        )


class GasTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(label='Газ', **kwargs)


class AmperageTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            label='Ток: 4-20mA',
            **kwargs
        )


class ModifiedAmperageTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            label='Ток: ед.изм.',
            **kwargs
        )


class AmperageLowTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(label='Ток\nНиз', **kwargs)


class AmperageHighTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(label='Ток\nВерх', **kwargs)


class FirstThresholdTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(label='Порог 1', **kwargs)


class SecondThresholdTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(label='Порог 2', **kwargs)


class CommentTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(
            height = 150,
            multiline=True,
            min_lines = 10,
            text_vertical_align = 0.0,
            text_align=ft.TextAlign.START,
            border_width = 3.5,
            border_radius = 70,
            content_padding = 30,
            label = 'Комментарий',
            label_style = ft.TextStyle(weight=ft.FontWeight.W_600, size=25, color='#000000'),
            **kwargs
        )


class SgmChannelTextField(DialogTextField):
    def __init__(self, **kwargs):
        super().__init__(label='Канал СГМ-130', **kwargs)


class DialogDropdown(ft.Dropdown):
    def __init__(self, **kwargs):
        super().__init__()
        self.width = 135
        self.alignment = ft.alignment.center
        self.border_radius = 28
        self.border_width = 2
        self.text_style = ft.TextStyle(weight=ft.FontWeight.W_600, size=19, color='#000000')
        self.height = 50
        self.border_color = "#A9A9A9"
        self.label_style = ft.TextStyle(weight=ft.FontWeight.W_600, color='#000000')

        for key, value in kwargs.items():
            setattr(self, key, value)


class UnitDropdown(DialogDropdown):
    def __init__(self, **kwargs):
        options = [
                ft.dropdown.Option('%НКПР'),
                ft.dropdown.Option('%об.д.'),
                ft.dropdown.Option('мг/м³'),
                ft.dropdown.Option('ppm'),
                ft.dropdown.Option('ppb')
        ]
        super().__init__(
            label='Ед. изм.',
            options=options,
            **kwargs
        )


class DiscretenessDropdown(DialogDropdown):
    def __init__(self, **kwargs):
        options = [
            ft.dropdown.Option('1'),
            ft.dropdown.Option('10'),
            ft.dropdown.Option('100')
        ]
        super().__init__(
            label='Дискрет.',
            options=options,
            **kwargs
        )


class StatusDropdown(DialogDropdown):
    def __init__(self, **kwargs):
        options = [
            ft.dropdown.Option("АВАРИЯ"),
            ft.dropdown.Option("ПОРОГ 1"),
            ft.dropdown.Option("ПОРОГ 2"),
            ft.dropdown.Option("ИНИЦИАЛИЗАЦИЯ"),
            ft.dropdown.Option("НОРМА"),
            ft.dropdown.Option("ОБРЫВ"),
            ft.dropdown.Option("ПРЕВЫШЕНИЕ СИГНАЛА"),
        ]
        super().__init__(
            label='Статус',
            options=options,
            **kwargs
        )


class DialogCheckbox(ft.Checkbox):
    def __init__(self, **kwargs):
        super().__init__()
        self.value = True
        self.width = 135
        self.label_style = ft.TextStyle(weight=ft.FontWeight.W_600, size=17, color='#000000')
        self.fill_color = '#096EFD'

        for key, value in kwargs.items():
            setattr(self, key, value)


class RsCheckbox(DialogCheckbox):
    def __init__(self, **kwargs):
        super().__init__(label='   RS485   ', **kwargs)


class AmperageCheckbox(DialogCheckbox):
    def __init__(self, **kwargs):
        super().__init__(label='Ток: ед.изм.', **kwargs)

class ModifiedAmperageCheckbox(DialogCheckbox):
    def __init__(self, **kwargs):
        super().__init__(label='Ток: 4-20mA', **kwargs)


class DeleteDialog(ft.AlertDialog):
    def __init__(
            self,
            factory_number: str,
            device
    ) -> None:
        super().__init__()
        self.modal = True
        self.device = device
        self.factory_number = factory_number
        self.title = ft.Row(
            [
                ft.Text(f'Удаление', weight=ft.FontWeight.W_900),
                ft.Icon(ft.icons.DELETE)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=200
        )
        self.content = ft.Text(f'Вы уверены, что хотите удалить навсегда устройство {self.factory_number}?')
        self.actions = [
            ft.TextButton('Да', on_click=self.delete),
            ft.TextButton('Нет', on_click=lambda e: self.page.close(self))
        ]

    async def delete(self, e):
        await self.page.area.delete(self.factory_number, self.device)
        self.page.close(self)


class AdvantRow(ft.Row):
    def __init__(self, controls: list):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 17.5
        self.width = 287.5
        self.controls = controls


class AdvantChannelColumn(ft.Column):
    def __init__(self, controls: list):
        super().__init__()
        self.width = 287.5
        self.height = 470
        self.spacing = 35
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER
        self.controls = controls