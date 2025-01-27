def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    vm = BoardViewModel()
    win = BoardMainWindow(vm)
    win.setup()
    win.show()
    sys.exit(app.exec())