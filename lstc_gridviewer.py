from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

class LstcGridViewer(QtWidgets.QWidget):
    DEFAULT_SCREEN_WIDTH = 1920
    DEFAULT_ZOOM_FACTOR = 0.95
    DEFAULT_SCROLL_X = 480
    MAX_ROW = 2
    MAX_COLUMN = 2
    LSTC_DOMAIN = "ls-tc.de"
    JS_REMOVE_FIXED_TOP = '''
        function findFirstDescendant(parent, tagname)
        {
            let p = document.getElementById(parent);
            var descendants = p.getElementsByTagName(tagname);
            if ( descendants.length )
                return descendants[0];
            return null;
        }
        let headerNav = findFirstDescendant("main_layout", "nav");
        if (headerNav) headerNav.setAttribute("class", "navbar navbar-default");
        '''

    def __init__(self, urls:list):
        super().__init__()
        self.gridLayout = None
        self.webEngineViews = []

        self._setup(urls)


    def _onLoadFinished0(self, success:bool):
        self._onLoadFinished(0, success)

    def _onLoadFinished1(self, success:bool):
        self._onLoadFinished(1, success)

    def _onLoadFinished2(self, success:bool):
        self._onLoadFinished(2, success)

    def _onLoadFinished3(self, success:bool):
        self._onLoadFinished(3, success)

    def _onLoadFinished(self, index:int, success:bool):
        if success:
            self.webEngineViews[index].page().runJavaScript(LstcGridViewer.JS_REMOVE_FIXED_TOP)
            self.webEngineViews[index].page().runJavaScript("window.scrollTo({}, {});".format(0, LstcGridViewer.DEFAULT_SCROLL_X))


    def _addUrl(self, url:str):
        maxEntries = LstcGridViewer.MAX_COLUMN * LstcGridViewer.MAX_ROW
        if len(self.webEngineViews) >= maxEntries :
            raise RuntimeError("This app only supports maximum {} views.".format(maxEntries))

        url = url.strip()

        if len(url) == 0:
            return

        # Check if the url is from ls-tc.de
        if LstcGridViewer.LSTC_DOMAIN not in url:
            print("WARNING: {} does not belong to ls-tc.de domain. This url will be ignored.".format(url))
            return

        webEngineView = QtWebEngineWidgets.QWebEngineView(self)
        webEngineView.setUrl(QtCore.QUrl(url))
        webEngineView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.webEngineViews.append(webEngineView)


    def _setup(self, urls:list):
        self.gridLayout = QtWidgets.QGridLayout(self)

        for url in urls:
            self._addUrl(url)

        for row in range(0, LstcGridViewer.MAX_ROW):
            for column in range(0, LstcGridViewer.MAX_COLUMN):
                currentWebViewIndex = column + row * LstcGridViewer.MAX_ROW

                if currentWebViewIndex >= len(self.webEngineViews):
                    # There's no url for this grid element.
                    continue
                else:
                    self._registerOnLoaded(currentWebViewIndex)
                    self.gridLayout.addWidget(self.webEngineViews[currentWebViewIndex], row, column)


    def _registerOnLoaded(self, currentWebViewIndex:int):
        if currentWebViewIndex == 0 :
            self.webEngineViews[currentWebViewIndex].loadFinished.connect(self._onLoadFinished0)
        elif currentWebViewIndex == 1:
            self.webEngineViews[currentWebViewIndex].loadFinished.connect(self._onLoadFinished1)
        elif currentWebViewIndex == 2:
            self.webEngineViews[currentWebViewIndex].loadFinished.connect(self._onLoadFinished2)
        elif currentWebViewIndex == 3:
            self.webEngineViews[currentWebViewIndex].loadFinished.connect(self._onLoadFinished3)


    def resizeEvent(self, resizeEvent):
        newZoomFactor = resizeEvent.size().width() * LstcGridViewer.DEFAULT_ZOOM_FACTOR / LstcGridViewer.DEFAULT_SCREEN_WIDTH
        for view in self.webEngineViews:
            view.setZoomFactor(newZoomFactor)
        super().resizeEvent(resizeEvent)