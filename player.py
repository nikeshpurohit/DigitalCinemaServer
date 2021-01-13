import platform
import os
import sys
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
from PySide2 import QtWidgets, QtGui, QtCore
import vlc
import cherrypy
import threading

class WebServer(QtCore.QThread):
    def run(self):
        cherrypy.tree.mount(self, '/')
        cherrypy.engine.start()

    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="web_open_file">
              <button type="submit">run action in qt</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def settings(self):
        return "here is where the settings page will be"

    @cherrypy.expose
    def web_open_file(self):
        self.player.play_file("filename")
        return

    def set_player(self, plr):
        self.player = plr

class VideoPlayer():
    def __init__(self):
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.is_paused = False

    def get_instance(self):
        return self.instance

    def get_media_player(self):
        return self.mediaplayer

    def is_playing(self):
        return self.mediaplayer.is_playing

    def play_file(self, filename):
        filename = "D:/dts-x-out-of-the-box-long-(www.demolandia.net).mkv"
        self.media = self.instance.media_new(filename)
        self.mediaplayer.set_media(self.media)
        self.media.parse()

        self.play_pause()

    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            #self.playbutton.setText("Play")
            self.is_paused = True
            #self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return

            self.mediaplayer.play()
            #self.playbutton.setText("Pause")
            #self.timer.start()
            self.is_paused = False

class DisplayWindow(QtWidgets.QMainWindow):

    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Display0")

        # Create a basic vlc instance
        # self.instance = vlc.Instance()
        #
        # self.media = None
        #
        # # Create an empty vlc media player
        # self.mediaplayer = self.instance.media_player_new()
        vlc2 = VideoPlayer()
        self.connect_vlc(vlc2)
        self.create_ui()
        self.draw_on_window()
        # self.is_paused = False

    def draw_on_window(self):
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.mediaplayer.set_hwnd(int(self.videoframe.winId()))
            print("using behaviour mitigation for windows: borderless fullscreen: windows")
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

    def connect_vlc(self, plr):
        self.mediaplayer = plr

    def get_vlc(self):
        return self.mediaplayer

    def create_ui(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        #self.setContentsMargins(0, 0, 0, 0)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin": # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        #self.videoframe.setContentsMargins(0,0,0,0)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.setContentsMargins(0,0,0,0)
        #self.vboxlayout.addWidget(self.positionslider)
        #self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)


        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

    # def play_pause(self):
    #     """Toggle play/pause status
    #     """
    #     if self.mediaplayer.is_playing():
    #         self.mediaplayer.pause()
    #         self.playbutton.setText("Play")
    #         self.is_paused = True
    #         self.timer.stop()
    #     else:
    #         if self.mediaplayer.play() == -1:
    #             self.open_file()
    #             return
    #
    #         self.mediaplayer.play()
    #         #self.playbutton.setText("Pause")
    #         self.timer.start()
    #         self.is_paused = False
    #
    # def stop(self):
    #     #stop player
    #     self.mediaplayer.stop()
    #     #self.playbutton.setText("Play")
    #
    #     #stop web server
    # def play_file(self, filename):
    #     filename = "D:/dts-x-out-of-the-box-long-(www.demolandia.net).mkv"
    #     self.media = self.instance.media_new(filename)
    #     self.mediaplayer.set_media(self.media)
    #     self.media.parse()
    #
    #     if platform.system() == "Linux": # for Linux using the X Server
    #         self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
    #     elif platform.system() == "Windows": # for Windows
    #         self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
    #         print("using behaviour mitigation for windows: borderless fullscreen: windows")
    #     elif platform.system() == "Darwin": # for MacOS
    #         self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
    #
    #     self.play_pause()
    #
    # def open_file(self):
    #     """Open a media file in a MediaPlayer
    #     """
    #
    #     dialog_txt = "Choose Media File"
    #     filename = QtWidgets.QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
    #     if not filename:
    #         return
    #
    #     print("file name:", filename)
    #
    #     # getOpenFileName returns a tuple, so use only the actual file name
    #     self.media = self.instance.media_new(filename[0])
    #
    #     # Put the media in the media player
    #     self.mediaplayer.set_media(self.media)
    #
    #     # Parse the metadata of the file
    #     self.media.parse()
    #
    #     # Set the title of the track as window title
    #     self.setWindowTitle(self.media.get_meta(0))
    #
    #     # The media player has to be 'connected' to the QFrame (otherwise the
    #     # video would be displayed in it's own window). This is platform
    #     # specific, so we must give the ID of the QFrame (or similar object) to
    #     # vlc. Different platforms have different functions for this
    #     if platform.system() == "Linux": # for Linux using the X Server
    #         self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
    #     elif platform.system() == "Windows": # for Windows
    #         self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
    #         print("using behaviour mitigation for windows: borderless fullscreen: windows")
    #     elif platform.system() == "Darwin": # for MacOS
    #         self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
    #
    #     self.play_pause()
    #
    # def set_volume(self, volume):
    #     """Set the volume
    #     """
    #     self.mediaplayer.audio_set_volume(volume)
    #
    # def set_position(self):
    #     """Set the movie position according to the position slider.
    #     """
    #
    #     # The vlc MediaPlayer needs a float value between 0 and 1, Qt uses
    #     # integer variables, so you need a factor; the higher the factor, the
    #     # more precise are the results (1000 should suffice).
    #
    #     # Set the media position to where the slider was dragged
    #     self.timer.stop()
    #     pos = self.positionslider.value()
    #     self.mediaplayer.set_position(pos / 1000.0)
    #     self.timer.start()

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        #media_pos = int(self.mediaplayer.get_position() * 1000)
        #self.positionslider.setValue(media_pos)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            if not self.is_paused:
                self.stop()

def start_client():
    #Entrypoint for our gui thread
    app = QtWidgets.QApplication(sys.argv)
    dw = DisplayWindow()
    dw.showFullScreen()
    dw.resize(1280, 720)

    # Entrypoint for our server thread
    httpd = WebServer()
    httpd.run()
    httpd.set_player(dw.get_vlc())

    app.exec_()



if __name__ == "__main__":
    start_client()
    #server_thread=threading.Thread(target=start_server)
