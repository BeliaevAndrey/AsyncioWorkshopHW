from datetime import datetime as _dt
import traceback


class SLogger:

    def __init__(self, name: str, /, logfile: str = None, display_on: bool = True):
        if logfile is None:
            self._logfile = 'server_logfile.log'
        else:
            self._logfile = logfile
        self._display_on = display_on
        self.name = name

    def log(self, log_string):
        time = _dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(self._logfile, 'a', encoding='utf-8') as f_out:
            f_out.write(f'{time} at {self.name}: {log_string}\n')
        if self._display_on:
            print(f'\033[32m{time} at {self.name}: {log_string}\033[0m')

    def log_exc(self, log_exc):
        time = _dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(self._logfile, 'a', encoding='utf-8') as f_out:
            f_out.write(f'{time} at {self.name}: Exception: {log_exc.__class__.__name__} {log_exc}\n')
        if self._display_on:
            print(f'\033[31mException on {time} at {self.name} {log_exc}')
            traceback.print_exc()
            print('\033[0m')
