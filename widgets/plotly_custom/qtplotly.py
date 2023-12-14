import plotly.graph_objects as go
import plotly.offline as po
from PySide6 import QtWebEngineCore, QtCore

class PlotlySchemeHandler(QtWebEngineCore.QWebEngineUrlSchemeHandler):
    def __init__(self, heatmapsDict):
        super().__init__()
        self.heatmaps = heatmapsDict

    def requestStarted(self, request):
        url = request.requestUrl()
        name = url.host()
        if self.heatmaps.__contains__(name):
            fig = self.heatmaps[name].fig
            if isinstance(fig, go.Figure):
                raw_html = '<html><head><meta charset="utf-8" />'
                raw_html += "<body>"
                raw_html += po.plot(fig, include_plotlyjs=True, output_type="div")
                raw_html += "</body></html>"
                
                buf = QtCore.QBuffer(parent=self)
                request.destroyed.connect(buf.deleteLater)
                buf.open(QtCore.QIODevice.WriteOnly)
                buf.write(raw_html.encode())
                buf.seek(0)
                buf.close()
                request.reply(b"text/html", buf)
                return
        request.fail(QtWebEngineCore.QWebEngineUrlRequestJob.UrlNotFound)


class PlotlyApplication(QtCore.QObject):
    scheme = b"plotly"

    def __init__(self, parent=None):
        super().__init__(parent)
        scheme = QtWebEngineCore.QWebEngineUrlScheme(PlotlyApplication.scheme)
        QtWebEngineCore.QWebEngineUrlScheme.registerScheme(scheme)
        
    def init_handler(self, heatmapDict, profile=None):
        if profile is None:
            profile = QtWebEngineCore.QWebEngineProfile.defaultProfile()
        handler = profile.urlSchemeHandler(PlotlyApplication.scheme)
        if handler is not None:
            profile.removeUrlSchemeHandler(handler)

        self.m_handler = PlotlySchemeHandler(heatmapDict)
        profile.installUrlSchemeHandler(PlotlyApplication.scheme, self.m_handler)
    
