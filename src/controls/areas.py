from asyncio import sleep
from src.devices import *
from src.database import *
from src.dialogs import *
from sqlalchemy import select, update, insert, delete
from random import uniform


class Element:
    """
    Пространство имён, соотнесённое с одним устройством
    Хранит набор переменных для удобного обращения к оным
    """
    def __init__(
            self,
            title: str,
            type_: type,
            model: Model,
            add_dialog: AddDialog,
            edit_dialog: Dialog
    ) -> None:
        self.title: str = title
        self.type: type = type_
        self.model: Model = model
        self.add_dialog: AddDialog = add_dialog
        self.edit_dialog: Dialog = edit_dialog


class Information:
    """
    Пространство имён, хранящее отношение всех связанных с устройствами параметров
    При вызове себя определяет по типу аргумента, что за параметр передан и ищет
    соответствие его с устройством
    """
    def __init__(
            self,
            area,
            titles: list[str],
            types: list[type],
            models: list[Model],
            add_dialogs: list[Dialog],
            edit_dialogs: list[Dialog]
    ):
        self.area = area  # Ссылка на Area, которой принадлежит пространство имён
        self.titles: list[str] = titles  # Все названия устройств, берутся из конфига
        self.types: list[type] = types  #  Все классы устройств
        self.models: list[Model] = models  # Модели из SQlAlchemy, меняются в зависимости от Area
        self.add_dialogs: list[Dialog] = add_dialogs  # AlertDialog для добавления устройства, меняются в зависимости от Area
        self.edit_dialogs: list[Dialog] = edit_dialogs # AlertDialog для изменения устройства, меняются в зависимости от Area
        self.elements: list[Element] = [
            Element(tl, tp, ml, ad, ed) for tl, tp, ml, ad, ed in zip(
                titles,
                types,
                models,
                add_dialogs,
                edit_dialogs
            )
        ]

    def __call__(self, param: object) -> str | type | Model | Dialog:
        """
        Принимает любой из доступных типов и проходится по элемента в поисках соответсвия
        Возвращает по совпадению объект элемента, через который можно получить
        все ассоциированные с устройством переменные
        """
        params: dict[str:type] = {  # Словарь соответствия атрибута элемента к его классу
            'title': str,
            'type': type,
            'model': Model,
            'add_dialog': AddDialog,
            'edit_dialog': Dialog
        }
        key = [key for key, value in params.items() if isinstance(param, value)]  # Ищет совпадение по классу
        if key[0] == 'type':
            if issubclass(param, Model):
                key[0] = 'model'
        for element in self.elements:
            if element.__dict__[key[0]] in [param, type(param)]:  # Ищет совпадение переменной элемента с параметром
                return element


class InAreaDevice:
    def __init__(
            self,
            factory_number: str,
            link: object,
            model: Model
    ) -> None:
        self.factory_number = factory_number
        self.link = link
        self.model = model


class Area(ft.Column):
    """
    Область со стендами и устройствами на них
    """
    DEVICES: list[type] = [  # Все классы имеющихся устройств
        Dgs210, Dgs230,
        Advant, Xs, Dct
    ]
    MODELS: list[Model]  # Модели из SQLAlchemy, меняются в зависимости от вида Area
    ADD_DIALOGS: list[AddDialog]  # Диалоги добавления устройства, меняются в зависимости от вида Area
    EDIT_DIALOGS: list[Dialog]  # Диалоги изменения устройства, меняются в зависимости от вида Area

    def __init__(self) -> None:
        super().__init__()  # Наследование
        self.scroll = ft.ScrollMode.AUTO  # Включает скроллинг
        self.expand = True   # Растягивание на всю длину
        self.alignment = ft.MainAxisAlignment.START    # Выравнивание по центру по вертикали
        self.horizontal_alignment = ft.CrossAxisAlignment.START # Выравнивание по центру по горизонтали

        # Ниже три стенда представленные рядами, в которые добавляются устройства
        self.resources_stand = ft.Row(wrap=True, expand=True)
        self.long_stand = ft.Row(wrap=True, expand=True)
        self.dct_stand = ft.Row(wrap=True, expand=True)
        self.controls = [  # Стенды, добавленные в Area
            self.resources_stand,
            self.long_stand,
            self.dct_stand
        ]

    def did_mount(self):
        """
        Наследуемая функция от Flet для запуска потока
        """
        self.info: Information = Information(  # Создание класса с информацией об устройствах
            self,
            self.page.config.devices.titles[:-1],
            self.DEVICES,
            self.MODELS,
            self.ADD_DIALOGS,
            self.EDIT_DIALOGS
        )
        self.devices: dict[str:Model] = {}  # Все данные устройств на страничке
        self.running = True
        self.page.run_task(self.run)

    def will_unmount(self):
        """
        Наследуемая функция от Flet для заверешения потока
        """
        self.running = False

    async def collect_all_devices(self) -> list[Model]:
        """
        Собирает все существующие в базе данных девайсы
        Возвращает массив моделей
        """
        devices: list[Model] = []
        for model in self.info.models:
            async with self.page.db() as session:
                result = await session.execute(select(model))
                devices += result.scalars().all()
        return devices

    async def collect_device(self, factory_number: str, device: str | type | Model | Dialog) -> Model:
        async with self.page.db() as session:
            device = self.info(device).model # Получение модели SQL по любой переменной устройства
            result = await session.execute(select(device).where(device.factory_number == factory_number))
            return result.scalar() # Извлечение и возврат объекта

    async def init_devices(self) -> None:
            devices = await self.collect_all_devices()  # Получает все устройства из БД
            for device in devices:
                await self.add(
                    device.stand,
                    device.factory_number,
                    device
                )

    async def add(
            self,
            stand: str,
            factory_number: str,
            device: Model
    ) -> None:
        model = device
        stands = self.page.config.stands.to_row  # Получаем все стенды
        device: Device = self.info(device).type(factory_number) # Преобразуем название в класс
        self.__dict__[stands[stand]].controls.append(device)  # Добавляем на стенд

        self.devices[factory_number] = InAreaDevice(
            factory_number,
            device,
            model
        ) # Добавляет в словарь данные об устройстве

        self.update() # Обновляем, дабы устройство добавилось на страницу
        if isinstance(device, SingleChannelDevice):  # Проверка на количество каналов
            await device.change_visibility(
                model.show_amperage,
                model.show_modified_amperage,
                model.show_rs485
            )
            await device.set_gas(model.gas)
            await device.set_unit(model.unit)
        elif isinstance(device, DoubleChannelDevice):
            await device.first_channel.change_visibility(
                model.show_amperage,
                model.show_modified_amperage,
                model.show_rs485
            )
            await device.first_channel.set_gas(model.gas_ch1)
            await device.first_channel.set_unit(model.unit_ch1)

            await device.second_channel.change_visibility(
                model.show_amperage,
                model.show_modified_amperage,
                model.show_rs485
            )
            await device.second_channel.set_gas(model.gas_ch2)
            await device.second_channel.set_unit(model.unit_ch2)
        self.update()

    async def add_from_dialog(
            self,
            device: str,
            **kwargs
    ) -> None:
        """
        Добавляет устройство в область после получения информации из диалога
        """
        model: Model = self.info(device).model # Получает SQL модель
        async with self.page.db() as session:  # Заносит в БД
            await session.execute(
                insert(model).
                values(**kwargs)
            )
            await session.commit()
        data = await self.collect_device(kwargs['factory_number'], device)  # Собирает свежедобавленные данные
        await self.add(
            kwargs['stand'],
            kwargs['factory_number'],
            data
        )  # Добавляет в область

    async def delete(
            self,
            factory_number: str,
            model: Model
    ) -> None:
        async with self.page.db() as session:  # Заносит в БД
            await session.execute(
                delete(model).
                where(model.factory_number == factory_number)
            )
            await session.commit()
        for i in self.controls:
            for j in i.controls:
                if j.factory_number == factory_number:
                    i.controls.remove(j)
                    self.update()
                    break

    async def edit(
            self,
            model,
            **kwargs
    ) -> None:
        factory_number = kwargs['factory_number']
        async with self.page.db() as session:  # Заносит в БД
            await session.execute(
                update(model).
                where(model.factory_number == factory_number).
                values(**kwargs)
            )
            await session.commit()
        data = await self.collect_device(factory_number, model)
        for i in self.controls:
            for j in i.controls:
                if j.factory_number == factory_number:
                    i.controls.remove(j)
                    break
        await self.add(data.stand, data.factory_number, data)
        self.update()


class UserArea(Area):
    MODELS: list[Model] = [
        Dgs210User,
        Dgs230User,
        AdvantUser,
        XsUser,
        DctUser
    ]
    ADD_DIALOGS: list[AddDialog] = [
        Dgs210UserAddDialog,
        Dgs230UserAddDialog,
        AdvantUserAddDialog,
        XsUserAddDialog,
        DctUserAddDialog
    ]

    EDIT_DIALOGS: list[Dialog] = [
        Dgs210UserEditDialog,
        Dgs230UserEditDialog,
        AdvantUserEditDialog,
        XsUserEditDialog,
        DctUserEditDialog
    ]
    def __init__(self):
        super().__init__()

    async def __ws_dgs(
            self,
            device: InAreaDevice,
            ws
    ) -> None:
        md = device.model
        amperage = ws['owens'][str(md.owen_id)][str(md.owen_channel)]
        rs = ws['rs']['dgs'][str(md.slave_id)]
        modified_amperage = (md.amperage_high-md.amperage_low)/16*(amperage-4)
        await device.link.set_amperage(amperage)
        await device.link.set_modified_amperage(modified_amperage)

        if rs != -1 and md.show_rs485:
            await device.link.set_rs(rs/md.discreteness)

        if md.show_amperage or md.show_modified_amperage:
            if amperage < 2:
                status = 'ОБРЫВ'
            elif 2.5 < amperage < 3.9:
                status = "ИНИЦИАЛИЗАЦИЯ"
            elif amperage > 19.7:
                status = "АВАРИЯ"
            else:
                if md.gas.upper() == 'O2':
                    if modified_amperage < md.amperage_threshold1:
                        status = 'ПОРОГ 1'
                    elif modified_amperage > md.amperage_threshold2:
                        status = 'ПОРОГ 2'
                    else:
                        status = 'НОРМА'
                else:
                    if modified_amperage > md.amperage_threshold1 and modified_amperage < md.amperage_threshold2:
                        status = 'ПОРОГ 1'
                    elif modified_amperage > md.amperage_threshold1 and modified_amperage > md.amperage_threshold2:
                        status = 'ПОРОГ 2'
                    else:
                        status = 'НОРМА'
        await device.link.set_status(status)

    async def __chitic_dgs(self, device, ws) -> None:
        md = device.model
        dt = ws['chitic']['dgs'][str(md.slave_id)]
        if dt['status'] == -1 or dt['concentration'] == -1:
            return None
        concentration = dt['concentration']
        status = bin(dt['status'])[2:].zfill(16)[::-1]
        await device.link.set_rs(concentration/md.discreteness)
        if status.count('0') == 16:
            st = 'НОРМА'
        elif status[1] == '1' and status[2] == '0':
            st = 'ПОРОГ 1'
        elif status[1] == '1' and status[2] == '1':
            st = 'ПОРОГ 2'
        elif status[5] == '1':
            st = 'ПРЕВЫШЕНИЕ СИГНАЛА'
        elif status[14] == '1' or status[13] == '1':
            st = 'ОБРЫВ'
        else:
            st = 'АВАРИЯ'
        await device.link.set_status(st)


    async def __dgs(self, device: InAreaDevice) -> None:
        ws = await self.page.socket.get_ws_data()
        if device.model.stand == 'Ресурсные испытания':
            await self.__ws_dgs(device, ws)
        else:
            await self.__chitic_dgs(device, ws)

    async def __advant_channel(
            self,
            gas: str,
            amperage: float,
            high: float,
            low: float,
            th1: float,
            th2: float,
            show_amperage: bool,
            show_modified_amperage: bool,
    ) -> tuple:
        modified_amperage = (high-low)/16*(amperage-4)
        if show_amperage or show_modified_amperage:
            if amperage < 2:
                status = 'ОБРЫВ'
            elif 2.5 < amperage < 3.9:
                status = "ИНИЦИАЛИЗАЦИЯ"
            elif amperage > 19.7:
                status = "АВАРИЯ"
            else:
                if gas.upper() == 'O2':
                    if modified_amperage < th1:
                        status = 'ПОРОГ 1'
                    elif modified_amperage > th2:
                        status = 'ПОРОГ 2'
                    else:
                        status = 'НОРМА'
                else:
                    if modified_amperage > th1 and modified_amperage < th2:
                        status = 'ПОРОГ 1'
                    elif modified_amperage > th1 and modified_amperage > th2:
                        status = 'ПОРОГ 2'
                    else:
                        status = 'НОРМА'

        return amperage, modified_amperage, status

    async def __advant(self, device):
        md = device.model
        ws = await self.page.socket.get_ws_data()
        amperage = ws['owens']
        rs_conc = ws['rs']['advant'][str(md.slave_id)]
        first_channel = await self.__advant_channel(
            md.gas_ch1,
            amperage[str(md.owen_id_ch1)][str(md.owen_number_ch1)],
            md.amperage_high_ch1,
            md.amperage_low_ch1,
            md.amperage_threshold1_ch1,
            md.amperage_threshold2_ch1,
            md.show_amperage,
            md.show_modified_amperage,
        )
        second_channel = await self.__advant_channel(
            md.gas_ch2,
            amperage[str(md.owen_id_ch2)][str(md.owen_number_ch2)],
            md.amperage_high_ch2,
            md.amperage_low_ch2,
            md.amperage_threshold1_ch2,
            md.amperage_threshold2_ch2,
            md.show_amperage,
            md.show_modified_amperage,
        )

        await device.link.first_channel.set_amperage(first_channel[0])
        await device.link.first_channel.set_modified_amperage(first_channel[1])
        await device.link.first_channel.set_status(first_channel[2])
        await device.link.first_channel.set_rs(rs_conc['first_channel_concentration']/md.discreteness_ch1)

        await device.link.second_channel.set_amperage(second_channel[0])
        await device.link.second_channel.set_modified_amperage(second_channel[1])
        await device.link.second_channel.set_status(second_channel[2])
        await device.link.second_channel.set_rs(rs_conc['second_channel_concentration']/md.discreteness_ch2)

        self.update()

    async def __xs(self, device: InAreaDevice):
        md = device.model
        ws = await self.page.socket.get_ws_data()
        data = ws['rs']['xs'][str(md.slave_id)]
        await device.link.set_amperage(data['amperage'])
        await device.link.set_modified_amperage(data['modified_amperage'])
        st = bin(data['status'])[2:].zfill(16)[::-1]
        if st.count('0') == len(st):
            status = 'НОРМА'
        elif st[9] == '1':
            status = 'АВАРИЯ'
        elif st[5] == '1':
            status = 'ПРЕВЫШЕНИЕ СИГНАЛА'
        elif st[1] == '1' and st[2] != '1':
            status = 'ПОРОГ 1'
        elif st[1] == '1' and st[2] == '1':
            status = 'ПОРОГ 2'
        else:
            status = 'ОБРЫВ'
        await device.link.set_status(status)


    async def __dct(self, device: InAreaDevice):
        sgm = await self.page.socket.get_sgm_data(device.model.channel)
        await device.link.set_amperage(sgm['amperage'])
        await device.link.set_modified_amperage(sgm['modified_amperage'])
        await device.link.set_status(sgm['status'])

    async def run(self) -> None:
        methods = dict(zip(self.MODELS, [
            self.__dgs,
            self.__dgs,
            self.__advant,
            self.__xs,
            self.__dct
        ]))
        await self.init_devices()
        while self.running:
            try:
                for device in self.devices.values():
                        await methods[type(device.model)](device)
            except Exception as ex:
                pass
                #print(f'UserArea, run() | {ex}')
            self.update()
            await sleep(0.01)


class CustomerArea(Area):
    MODELS: list[Model] = [
        Dgs210Customer,
        Dgs230Customer,
        AdvantCustomer,
        XsCustomer,
        DctCustomer
    ]
    ADD_DIALOGS: list[AddDialog] = [
        Dgs210CustomerAddDialog,
        Dgs230CustomerAddDialog,
        AdvantCustomerAddDialog,
        XsCustomerAddDialog,
        DctCustomerAddDialog
    ]

    EDIT_DIALOGS: list[Dialog] = [
        Dgs210CustomerEditDialog,
        Dgs230CustomerEditDialog,
        AdvantCustomerEditDialog,
        XsCustomerEditDialog,
        DctCustomerEditDialog
    ]
    def __init__(self):
        super().__init__()


    async def run(self) -> None:
        config = self.page.config.customer
        await self.init_devices()
        while self.running:
            for factory_number, device in self.devices.items():
                link = device.link
                model = device.model
                try:
                    if isinstance(link, SingleChannelDevice):
                        if model.gas.upper() in ['O2', 'О2']:
                            ox = config['oxygen']
                        else:
                            ox = config['others']
                        amperage = round(uniform(ox['amperage']['min'], ox['amperage']["max"]), 3)
                        modified_amperage = round(uniform(ox['modified_amperage']['min'], ox['modified_amperage']["max"]), 1)
                        concentration = round(uniform(ox['concentration']['min'], ox['concentration']["max"]), 1)
                        await link.set_status(model.status)
                        await link.set_amperage(amperage)
                        await link.set_rs(concentration)
                        await link.set_modified_amperage(modified_amperage)

                    elif isinstance(link, DoubleChannelDevice):
                        ox = config['others']
                        amperage = round(uniform(ox['amperage']['min'], ox['amperage']["max"]), 3)
                        modified_amperage = round(uniform(ox['modified_amperage']['min'], ox['modified_amperage']["max"]), 1)
                        concentration = round(uniform(ox['concentration']['min'], ox['concentration']["max"]), 1)
                        await link.first_channel.set_status(model.status_ch1)
                        await link.first_channel.set_amperage(amperage)
                        await link.first_channel.set_rs(concentration)
                        await link.first_channel.set_modified_amperage(modified_amperage)

                        await link.second_channel.set_status(model.status_ch2)
                        await link.second_channel.set_amperage(amperage)
                        await link.second_channel.set_rs(concentration)
                        await link.second_channel.set_modified_amperage(modified_amperage)
                except AttributeError as ex:
                    print(ex)
            self.update()
            await sleep(config['delay'])


