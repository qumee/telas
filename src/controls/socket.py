import asyncio
import websockets
import flet as ft
from pymodbus.client import AsyncModbusTcpClient
from json import loads, dumps


class Socket(ft.Container):
    def __init__(self):
        super().__init__()
        self.__ws_data: dict = {}
        self.__sgm_data: dict = {}
        self.long_line_status: bool = False
        self.first_production_status: bool = False
        self.dct_status: bool = False
        self.disabled: bool = True
        self.visible: bool = False

    def did_mount(self):
        self.running = True
        self.ws = self.page.config.connections.websocket
        self.sgm = self.page.config.connections.sgm
        self.page.run_task(self.run_ws)
        self.page.run_task(self.run_sgm)

    def will_unmount(self):
        self.running = False

    async def stop(self):
        self.running = False
        await self.websocket.close()
        self.websocket = await websockets.connect(f'ws://{self.ws.host}:{self.ws.port}')
        await self.websocket.send(dumps({'action': 'stop'}))
        print(await self.websocket.recv())

    async def start(self):
        self.running = True
        self.page.run_task(self.run_ws)
        self.page.run_task(self.run_sgm)

    async def set(
            self,
            devices: list[int],
            address: int,
            value: int
    ) -> dict:
        await self.websocket.send(dumps({
            'action': 'set',
            'devices': devices,
            'address': address,
            'value': value
        }))
        return loads(await self.websocket.recv())

    async def run_ws(self):
        self.websocket = await websockets.connect(f'ws://{self.ws.host}:{self.ws.port}')
        await self.websocket.send(dumps({'action': 'start'}))
        await self.websocket.recv()
        while self.running:
            await self.websocket.send(dumps({'action': 'get'}))
            data = await self.websocket.recv()
            statuses = loads(data)['statuses']
            self.long_line_status: bool = statuses['long_line']
            self.first_production_status: bool = statuses['first_production']
            self.dct_status: bool = statuses['dct']
            await self.__set_ws_data(data)

            await asyncio.sleep(self.ws.timeout)
        self.ws_status = False

    async def run_sgm(self):
        self.client = AsyncModbusTcpClient(host=self.sgm.host, port=self.sgm.port)
        await self.client.connect()

    async def __set_ws_data(self, data: str) -> None:
        self.__ws_data = loads(data)

    async def get_ws_data(self) -> dict:
        return self.__ws_data
