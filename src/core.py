from pypresence import Presence, exceptions as pExceptions
from requests import get, exceptions as rExceptions
from time import sleep, time
from os import getenv, system

REPO_URL = 'https://api.github.com/repos/manucabral/phasmopresence/releases'
RELEASE_URL = 'https://github.com/manucabral/phasmopresence/releases/latest'
AUTHOR = '@manucabral'
VERSION = '0.1'


class PhasmoPresence:

    log_path = getenv('APPDATA').replace('Roaming', 'LocalLow') + \
        '\\Kinetic Games\\Phasmophobia\\Player.log'
    game_running = running = False
    target_words = ['XR stopped completely',
                    'Loaded Level', 'Callback aborted']
    rpc = start_time = None
    last_data = {}
    attemps = 0

    def __init__(self, client_id: str, log: bool = False):
        self.client_id = client_id
        self.log = log

    def check_update(self):
        res = get(REPO_URL)
        try:
            res.raise_for_status()
        except rexceptions.HTTPError as err:
            self.print(f'{err}', type="ERROR")
            return
        versions = []
        for key in res.json():
            versions.append(key['tag_name'])
        if versions[0] != VERSION:
            self.print(
                f'New version available: {versions[0]}', type="INFO")
            self.print(
                f'Download it here: {RELEASE_URL}', type="INFO")
        else:
            self.print('Up to date!', type="PHASMOPRESENCE")

    def get_game_status(self) -> bool:
        lines = self.read()
        stop_words = ['xr stopped', 'callback aborted']
        for line in lines:
            if any(word in line for word in stop_words):
                return False
        return True

    def read(self) -> list:
        try:
            with open(self.log_path, 'r') as f:
                lines = f.readlines()
                return [line.lower() for line in lines if any(word in line for word in self.target_words)]
        except Exception as e:
            self.print(e, type="ERROR")

    def print(self, message: str, **kwargs) -> None:
        type = kwargs.get("type", "INFO")
        if self.log:
            print(f'[{type}] {message}')

    def connect(self) -> None:
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.running = True
            self.print('Connected to Discord!', type="DISCORD")
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.print(e, type="ERROR")
            self.print('Reconnecting in 5 seconds ...')
            sleep(5)
            if self.attemps > 3:
                self.print('Reconnecting failed!', type="ERROR")
                self.stop()
                return
            else:
                self.attemps += 1
                self.run()

    def get_levels(self) -> dict:
        levels = [line.split('|')
                  for line in self.read() if 'loaded level' in line]
        data = []
        if not levels:
            return {}
        for level in levels:
            dic = {}
            for arguments in level:
                keyword, value = arguments.split(':')
                dic[keyword.strip()] = value.strip()
        data.append(dic)
        return data

    def presence_handler(self) -> dict:
        state = details = large_text = None
        large_image = small_text = None
        large_image = small_image = 'logo'
        levels = self.get_levels()
        if len(levels) == 0:
            state = 'Loading game ...'
        else:
            last_level = levels[-1]
            ishost = last_level.get('ishost') == 'true'
            players = int(last_level.get('players'))
            difficulty = last_level.get('difficulty')
            mapname = last_level.get('loaded level')
            if players == 0:
                state = 'In Main Menu'
            elif players >= 1:
                details = f'{"Host, " if ishost else ""}{"SinglePlayer" if players == 1 else "MultiPlayer"} ({players}/4)'
                state = f'Difficulty {difficulty.capitalize()}'
                large_image = f'{mapname.lower().replace(" ", "")}'
                large_text = f'{mapname.title()}'
        return {
            'state': state,
            'details': details,
            'start': self.start_time,
            'large_image': large_image,
            'large_text': large_text,
            'small_image': small_image,
            'small_text': small_text,
            'buttons': [
                {"label": "Download Extension", "url": RELEASE_URL}
            ]
        }

    def update(self) -> None:
        self.start_time = time()
        while self.running and self.game_running:
            try:
                self.print('Updating presence ...')
                data = self.presence_handler()
                self.rpc.update(**data)
                if data != self.last_data:
                    self.start_time = time()
                self.last_data = data
                sleep(15)
                self.game_running = self.get_game_status()
            except KeyboardInterrupt:
                self.stop()
                return
            except Exception as e:
                self.print(f'Error: {e}', type="ERROR")
        if not self.game_running:
            self.print('Game stopped!', type="PHASMOPHOBIA")
            self.wait_game_start()

    def wait_game_start(self) -> None:
        self.print('Waiting game start ...', type="PHASMOPHOBIA")
        try:
            while not self.game_running:
                self.game_running = self.get_game_status()
                sleep(2)
        except KeyboardInterrupt:
            self.stop()
            return
        self.print('Game started!', type="PHASMOPHOBIA")
        self.update()

    def stop(self) -> None:
        self.print('Stopping client ...')
        self.running = False
        if self.rpc != None:
            self.rpc.close()
        self.print('Client stopped successfully!')
        sleep(2)

    def run(self) -> None:
        system('cls')
        system('title PhasmoPresence ' + VERSION + ' ' + AUTHOR)
        self.check_update()
        self.print('Starting client ...')
        self.connect()
        if self.running:
            self.wait_game_start()


if __name__ == '__main__':
    p = PhasmoPresence('client id', log=True)
    p.run()
