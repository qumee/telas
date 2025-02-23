import flet as ft
from .dialog import AddDialog
from .custom_contorols import *


class DgsUserAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)

        self.ids_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                RsTextField(),
                OwenIdTextField(),
                OwenChannelTextField()
            ]
        )

        self.basic_data_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                UnitDropdown(),
                DiscretenessDropdown(),
                GasTextField()
            ]
        )
        self.visibility_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                RsCheckbox(),
                AmperageCheckbox(),
                ModifiedAmperageCheckbox()
            ]
        )
        amperage_width = 99.375
        self.amperage_settings_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            width=450,
            controls=[
                AmperageLowTextField(width=amperage_width),
                AmperageHighTextField(width=amperage_width),
                FirstThresholdTextField(width=amperage_width),
                SecondThresholdTextField(width=amperage_width)
            ]

        )
        self.comment_text_field: ft.TextField = CommentTextField(width=450)
        self.content = ft.Column(
            [
                self.ids_row,
                self.basic_data_row,
                self.visibility_row,
                self.amperage_settings_row,
                self.comment_text_field
            ],
            width=450,
            height=465,
            spacing=35
        )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "unit": self.basic_data_row.controls[0].value,
            "gas": self.basic_data_row.controls[2].value,
            "comment": self.comment_text_field.value,
            "discreteness": int(self.basic_data_row.controls[1].value),
            "slave_id": int(self.ids_row.controls[0].value),
            "owen_id": int(self.ids_row.controls[1].value),
            "owen_channel": int(self.ids_row.controls[2].value),
            "show_rs485": self.visibility_row.controls[0].value,
            "show_modified_amperage": self.visibility_row.controls[2].value,
            "show_amperage": self.visibility_row.controls[1].value,
            "amperage_low": float(self.amperage_settings_row.controls[0].value),
            "amperage_high": float(self.amperage_settings_row.controls[1].value),
            "amperage_threshold1": float(self.amperage_settings_row.controls[2].value),
            "amperage_threshold2": float(self.amperage_settings_row.controls[3].value)
        }


class Dgs210UserAddDialog(DgsUserAddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)


class Dgs230UserAddDialog(DgsUserAddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)


class AdvantUserAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)

        #  Device
        self.rs485_settings_row: ft.Row = AdvantRow([
                RsTextField(width=135),
                RsCheckbox(width=135)
            ]
        )
        self.amperage_visibility_row: ft.Row = AdvantRow([
                AmperageCheckbox(width=135),
                ModifiedAmperageCheckbox(width=135)
            ]
        )
        self.comment_text_field: ft.TextField = CommentTextField(width=287.5)
        self.device_settings_column: ft.Column = ft.Column(
            width=287.5,
            height=380,
            spacing=35,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.rs485_settings_row,
                self.amperage_visibility_row,
                self.comment_text_field
            ]
        )

        #  First channel
        self.first_channel_gas_text_field: ft.TextField = GasTextField(width=287.5)
        self.first_channel_owen_row: AdvantRow = AdvantRow([
                OwenIdTextField(width=135),
                OwenChannelTextField(width=135)
            ]
        )
        self.first_channel_basic_data_row: AdvantRow = AdvantRow([
                UnitDropdown(width=135),
                DiscretenessDropdown(width=135)
            ]
        )
        self.first_channel_amperage_settings_row: AdvantRow = AdvantRow([
                AmperageLowTextField(width=135),
                AmperageHighTextField(width=135)
            ]
        )
        self.first_channel_thresholds_row: AdvantRow = AdvantRow([
                FirstThresholdTextField(width=135),
                SecondThresholdTextField(width=135)
            ]
        )
        self.first_channel_column: AdvantChannelColumn = AdvantChannelColumn([
                self.first_channel_gas_text_field,
                self.first_channel_owen_row,
                self.first_channel_basic_data_row,
                self.first_channel_amperage_settings_row,
                self.first_channel_thresholds_row
            ]
        )

        #  Second channel
        self.second_channel_gas_text_field: ft.TextField = GasTextField(width=287.5)
        self.second_channel_owen_row: AdvantRow = AdvantRow([
                OwenIdTextField(width=135),
                OwenChannelTextField(width=135)
            ]
        )
        self.second_channel_basic_data_row: AdvantRow = AdvantRow([
                UnitDropdown(width=135),
                DiscretenessDropdown(width=135)
            ]
        )
        self.second_channel_amperage_settings_row: AdvantRow = AdvantRow([
                AmperageLowTextField(width=135),
                AmperageHighTextField(width=135)
            ]
        )
        self.second_channel_thresholds_row: AdvantRow = AdvantRow([
                FirstThresholdTextField(width=135),
                SecondThresholdTextField(width=135)
            ]
        )
        self.second_channel_column: AdvantChannelColumn = AdvantChannelColumn([
                self.second_channel_gas_text_field,
                self.second_channel_owen_row,
                self.second_channel_basic_data_row,
                self.second_channel_amperage_settings_row,
                self.second_channel_thresholds_row
            ]
        )
        self.content = ft.Tabs(
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
                    content=self.second_channel_column ,
                ),
            ],
            width=330,
            height=470
        )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "slave_id": int(self.rs485_settings_row.controls[0].value),
            "comment": self.comment_text_field.value,
            "show_rs485": self.rs485_settings_row.controls[1].value,
            "show_modified_amperage": self.amperage_visibility_row.controls[1].value,
            "show_amperage": self.amperage_visibility_row.controls[0].value,
            "unit_ch1": self.first_channel_basic_data_row.controls[0].value,
            "gas_ch1": self.first_channel_gas_text_field.value,
            "discreteness_ch1": int(self.first_channel_basic_data_row.controls[1].value),
            "unit_ch2": self.second_channel_basic_data_row.controls[0].value,
            "gas_ch2": self.second_channel_gas_text_field.value,
            "discreteness_ch2": int(self.second_channel_basic_data_row.controls[1].value),
            "owen_id_ch1": int(self.first_channel_owen_row.controls[0].value),
            "owen_number_ch1": int(self.first_channel_owen_row.controls[1].value),
            "owen_id_ch2": int(self.second_channel_owen_row.controls[0].value),
            "owen_number_ch2": int(self.second_channel_owen_row.controls[1].value),
            "amperage_low_ch1": float(self.first_channel_amperage_settings_row.controls[0].value),
            "amperage_high_ch1": float(self.first_channel_amperage_settings_row.controls[1].value),
            "amperage_threshold1_ch1": float(self.first_channel_thresholds_row.controls[0].value),
            "amperage_threshold2_ch1": float(self.first_channel_thresholds_row.controls[1].value),
            "amperage_low_ch2": float(self.second_channel_amperage_settings_row.controls[0].value),
            "amperage_high_ch2": float(self.second_channel_amperage_settings_row.controls[1].value),
            "amperage_threshold1_ch2": float(self.second_channel_thresholds_row.controls[0].value),
            "amperage_threshold2_ch2": float(self.second_channel_thresholds_row.controls[1].value)
        }


class XsUserAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)

        self.rs_text_field: ft.TextField = RsTextField(width=287.5)

        self.visibility_row: ft.Row  = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                AmperageCheckbox(width=135),
                ModifiedAmperageCheckbox(width=135)
            ]
        )

        self.basic_data_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                UnitDropdown(width=135),
                GasTextField(width=135)
            ]
        )

        self.amperage_settings_row = AdvantRow(
            controls=[
                AmperageLowTextField(width=135),
                AmperageHighTextField(width=135)
            ]
        )

        self.threshold_settings_row = AdvantRow(
            controls=[
                FirstThresholdTextField(),
                SecondThresholdTextField()
            ]
        )

        self.comment_text_field: ft.TextField = CommentTextField(width=287.5)

        self.content = ft.Column(
            [
                self.rs_text_field,
                self.basic_data_row,
                self.visibility_row,
                self.amperage_settings_row,
                self.threshold_settings_row,
                self.comment_text_field
            ],
            width=287.5,
            height=570,
            spacing=35
        )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "unit": self.basic_data_row.controls[0].value,
            "gas": self.basic_data_row.controls[1].value,
            "comment": self.comment_text_field.value,
            "slave_id": int(self.rs_text_field.value),
            "show_rs485": False,
            "show_modified_amperage": self.visibility_row.controls[1].value,
            "show_amperage": self.visibility_row.controls[0].value,
            "amperage_low": float(self.amperage_settings_row.controls[0].value),
            "amperage_high": float(self.amperage_settings_row.controls[1].value),
            "amperage_threshold1": float(self.threshold_settings_row.controls[0].value),
            "amperage_threshold2": float(self.threshold_settings_row.controls[1].value)
        }


class DctUserAddDialog(AddDialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(stand, factory_number, device)

        self.channel_text_field: ft.TextField = SgmChannelTextField(width=287.5)

        self.visibility_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                AmperageCheckbox(width=135),
                ModifiedAmperageCheckbox(width=135)
            ]
        )

        self.basic_data_row: ft.Row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=17.5,
            controls=[
                UnitDropdown(width=135),
                GasTextField(width=135)
            ]
        )


        self.comment_text_field: ft.TextField = CommentTextField(width=287.5)

        self.content = ft.Column(
            [
                self.channel_text_field,
                self.basic_data_row,
                self.visibility_row,
                self.comment_text_field
            ],
            width=287.5,
            height=420,
            spacing=35
        )

    @property
    def links(self) -> dict[str:object]:
        return {
            "factory_number": self.factory_number,
            "stand": self.stand,
            "unit": self.basic_data_row.controls[0].value,
            "gas": self.basic_data_row.controls[1].value,
            "comment": self.comment_text_field.value,
            "channel": int(self.channel_text_field.value),
            "show_rs485": False,
            "show_modified_amperage": self.visibility_row.controls[1].value,
            "show_amperage": self.visibility_row.controls[0].value,
        }


class DgsUserEditDialog(DgsUserAddDialog):
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
            "gas": self.basic_data_row.controls[2],
            "comment": self.comment_text_field,
            "discreteness": self.basic_data_row.controls[1],
            "slave_id": self.ids_row.controls[0],
            "owen_id": self.ids_row.controls[1],
            "owen_channel": self.ids_row.controls[2],
            "show_rs485": self.visibility_row.controls[0],
            "show_modified_amperage": self.visibility_row.controls[2],
            "show_amperage": self.visibility_row.controls[1],
            "amperage_low": self.amperage_settings_row.controls[0],
            "amperage_high": self.amperage_settings_row.controls[1],
            "amperage_threshold1": self.amperage_settings_row.controls[2],
            "amperage_threshold2": self.amperage_settings_row.controls[3],
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()


class Dgs210UserEditDialog(DgsUserEditDialog):
    def __init__(self, data):
        super().__init__(data)


class Dgs230UserEditDialog(DgsUserEditDialog):
    def __init__(self, data):
        super().__init__(data)


class AdvantUserEditDialog(AdvantUserAddDialog):
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
            "slave_id":self.rs485_settings_row.controls[0],
            "comment": self.comment_text_field,
            "show_rs485": self.rs485_settings_row.controls[1],
            "show_modified_amperage": self.amperage_visibility_row.controls[1],
            "show_amperage": self.amperage_visibility_row.controls[0],
            "unit_ch1": self.first_channel_basic_data_row.controls[0],
            "gas_ch1": self.first_channel_gas_text_field,
            "discreteness_ch1":self.first_channel_basic_data_row.controls[1],
            "unit_ch2": self.second_channel_basic_data_row.controls[0],
            "gas_ch2": self.second_channel_gas_text_field,
            "discreteness_ch2":self.second_channel_basic_data_row.controls[1],
            "owen_id_ch1":self.first_channel_owen_row.controls[0],
            "owen_number_ch1":self.first_channel_owen_row.controls[1],
            "owen_id_ch2":self.second_channel_owen_row.controls[0],
            "owen_number_ch2":self.second_channel_owen_row.controls[1],
            "amperage_low_ch1":self.first_channel_amperage_settings_row.controls[0],
            "amperage_high_ch1":self.first_channel_amperage_settings_row.controls[1],
            "amperage_threshold1_ch1":self.first_channel_thresholds_row.controls[0],
            "amperage_threshold2_ch1":self.first_channel_thresholds_row.controls[1],
            "amperage_low_ch2":self.second_channel_amperage_settings_row.controls[0],
            "amperage_high_ch2":self.second_channel_amperage_settings_row.controls[1],
            "amperage_threshold1_ch2":self.second_channel_thresholds_row.controls[0],
            "amperage_threshold2_ch2":self.second_channel_thresholds_row.controls[1]
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()


class XsUserEditDialog(XsUserAddDialog):
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
            "comment": self.comment_text_field,
            "slave_id": self.rs_text_field,
            "show_modified_amperage": self.visibility_row.controls[1],
            "show_amperage": self.visibility_row.controls[0],
            "amperage_low": self.amperage_settings_row.controls[0],
            "amperage_high": self.amperage_settings_row.controls[1],
            "amperage_threshold1": self.threshold_settings_row.controls[0],
            "amperage_threshold2": self.threshold_settings_row.controls[1]
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()


class DctUserEditDialog(DctUserAddDialog):
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
            "comment": self.comment_text_field,
            "channel": self.channel_text_field,
            "show_modified_amperage": self.visibility_row.controls[1],
            "show_amperage": self.visibility_row.controls[0],
        }
        for param, link in links.items():
            setattr(link, 'value', self.model.__dict__[param])
        self.update()