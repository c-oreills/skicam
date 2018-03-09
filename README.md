# skicam
Home made GoPro/MP3 Player using Raspberry Pi and Camera Module.

![Jegg and Bullard get some sick air](readme_imgs/boarding.s.gif?raw=true)

Jegg and Bullard get some sick air

![Duct tape camera to match the duct tape programming](readme_imgs/cammodule.jpg?raw=true)

Duct tape camera to match the duct tape programming

## Features
* Photo/Video recording
* MP3 player with full support for playlists, volume control, skipping and shuffle
* WiFi hotspot with web interface for camera configuration and photoreel view
* Audio interface with audio cues to navigate submenus
* Input based on toggle button in ski glove linked to GPIO

## Submenus
Each Submenu option is selected by clicking the toggle button a number of times, e.g. toggling 4 times will select option 4 on the current menu.

Each submenu has a distinct audio cue to ease navigation.

### Main Menu
1. Take Photo
2. Start Video Recording (click again to stop, 30 second audio cue to remind recording still underway)
3. -> Music Menu
4. Music: Toggle Play/Pause
5. -> Utils Menu
6. Start WiFi and Web Interface

### Music Menu
1. Next Track
2. Next Playlist
3. -> Main Menu
4. Prev Track
5. -> Music Misc Menu

### Music Misc Menu
1. Volume Down
2. Volume Up
3. -> Music Menu
4. Toggle Shuffle
5. Toggle Repeat

### Utils Menu
1. Say IP Address of Web Interface
2. Say Last Captured Photo/Video
3. -> Main Menu
4. System Reboot (with Prompt)
5. Delete Photos Marked Bad (with Prompt)

Any number of toggles in the main menu will result in a photo being taken instantly before the selected command to eliminate timing issues. Any photos taken prior to another command in this manner are marked "Bad" and can optionally be deleted to free space.
