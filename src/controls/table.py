import flet as ft
from sqlalchemy import select, update, insert, delete
from src.database.user_models import StandsService

MONTHS = [
    'Январь', "Февраль", 'Март', "Апрель", "Май", "Июнь",
    'Июль', 'Август', "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]
class Table(ft.DataTable):
    def __init__(self, data: list[list[ft.Control]], disabled: bool=True) -> None:
        self.columns = [
            ft.DataColumn(ft.Text(
                'Стенд',
                style=ft.TextStyle(weight=ft.FontWeight.W_600,  size=19),
                width=170,
                text_align=ft.TextAlign.CENTER,
            )),
            *[ft.DataColumn(
                ft.Text(
                    month,
                    width=170,
                    text_align=ft.TextAlign.CENTER
                )) for month in MONTHS]
        ]
        self.rows = [ft.DataRow(cells=[ft.DataCell(stand) for stand in x]) for x in data]
        super().__init__(self.columns, self.rows)
        self.disabled = disabled
        self.border = ft.border.all(3, '#A9A9A9')
        self.border_radius = 15
        self.vertical_lines = ft.BorderSide(1, '#A9A9A9')
        self.horizontal_lines = ft.BorderSide(1, '#A9A9A9')
        self.data_row_max_height = float('inf')
        self.column_spacing = 20
        self.heading_row_alignment = ft.MainAxisAlignment.CENTER
        self.heading_text_style = ft.TextStyle(weight=ft.FontWeight.W_600,  size=19)
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE


    async def get_data(self) -> list[list[str | int]]:
        return [[w.content.value for w in z] for z in [y for y in [x.cells for x in self.rows]]]



class Data:
    MODEL = StandsService

    def __init__(self, page) -> None:
        self.page = page

    async def get_data(self, year=int) -> list[list[str | int]]:
        async with self.page.db() as session:
            result = await session.execute(
                select(self.MODEL).
                where(self.MODEL.year == year)
            )
            return result.scalars().all()

    async def get_formatted_data(self, year=int) -> list[list[ft.TextField | ft.Text]]:
        return await self.format_data(await self.get_data(year))

    async def get_unformatted_data(self, year=int) -> list[list[ft.TextField | ft.Text]]:
        data = await self.get_data(year)
        reply = []
        for stand in ['Ресурсные испытания', "Длинная линия", 'Ресурсные испытания DCT']:
            row = [stand]
            s = {x.month: x.action for x in data if x.stand == stand}
            for month in MONTHS:
                if month in s.keys():
                    sign = s[month]
                else:
                    sign = ''
                row.append(sign)
            reply.append(row)
        return reply

    @staticmethod
    async def format_data(data) -> list[list[ft.TextField | ft.Text]]:
        reply = []
        for stand in ['Ресурсные испытания', "Длинная линия", 'Ресурсные испытания DCT']:
            row = [ft.Text(
                stand,
                style=ft.TextStyle(weight=ft.FontWeight.W_600,  size=19),
                width=170,
                text_align=ft.TextAlign.CENTER
            )]
            s = {x.month: x.action for x in data if x.stand == stand}
            for month in MONTHS:
                if month in s.keys():
                    sign = s[month]
                else:
                    sign = ''
                row.append(ft.TextField(
                    value=sign,
                    border='none',
                    text_align=ft.TextAlign.CENTER,
                    multiline=True,
                    width=170,
                    height=70,
                    content_padding=7
                ))
            reply.append(row)# ft.TextField(stand)
        return reply

    async def edit_data(self, stand, month, action, year=int) -> None:
        async with self.page.db() as session:  # Заносит в БД
            await session.execute(
                update(self.MODEL).
                where(
                    self.MODEL.stand == stand,
                    self.MODEL.month == month,
                    self.MODEL.year==year
                ).
                values(action=action)
            )
            await session.commit()

    async def insert_data(self, stand, year, month, action) -> None:
        async with self.page.db() as session:
            await session.execute(
                insert(self.MODEL).
                values(stand=stand, year=year, month=month, action=action)
            )
            await session.commit()


class TableDialog(ft.AlertDialog):
    def __init__(self) -> None:
        super().__init__()
        self.title = ft.Text(
            'График техобслуживания',
             weight=ft.FontWeight.W_800,
            size=20,
            text_align=ft.TextAlign.CENTER
        )
        self.modal = True
        self.content = ft.Column(
            height=80,
            width=200,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                ft.TextField(
                    border_color="#A9A9A9",
                    width=200,
                    height=80,
                    text_size=42,
                    text_vertical_align=0.0,
                    text_align=ft.TextAlign.CENTER,
                    text_style=ft.TextStyle(weight=ft.FontWeight.W_900, letter_spacing=8, size=42),
                    value='',
                    max_length=6,
                    input_filter=ft.NumbersOnlyInputFilter(),
                    autofocus=True,
                    border_width=3.5,
                    border_radius=21,
                    label='Год',
                    label_style=ft.TextStyle(weight=ft.FontWeight.W_900, color='#000000'),
                    on_submit=self.show_data,
                    expand=True
                )
            ]
        )

    def did_mount(self):
        self.data = Data(self.page)
        self.access = self.page.floating_action_button.visible
        self.actions = [ft.FilledButton(
            "Закрыть",
            on_click=lambda e: self.page.close(self),
            color='#FFFFFF',
            bgcolor='#000000'
        )]
        self.update()

    async def show_data(self, e) -> None:
        self.table = Table(await self.data.get_formatted_data(year=int(e.data)), disabled=not self.access)
        self.content = ft.Column(
            controls=[
                ft.TextField(
                    width=135,
                    value=e.data,
                    border_color="#A9A9A9",
                    text_size=19,
                    text_vertical_align=0.0,
                    height=50,
                    text_align=ft.TextAlign.CENTER,
                    text_style=ft.TextStyle(weight=ft.FontWeight.W_600, size=19),
                    border_width=2,
                    border_radius=28,
                    label="Год",
                    input_filter=ft.NumbersOnlyInputFilter(),
                    on_submit=self.show_data
                ),
                ft.Row(scroll=ft.ScrollMode.ADAPTIVE, controls=[self.table], spacing=10)
        ])
        self.actions = {
            True: [
                ft.FilledButton(
                    "Сохранить",
                    on_click=self.save,
                    color='#FFFFFF',
                    bgcolor='#000000'
                ),
                ft.FilledButton(
                    "Отмена",
                    on_click=lambda e: self.page.close(self),
                    color='#FFFFFF',
                    bgcolor='#6C757D'
                )
            ],
            False: [ft.FilledButton(
                    "Закрыть",
                    on_click=lambda e: self.page.close(self),
                    color='#FFFFFF',
                    bgcolor='#000000'
                )]
        }[self.access]
        self.update()

    async def save(self, e):
        data = await self.table.get_data()
        before = await self.data.get_unformatted_data(int(self.content.controls[0].value))
        year = int(self.content.controls[0].value)
        for bef, aft in zip(before, data):
            stand = bef[0]
            ind = 0
            for vb, va in zip(bef[1:], aft[1:]):
                month = MONTHS[ind]
                if vb != va:
                    if vb == '':
                        await self.data.insert_data(stand=stand, year=year, month=month, action=va)
                    else:
                        await self.data.edit_data(stand=stand, year=year, month=month, action=va)
                ind += 1
        self.page.close(self)


class TableButton(ft.IconButton):
    def __init__(self) -> None:
        super().__init__()
        self.icon = ft.icons.MISCELLANEOUS_SERVICES
        self.on_click = lambda e: self.page.open(TableDialog())
        self.icon_size: int = 30
        self.icon_color: str = '#A9A9A9'
        self.tooltip: str = "Техобслуживание"
        self.splash_radius: int = 0