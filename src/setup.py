from cx_Freeze import setup, Executable

build_exe_options = {'packages': ['os'], 'excludes': ['tkinter']}

setup(
    name='PhasmoPresence',
    version='0.1',
    description='A simple Phasmophobia Discord Rich Presence',
    options={'build_exe': build_exe_options},
    executables=[Executable(
        'core.py', target_name='PhasmoPresence.exe', icon='logo.ico')]
)
