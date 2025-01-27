from PyQt6 import QtCore

class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    def setFunction(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        

    def run(self):
        if self.fn is None:
            return
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.result.emit(result)
        except Exception as e:
            print(f"Error in worker function: {e}")
        finally:
            self.finished.emit()
    