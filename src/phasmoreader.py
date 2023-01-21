'''
Phasmophobia log reader for Python 3.8+
This script reads the Player.log file and returns a dictionary with the current game state and data.
'''

import os
from typing import Dict, List

class PhasmoReader:
    '''Core class.'''
    __slots__ = ['__log', '__log_path']

    def __init__(self, path: str = None):
        self.__log = ''
        self.__log_path = path if path else os.path.join(\
            os.environ['LOCALAPPDATA'] + 'Low', 'Kinetic Games', 'Phasmophobia', 'Player.log')

    def __filter(self, word: str) -> List[str]:
        return [line for line in self.__log.splitlines() if word in line]

    def __format(self, data: List[str]) -> Dict[str, str]:
        data_dict = {}
        for line in data.splitlines():
            key, value = line.split(':')
            key = key.strip()
            if key == 'Difficulty' and '(Difficulty)' in value:
                value = 'Normal'
            data_dict[key] = value.strip()
        return data_dict

    def __send_state(self, state: str, data: Dict[str, str] = None) -> Dict[str, str]:
        return {'state': state, 'data': data }

    def load(self) -> None:
        '''Loads the log file.'''
        try:
            with open(self.__log_path, 'r', errors='ignore', encoding='utf-8') as log_file:
                self.__log = log_file.read()
        except FileNotFoundError as exc:
            raise FileNotFoundError('Log file not found') from exc

    def running(self) -> bool:
        '''Returns True if the game is running.'''
        return 'Stop' not in self.__log

    def fetch(self) -> Dict[str, str]:
        '''Returns a dictionary with the current game state and data.'''
        if not self.__log:
            self.load()
        if not self.running():
            return self.__send_state('Game not running')
        level = self.__filter('Level:')
        if not level:
            return self.__send_state('Game starting')
        data = {}
        for line in level[-1].split('|'):
            data.update(self.__format(line))
        return self.__send_state('In-game', data)
