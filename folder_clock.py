import argparse
import datetime
import time
import os

class FolderClock:
    ''' Folder clock class. '''
    def __init__(self, wd="", mode=0):
        self.wd = wd
        self.mode = mode
        self.time = None
        self.fname = None
        self.period = None
        self.prev = None

    def run(self):
        ''' Start displaying the folder clock. '''
        while True:
            self.update()
            delta = 60 - datetime.datetime.now().second
            time.sleep(delta)  # Sleep until minute changes

    def update(self):
        ''' Create a folder with the time as its name. '''
        if self.wd == "":
            self.wd = self.get_wd()
        self.time = self.get_time()
        self.fname = self.wd + '/' + '.'.join(self.time)
        if self.mode == 12:
            self.fname = self.fname + ' ' + self.period
        self.make_folder()
        if self.prev:
            self.delete_prev()
        self.prev = self.fname

    def get_time(self):
        ''' Return list of current hour, minute, and second. '''
        t = time.localtime()
        time_str = time.strftime("%H:%M", t)
        current_time = time_str.split(":")

        # Handle 12h mode
        if self.mode == 12:
            self.period = 'AM' if int(current_time[0]) < 12 else 'PM'
            current_time[0] = str(int(current_time[0]) - 12)
        return current_time

    def get_wd(self):
        ''' Return the current working directory. '''
        return os.getcwd()

    def make_folder(self):
        ''' Create folder self.fname. '''
        try:
            os.mkdir(self.fname)
        except OSError:
            print("Creation of the directory %s failed" % self.fname)

    def delete_prev(self):
        ''' Delete the previously created folder. '''
        try:
            os.rmdir(self.prev)
        except OSError:
            print("Deletion of the directory %s failed" % self.prev)

    def h24_to_h12(self):
        ''' Return hour (t[0]) in 12 hr format. '''
        h = int(self.time[0])
        self.period = 'am' if h < 12 else 'pm'
        return h if h < 12 else h - 12


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wd", help="dir to display the folder-clock")
    parser.add_argument("--mode", help="either 12 or 24 hr mode")
    args = parser.parse_args()
    wd = args.wd if args.wd is not None else ""
    mode = int(args.mode) if args.mode is not None else ""
    return wd, mode

def main():
    ''' Run the clock. '''
    wd, mode = get_args()
    fc = FolderClock(wd=wd, mode=mode)
    fc.run()

if __name__ == '__main__':
    main()
