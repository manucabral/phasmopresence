# PhasmoPresence
A simple Phasmophobia Rich Presence client made with :heart:

IMPORTANT! This app does not use MelonLoader or PhasBypass

## Features
- Shows if you're playing singleplayer or multiplayer
- Shows how long you've been playing
- Shows current playing map
- Respects Discords 15 seconds status update limit

## Usage
1. Download the last version from [here](https://github.com/manucabral/phasmopresence/releases)
2. Extract the zip file and open `PhasmoPresence.exe`
3. Play Phasmophobia

> If you want to open phasmopresence and phasmophobia at the same time execute runpp.bat

## Setup for developers
1. Go to Discord Developer Portal and create an application
3. Now go to Settings > OAuth2 and copy the clientid
4. Finally go to Settings > Rich Presence and add each map image with the following pattern: `bleasdalefarmhouse`
> All maps need to be added
5. Clone the repository
```bash
git clone https://github.com/manucabral/phasmopresence.git
cd phasmopresence
```
6. Install the requirements
```bash
pip install -r requirements.txt
```
7. Go to **src/core.py** and put your clientid.
```py
PhasmoPresence('YOUR CLIENT ID', log=True)
```
8. Run src/core.py
```bash
py src/core.py
```

## How does it work?
It's simple, PhasmoPresence periodically gets and checks information from the player log.

The player log is located in the next path `C:\Users\%YOUR_USER%\AppData\LocalLow\Kinetic Games\Phasmophobia\Player.log`

## FAQ
- **My Rich Presence Client is not displaying?**
  - Try
     - Go to your User Settings > Activity Status > Display current activity as a status message and make sure it's enabled.
     - Restart the app when Phasmophobia is running.

- **Do I need Discord open on my pc to use this app?**
  - Yes, you need to open Discord to run the app.

## Contributing
All contributions, bug reports, bug fixes, enhancements, and ideas are welcome. Just make a pull request or a issue!

## Preview
<p align="center"> 
<img src="https://github.com/manucabral/phasmopresence/blob/main/assets/loading.png?raw=true" width="250" title="loading">
<img src="https://github.com/manucabral/phasmopresence/blob/main/assets/playing.png?raw=true" width="250" title="playing">
<img src="https://github.com/manucabral/phasmopresence/blob/main/assets/menu.png?raw=true" width="250" title="menu">
</p>

## Credits
- [pypresence](https://github.com/qwertyquerty/pypresence)
- [phasmophobia](https://store.steampowered.com/app/739630/Phasmophobia/)
