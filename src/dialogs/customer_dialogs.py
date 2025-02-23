import flet as ft
from .dialog import *
from .user_dialogs import *
from .custom_contorols import *


class DgsCustomerAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)

        self.status_dropdown: StatusDropdown= StatusDropdown(width=270)

        self.basic_data_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                UnitDropdown(width=125),
                GasTextField(width=125)
            ]
        )

        self.row_list = [
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=25,
                controls=[
                    checkbox(width=135),
                    #text_field(width=110)
                ]
            )
            for checkbox in
                [
                    RsCheckbox,
                    AmperageCheckbox,
                    ModifiedAmperageCheckbox
                ]
                # [
                #     ConcentrationTextField,
                #     AmperageTextField,
                #     ModifiedAmperageTextField
                # ]

        ]

        self.content = ft.Column(
            [
                self.status_dropdown,
                self.basic_data_row,
                *self.row_list
            ],
            width=270,
            height=275,
            spacing=25
        )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "unit": self.basic_data_row.controls[0].value,
            "gas": self.basic_data_row.controls[1].value,
            "show_rs485": self.content.controls[2].controls[0].value,
            "show_modified_amperage": self.content.controls[4].controls[0].value,
            "show_amperage": self.content.controls[3].controls[0].value,
            "concentration": 0.0,
            "amperage": 0.0,
            "modified_amperage": 0.0,
            # "concentration": float(self.content.controls[2].controls[1].value),
            # "amperage": float(self.content.controls[3].controls[1].value),
            # "modified_amperage": float(self.content.controls[4].controls[1].value),
            "status": self.status_dropdown.value
        }


class Dgs210CustomerAddDialog(DgsCustomerAddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)


class Dgs230CustomerAddDialog(DgsCustomerAddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)


class AdvantCustomerAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
            super().__init__(stand, factory_number, device)


            self.first_channel_basic_data_row = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=17.5,
                width=287.5,
                controls=[
                    UnitDropdown(width=135),
                    GasTextField(width=135)
                ]
            )
            self.second_channel_basic_data_row = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=17.5,
                width=287.5,
                controls=[
                    UnitDropdown(width=135),
                    GasTextField(width=135)
                ]
            )
            self.first_channel_concentration_row = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=17.5,
                width=287.5,
                controls=[
                    ConcentrationTextField(width=135)
                ]
            )
            self.second_channel_concentration_row = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=17.5,
                width=287.5,
                controls=[
                    ConcentrationTextField(width=135)
                ]
            )
            self.first_channel_amperage_settings_row = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=17.5,
                width=287.5,
                controls=[
                    AmperageTextField(width=135),
                    ModifiedAmperageTextField(width=135)
                ]
            )
            self.second_channel_amperage_settings_row = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=17.5,
                width=287.5,
                controls=[
                    AmperageTextField(width=135),
                    ModifiedAmperageTextField(width=135)
                ]
            )
            self.device_settings_column: ft.Column = ft.Column(
                width=287.5,
                height=280,
                spacing=35,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    RsCheckbox(width=135),
                    AmperageCheckbox(width=135),
                    ModifiedAmperageCheckbox(width=135)
                ]
            )
            self.first_channel_column: ft.Column = ft.Column(
                width=287.5,
                height=280,
                spacing=35,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    StatusDropdown(width=287.5),
                    self.first_channel_basic_data_row,
                    # self.first_channel_concentration_row,
                    # self.first_channel_amperage_settings_row
                ]
            )
            self.second_channel_column: ft.Column = ft.Column(
                width=287.5,
                height=280,
                spacing=35,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    StatusDropdown(width=287.5),
                    self.second_channel_basic_data_row,
                    # self.second_channel_concentration_row,
                    # self.second_channel_amperage_settings_row
                ]
            )
            self.content: ft.Tabs = ft.Tabs(
                selected_index=0,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="Общие",
                        icon=ft.icons.SETTINGS,
                        content=self.device_settings_column
                    ),
                    ft.Tab(
                        text="Канал 1",
                        icon=ft.icons.WIFI_TETHERING,
                        content=self.first_channel_column,
                    ),
                    ft.Tab(
                        text="Канал 2",
                        icon=ft.icons.WIFI_TETHERING,
                        content=self.second_channel_column,
                    ),
                ],
                expand=1,
                width=330,
                height=280,
            )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "show_rs485": self.device_settings_column.controls[0].value,
            "show_modified_amperage": self.device_settings_column.controls[2].value,
            "show_amperage": self.device_settings_column.controls[1].value,
            "unit_ch1": self.first_channel_basic_data_row.controls[0].value,
            "gas_ch1": self.first_channel_basic_data_row.controls[1].value,
            "amperage_ch1": 0.0,
            "modified_amperage_ch1": 0.0,
            "concentration_ch1": 0.0,
            # "amperage_ch1": float(self.first_channel_amperage_settings_row.controls[0].value),
            # "modified_amperage_ch1": float(self.first_channel_amperage_settings_row.controls[1].value),
            # "concentration_ch1": float(self.first_channel_concentration_row.controls[0].value),
            "status_ch1": self.first_channel_column.controls[0].value,
            "unit_ch2": self.second_channel_basic_data_row.controls[0].value,
            "gas_ch2": self.second_channel_basic_data_row.controls[1].value,
            "amperage_ch2": 0.0,
            "modified_amperage_ch2": 0.0,
            "concentration_ch2": 0.0,
            # "amperage_ch2": float(self.second_channel_amperage_settings_row.controls[0].value),
            # "modified_amperage_ch2": float(self.second_channel_amperage_settings_row.controls[1].value),
            # "concentration_ch2": float(self.second_channel_concentration_row.controls[0].value),
            "status_ch2": self.second_channel_column.controls[0].value
        }


class XsCustomerAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
            super().__init__(stand, factory_number, device)
            self.visibility_row: ft.Row = AdvantRow(
                controls=[
                    AmperageCheckbox(width=135),
                    ModifiedAmperageCheckbox(width=135)
                ]
            )
            self.amperage_settings_row: ft.Row = AdvantRow(
                controls=[
                    AmperageTextField(width=135),
                    ModifiedAmperageTextField(width=135)
                ]
            )
            self.basic_data_row: ft.Row = AdvantRow(
                controls=[
                    UnitDropdown(width=135),
                    GasTextField(width=135)
                ]
            )
            self.status_dropdown: ft.Dropdown = StatusDropdown(width=287.5)
            self.content = ft.Column(
                width=287.5,
                height=190,
                spacing=35,
                controls=[
                    self.basic_data_row,
                    self.visibility_row,
                    #self.amperage_settings_row,
                    self.status_dropdown
                ]
            )
    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "unit": self.basic_data_row.controls[0].value,
            "gas": self.basic_data_row.controls[1].value,
            "show_modified_amperage": self.visibility_row.controls[1].value,
            "show_amperage": self.visibility_row.controls[0].value,
            # "modified_amperage": float(self.amperage_settings_row.controls[1].value),
            # "amperage": float(self.amperage_settings_row.controls[0].value),
            "modified_amperage": 0.0,
            "amperage": 0.0,
            'status': self.status_dropdown.value,
            "show_rs485": False,
            "concentration": 0.0
        }


class DctCustomerAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
            super().__init__(stand, factory_number, device)
            self.visibility_row: ft.Row = AdvantRow(
                controls=[
                    AmperageCheckbox(width=135),
                    ModifiedAmperageCheckbox(width=135)
                ]
            )
            self.amperage_settings_row: ft.Row = AdvantRow(
                controls=[
                    AmperageTextField(width=135),
                    ModifiedAmperageTextField(width=135)
                ]
            )
            self.basic_data_row: ft.Row = AdvantRow(
                controls=[
                    UnitDropdown(width=135),
                    GasTextField(width=135)
                ]
            )
            self.status_dropdown: ft.Dropdown = StatusDropdown(width=287.5)
            self.content = ft.Column(
                width=287.5,
                height=190,
                spacing=35,
                controls=[
                    self.basic_data_row,
                    self.visibility_row,
                   # self.amperage_settings_row,
                    self.status_dropdown
                ]
            )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": "Ресурсные испытания DCT",
            "unit": self.basic_data_row.controls[0].value,
            "gas": self.basic_data_row.controls[1].value,
            "show_modified_amperage": self.visibility_row.controls[1].value,
            "show_amperage": self.visibility_row.controls[0].value,
            "modified_amperage": 0.0,
            "amperage": 0.0,
            # "modified_amperage": float(self.amperage_settings_row.controls[1].value),
            # "amperage": float(self.amperage_settings_row.controls[0].value),
            'status': self.status_dropdown.value,
            "show_rs485": False,
            "concentration": 0.0
        }


class DgsCustomerEditDialog(DgsCustomerAddDialog):
    def __init__(self, model):
        super().__init__(
            model.stand,
            model.factory_number,
            type(model)
        )
        self.model = model
        self.actions = [
            ft.TextButton(
                'Удалить',
                style=ft.ButtonStyle(color='#FF0000'),
                on_click=lambda e: self.page.open(DeleteDialog(self.model.factory_number, type(model)))
            ),
            ft.FilledButton(
                'Сохранить',
                on_click=self.save,
                color='#FFFFFF',
                bgcolor='#000000'
            ),
            ft.FilledButton(
                'Отмена',
                on_click=lambda e: self.page.close(self),
                color='#FFFFFF',
                bgcolor='#6C757D'
            )
        ]

    def did_mount(self):
        links = {
            "unit": self.basic_data_row.controls[0],
            "gas": self.basic_data_row.controls[1],
            "show_rs485": self.content.controls[2].controls[0],
            "show_modified_amperage": self.content.controls[4].controls[0],
            "show_amperage": self.content.controls[3].controls[0],
            #"concentration": self.content.controls[2].controls[1],
            #"amperage": self.content.controls[3].controls[1],
            #"modified_amperage": self.content.controls[4].controls[1],
            "status": self.status_dropdown
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()


class Dgs210CustomerEditDialog(DgsCustomerEditDialog):
    def __init__(self, model):
        super().__init__(model)


class Dgs230CustomerEditDialog(DgsCustomerEditDialog):
    def __init__(self, model):
        super().__init__(model)


class AdvantCustomerEditDialog(AdvantCustomerAddDialog):
    def __init__(self, model):
        super().__init__(
            model.stand,
            model.factory_number,
            type(model)
        )
        self.model = model
        self.actions = [
            ft.TextButton(
                'Удалить',
                style=ft.ButtonStyle(color='#FF0000'),
                on_click=lambda e: self.page.open(DeleteDialog(self.model.factory_number, type(model)))
            ),
            ft.FilledButton(
                'Сохранить',
                on_click=self.save,
                color='#FFFFFF',
                bgcolor='#000000'
            ),
            ft.FilledButton(
                'Отмена',
                on_click=lambda e: self.page.close(self),
                color='#FFFFFF',
                bgcolor='#6C757D'
            )
        ]

    def did_mount(self):
        links = {
            "show_rs485": self.device_settings_column.controls[0],
            "show_modified_amperage": self.device_settings_column.controls[2],
            "show_amperage": self.device_settings_column.controls[1],
            "unit_ch1": self.first_channel_basic_data_row.controls[0],
            "gas_ch1": self.first_channel_basic_data_row.controls[1],
            # "amperage_ch1": self.first_channel_amperage_settings_row.controls[0],
            # "modified_amperage_ch1": self.first_channel_amperage_settings_row.controls[1],
            # "concentration_ch1": self.first_channel_concentration_row.controls[0],
            "status_ch1": self.first_channel_column.controls[0],
            "unit_ch2": self.second_channel_basic_data_row.controls[0],
            "gas_ch2": self.second_channel_basic_data_row.controls[1],
            # "amperage_ch2": self.second_channel_amperage_settings_row.controls[0],
            # "modified_amperage_ch2": self.second_channel_amperage_settings_row.controls[1],
            # "concentration_ch2": self.second_channel_concentration_row.controls[0],
            "status_ch2": self.second_channel_column.controls[0],
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()


class XsCustomerEditDialog(XsCustomerAddDialog):
    def __init__(self, model):
        super().__init__(
            model.stand,
            model.factory_number,
            type(model)
        )
        self.model = model
        self.actions = [
            ft.TextButton(
                'Удалить',
                style=ft.ButtonStyle(color='#FF0000'),
                on_click=lambda e: self.page.open(DeleteDialog(self.model.factory_number, type(model)))
            ),
            ft.FilledButton(
                'Сохранить',
                on_click=self.save,
                color='#FFFFFF',
                bgcolor='#000000'
            ),
            ft.FilledButton(
                'Отмена',
                on_click=lambda e: self.page.close(self),
                color='#FFFFFF',
                bgcolor='#6C757D'
            )
        ]

    def did_mount(self):
        links = {
            "unit": self.basic_data_row.controls[0],
            "gas": self.basic_data_row.controls[1],
            "show_modified_amperage": self.visibility_row.controls[1],
            "show_amperage": self.visibility_row.controls[0],
            #"modified_amperage": self.amperage_settings_row.controls[1],
            #"amperage": self.amperage_settings_row.controls[0],
            'status': self.status_dropdown,
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()


class DctCustomerEditDialog(DctCustomerAddDialog):
    def __init__(self, model):
        super().__init__(
            model.stand,
            model.factory_number,
            type(model)
        )
        self.model = model
        self.actions = [
            ft.TextButton(
                'Удалить',
                style=ft.ButtonStyle(color='#FF0000'),
                on_click=lambda e: self.page.open(DeleteDialog(self.model.factory_number, type(model)))
            ),
            ft.FilledButton(
                'Сохранить',
                on_click=self.save,
                color='#FFFFFF',
                bgcolor='#000000'
            ),
            ft.FilledButton(
                'Отмена',
                on_click=lambda e: self.page.close(self),
                color='#FFFFFF',
                bgcolor='#6C757D'
            )
        ]

    def did_mount(self):
        links = {
            "unit": self.basic_data_row.controls[0],
            "gas": self.basic_data_row.controls[1],
            "show_modified_amperage": self.visibility_row.controls[1],
            "show_amperage": self.visibility_row.controls[0],
            #"modified_amperage": self.amperage_settings_row.controls[1],
            #"amperage": self.amperage_settings_row.controls[0],
            'status': self.status_dropdown,
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()
