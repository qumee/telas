import flet as ft
from nest_asyncio import apply
from src.database import Model
from src.config import Config
from src.controls import (
    MenuBar,
    UserArea,
    AddButton,
    Socket
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


async def design_page(page: ft.Page) -> ft.Page:
    """
    Оформление страницы и окна
    """
    page.title = "Ресурсные испытания"  # Ставит имя программы
    page.theme_mode = ft.ThemeMode.LIGHT  # Включение тёмной темы
    page.bgcolor = "#F5F5F5"

    page.window.frameless = False  # Оставляет рамку приложения
    page.window.min_width = 1005  # Минимальная ширина окна, в пикслях
    page.window.min_height = 650  # Максимальная ширина окна, в пикслях

    async def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'F9':  # Хоткей для того, чтобы убрать рамки
            page.window.title_bar_hidden = not page.window.title_bar_hidden  # Убирает бар сверху
            page.window.title_bar_buttons_hidden = not page.window.title_bar_buttons_hidden  # Убирает кнопки
            page.update()

    page.on_keyboard_event = on_keyboard  # Хандлер на хоткеи

    page.floating_action_button = AddButton()  # Кнопка добавления устройств, по умолчанию отключена

    return page


async def add_attributes(page: ft.Page) -> ft.Page:
    """
    С помощью setattr() инжектит в класс страницы 
    атрибуты конфига и engine для связи с Postgres
    и для удобства ссылки на MenuBar и Area
    """
    config = Config(r'src\config\config.json')  # Иницилизация класса конфига и передача пути
    engine = create_async_engine(config.postgres.url) # Через @property передаёт url к Postgres
    session = sessionmaker( # Создаёт асинхронную сессию для работы с Postgres
        engine, # engine
        expire_on_commit=False,  # Сохраняет её работу до отключения программы
        class_=AsyncSession  # Делает асинхронной
    )

    attrs = {
        'config': config,
        'engine': engine,
        'db': session,
        'menubar': MenuBar(),
        'area': UserArea(),
    }

    for attr, value in attrs.items():  # Инжектит циклом все значения в page
        setattr(page, attr, value)

    socket = Socket()
    page.add(socket)
    setattr(page, 'socket', socket)

    async with page.engine.begin() as con:
       await con.run_sync(Model.metadata.create_all)  # Создаёт таблицы, если их нет; Модели таблиц в директории database

    return page


async def main(page: ft.Page) -> None:
    page = await design_page(page)  # Оформляет страницу
    page = await add_attributes(page)  # Инжектит новые атрибуты в page

    page.add(  # Объект страницы
        ft.Column(
            [
                ft.WindowDragArea(page.menubar), # Позволяет управлять движением окна MenuBar-ом
                page.area
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )


if __name__ == '__main__':
    apply()  # Запускает nest-asyncio для избежания RuntimeError
    ft.app(target=main, assets_dir='assets')  # Запуск Flet
