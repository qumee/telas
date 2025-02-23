import flet as ft
from .custom_contorols import *


class Dialog(ft.AlertDialog):
    def __init__(self, factory_number: str) -> None:
        super().__init__()
        self.actions = []
        self.modal = True
        self.factory_number = factory_number
        self.title: ft.Text = ft.Text( # Заголовок диалог - заводской номер устройства
            factory_number,
            weight=ft.FontWeight.W_800,
            size=20,
            text_align=ft.TextAlign.CENTER
        )

    @property
    def links(self) -> dict[str:object]:
        return {}

    async def save(self, e):
        await self.page.area.edit(
            type(self.model),
            **self.links
        )
        self.page.close(self)


class AddDialog(Dialog):
    def __init__(
            self,
            stand: str,
            factory_number: str,
            device: str
    ) -> None:
        super().__init__(factory_number)
        self.stand = stand
        self.device = device
        self.actions = [
            ft.FilledButton(
                'Добавить',
                on_click=self.add,
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

    async def add(self, e):
        print(self.links)
        await self.page.area.add_from_dialog(
            device=self.device,
            **self.links
        )
        self.page.close(self)
