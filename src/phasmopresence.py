import pypresence as pyp
import time
import re
import os
import logging

from .phasmoreader import PhasmoReader

class PhasmoPresence:

    author = 'Manuel Cabral'
    version = '0.2'
    __slots__ = ['__client_id', '__reader', '__rpc']

    def __init__(self, client_id: str = None):
        self.__client_id = client_id
        self.__reader = PhasmoReader()
        self.__rpc = pyp.Presence(self.__client_id)

    def connect(self) -> None:
        logging.info('Connecting to Discord...')
        try:
            self.__rpc.connect()
            logging.info('Connected to Discord')
        except Exception as exc:
            logging.error(f'Failed to connect to Discord {exc}')
            raise Exception('Failed to connect to Discord') from exc
    
    def disconnect(self) -> None:
        self.__rpc.close()

    def format_data(self, state: str, data: dict) -> dict:
        if state == 'In-game':
            if data['Loaded Level'] == 'Main Menu':
                return { 'state': 'In main menu', 'large_image': 'logo'}
            mapname = re.sub(r"(\w)([A-Z])", r"\1 \2", data['Loaded Level'])
            details = int(data['Players']) > 1 and f'Playing with {data["Players"]} players' or 'Playing Solo'
            return {
                'state': details,
                'details': mapname,
                'large_image': data['Loaded Level'].lower(),
                'large_text': mapname,
                'small_image': 'logo',
                'small_text': data['Difficulty']
            }
        return { 'state': state, 'large_image': 'logo'}

    def update(self) -> None:
        self.__reader.load()
        fetched = self.__reader.fetch()
        formated_data = self.format_data(fetched['state'], fetched['data'])
        return formated_data

    def update_presence(self, data) -> None:
        self.__rpc.update(**data)
    
    def run(self) -> None:
        self.connect()
        os.system(f'title PhasmoPresence v{self.version}')
        try:
            logging.info('PhasmoPresence started, waiting for game to start.')
            logging.info('Press Ctrl+C to stop.')
            while True:
                data = self.update()
                self.update_presence(data)
                time.sleep(15)
        except KeyboardInterrupt:
            self.stop()
        except Exception as exc:
            logging.error(exc)
            self.stop()
        
    def stop(self) -> None:
        logging.info('PhasmoPresence stopped')
        self.disconnect()