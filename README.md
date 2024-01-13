# Folder Monitor
<p align="center">
<img src="https://github.com/theanine3D/folder_monitor/assets/88953117/922ed794-f0d9-4f7d-bf7e-4a19c30743dc">
</p>
<p align="center">
A simple, portable, lightweight app that monitors a specified folder and logs any changes to its contained files.
</p>

### Installation
You can download a compiled binary from the Releases page. This is the easiest method, as it requires no installation. The executable is fully portable and can be placed anywhere on your hard drive.

Alternatively, you can download the source code and run the Python file via the command line. You will need to first install the dependencies via the command:
```
pip install PySimpleGUI watchdog
```
and then open a command prompt and use the command:
```
python folder_monitor.py
```

### Use Cases
I created Folder Monitor because I needed to locate a specific file being loaded by a game. This game uses obfuscated/hashed filenames for its datafiles (such as models, textures, etc.), which makes it very difficult to locate any specific file. However, by starting the monitoring in this program, and then going to a specific level in the game, all of the files being loaded in that level were logged by Folder Monitor. Locating specific files this way makes it now trivially easy with Folder Monitor. See screenshot below.

### Preview
![image](https://github.com/theanine3D/folder_monitor/assets/88953117/398c0f18-43e8-4706-b1ec-6f5700ed27bc)

