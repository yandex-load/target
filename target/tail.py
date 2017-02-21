import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ModifyHandler(FileSystemEventHandler):
    def __init__(self, path):
        super(ModifyHandler, self).__init__()
        self.path = path
        self.where = os.stat(path)[6]

    def on_modified(self, event):
        if self.path in event.src_path:
            with open(self.path, "r") as logfile:
                logfile.seek(self.where)
                lines = logfile.readlines()
                if len(lines) == 3:
                    try:
                        stats = {}
                        nobjects = [
                            int(v) for v
                            in lines[1].rstrip("\n").rsplit(":", 1)[1].split()
                        ]
                        for i, v in enumerate(nobjects):
                            stats["nobjects_%s" % i] = v
                        pairs = lines[2].rstrip("\n").split(",")[1:]

                        stats["unreachable"] = int(pairs[0].split()[0])
                        stats["uncollectable"] = int(pairs[1].split()[0])
                        stats["elapsed"] = float(
                            pairs[2].split()[0].rstrip("s"))
                        print(json.dumps({
                            "name": "gc",
                            "timestamp": int(time.time()),
                            "fields": stats,
                        }))
                    except:
                        pass
                self.where = logfile.tell()


def main():
    event_handler = ModifyHandler("./test.log")
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
