import os
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import utility_func as uf

home = str(Path.home())

managed_dir_name = "Clean"
folder_to_track = os.path.join(home, "Downloads")

ignore_files = [".DS_Store", ".download"]


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename_w_ext in os.listdir(folder_to_track):
            if filename_w_ext != managed_dir_name and not any(
                [pattern in filename_w_ext for pattern in ignore_files]
            ):
                # try:
                filename = os.path.splitext(filename_w_ext)[0]
                extension = os.path.splitext(filename_w_ext)[1] or "noname"

                # get directory as per the extension
                # get noname by default if file extension does not exist
                ext_dir = extensions_dirs.get(
                    extension, extensions_dirs.get("noname")
                )

                # get_source_path
                src = uf.get_absolute_file_source_path(
                    folder_to_track, filename_w_ext
                )

                # get_destination_path
                dest = uf.get_absolute_file_destination_path(
                    ext_dir, filename_w_ext
                )

                # if destination path exists rename the file name and
                # check again
                i = 0
                extension = extension if extension != "noname" else ""
                while os.path.isfile(dest):
                    i += 1
                    new_name = f"{filename} ({str(i)})"
                    dest = uf.get_absolute_file_destination_path(
                        ext_dir, new_name + extension
                    )
                print(dest)

                # found file name unique move it
                os.rename(src, dest)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        folder_to_track = args[1]
        managed_dir_name = args[2]

    managing_dir_abs_path = os.path.join(folder_to_track, managed_dir_name)

    if not os.path.exists(managing_dir_abs_path):
        uf.create_path(managing_dir_abs_path)

    extensions_dirs = uf.get_mapping_dict(managing_dir_abs_path)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
