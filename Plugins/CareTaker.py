import os
import psutil
from Mitten.Events import *
from Mitten import Configs

PLUGIN = __name__.split('.')[-1]

class CareTaker():
    def __init__(self, processName, path):
        self.processName = processName
        self.path = path
        self.exe = self.path + self.processName
        self._processName = 'Server.exe'
        self._exe = self.path + self._processName

    # Check output of this func to make sure it's not None
    def _GetRunningServer(self):
        try:
            for process in psutil.process_iter():
                if process.name() == self._processName:
                    if process.exe() == self._exe:
                        return process
        except Exception as e:
            print(f'[{PLUGIN}] Error in _GetRunningServer!\n'
                  f'* Error: {e}')
        return None

    def _StartServer(self):
        try:
            os.chdir(self.path)
            os.startfile(self.exe)
        except Exception as e:
            print(f'[{PLUGIN}] Could not start server!\n'
                  f'* In directory: {self.path}\n'
                  f'* Process: {self.processName}\n'
                  f'* Error: {e}')
            return
        print(f'[{PLUGIN}] Successfully started {self.processName}')

    def _CloseServer(self):
        serverProcess = self._GetRunningServer()
        if serverProcess is None: return
        try:
            serverProcess.kill()
        except Exception as e:
            print(f'[{PLUGIN}] Could not kill server!\n'
                  f'* Error: {e}')

    def RestartServer(self):
        self._CloseServer()
        self._StartServer()


# TODO: Instead of using hardcoded value, fetch from global config
# Initialize the caretaker :)
caretaker = CareTaker(
    Configs.GetAttribute(PLUGIN, 'internalExecutableName', 'Server.exe'),
    Configs.GetAttribute(PLUGIN, 'internalExecutablePath', os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    )) + '\\'
)

@Handle(OnServerFailure)
def FailureHandler(sock, server):
    print(f'[{PLUGIN}] Handling a server failure :o')
    caretaker.RestartServer()
    sock.connect(server)
