"""
Folder Monitor
Copyright (c) 2024 Pedro Valencia (Theanine3D)
Web: https://www.github.com/theanine3D
Discord: @theanine3D
Date: 2023-01-16

Description:
This program monitors a specified folder for any modifications to its contained files.
Each time the program detects a modification, it prints out the filename, with a timestamp.
If the file's metadata, such as "last access date", happen to change, the program also logs this.
Because of that, the program can also be used to log which specific files are being read.

License: GPLv3 License
"""


from time import strftime, localtime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import os
import FreeSimpleGUI as sg

version = "1.1"
watcher = None
thread = None

output = sg.Output(size=(120, 20), key='-OUTPUT-', expand_x=True, expand_y=True)

empty_space = sg.Text('', size=(1, 1), expand_x=True)

layout = [
    [sg.Text('Folder Path:'), sg.InputText(enable_events=True, key='-FOLDER-', size=(40, 1)), sg.Button('Browse'), sg.Button('Start', key='-START-'), sg.Button('Stop', key='-STOP-', disabled=True), empty_space, sg.Button('About')],
    [output]
]

window = sg.Window("Folder Monitor", layout, finalize=True, resizable=True, icon="icon.ico")

class Watcher:
    def __init__(self, directory_to_watch):
        self.observer = Observer()
        self.directory_to_watch = os.path.abspath(directory_to_watch)
        self.should_stop = threading.Event()

    def run(self):
        event_handler = Handler(self.directory_to_watch)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while not self.should_stop.wait(timeout=1):  # Wait for the stop signal
                pass
        finally:
            self.observer.stop()
            self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type in ('created', 'modified', 'deleted'):
            rel_path = os.path.relpath(event.src_path, self.watch_dir)
            timestamp = strftime('%H:%M:%S - %Y-%m-%d',localtime())
            filesize = None
            try:
                filesize = os.path.getsize(event.src_path)
            except:
                pass
            filesize_unit = "B"
            if filesize != None:
                if filesize >= 1048576:
                    filesize = filesize / 1024 / 1024
                    filesize_unit = "MB"
                elif filesize >= 1024:
                    filesize = filesize / 1024
                    filesize_unit = "KB"
            line = f"{timestamp} - {event.event_type.capitalize()}: - {rel_path}"
            if filesize != None:
                line += f" - {round(filesize,2)} {filesize_unit}"
            print(line)

def monitor_directory(directory_to_watch):
    global watcher, thread
    watcher = Watcher(directory_to_watch)
    thread = threading.Thread(target=watcher.run)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

        elif event == 'About':
            sg.popup_quick_message(f"Version {version}\n\nCreated by Theanine3D\n\ngithub.com/theanine3D")

        elif event == 'Browse':

            folder_path = sg.popup_get_folder("Select a folder")

            if folder_path:
                window['-FOLDER-'].update(folder_path)

        elif event == '-START-':
            
            folder_path = values['-FOLDER-']

            if os.path.isdir(folder_path):
                if watcher is None or not watcher.observer.is_alive():
                    monitor_directory(values['-FOLDER-'])
                    print(f"Started monitoring {folder_path}")
                    window['-START-'].update(disabled=True)
                    window['-STOP-'].update(disabled=False)
                else: 
                    print("A monitoring thread already exists! If this error persists, restart the program.")
            else:
                print("The folder you specified doesn't exist.")

        elif event == '-STOP-':

            if watcher and watcher.observer.is_alive():
                watcher.should_stop.set()  # Signal the watcher to stop
                thread.join(timeout=1)  # Timeout to prevent GUI freeze
                watcher = None  # Reset the watcher
                window['-START-'].update(disabled=False)
                window['-STOP-'].update(disabled=True)
                print("Stopped monitoring.")
            else:
                print("Not currently monitoring.")

    window.close()
