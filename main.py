import sys
from PyQt5 import QtWidgets

from lstc_gridviewer import LstcGridViewer

def main(argv):
    app = QtWidgets.QApplication(argv)

    with open(argv[1]) as f:
        urls = f.readlines()

    gridViewer = LstcGridViewer(urls)
    gridViewer.showFullScreen()
    return app.exec_()

def help():
    helpStr = '''\
    Usage example : python main.py watchlist
    This app take a file which contains the desired ls-tc.de links
    to be displayed. Each link is separated by newline.
    Example content of the watchlist file:
    ```
    https://www.ls-tc.de/en/stock/xilinx-dl-01-aktie
    https://www.ls-tc.de/en/stock/airbus-group-se-aktie
    https://www.ls-tc.de/en/stock/advanced-mic-dev-dl-01-aktie
    https://www.ls-tc.de/en/stock/micron-techn-dl-10-aktie
    ```
    Maximum number of view is 4 and this app only support urls from ls-tc.de .
    '''
    print(helpStr)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        help()
        sys.exit(-1)

    sys.exit(main(sys.argv))