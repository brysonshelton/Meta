#!/usr/bin/env python3

import eyed3
import sys
import os
import getpass
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic


class Meta(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(f'{BASE_PATH}', 'meta.ui'), self)
        self.setWindowTitle('Meta Data Editor')
        self.btnCancel.clicked.connect(self.close)
        self.btnSave.clicked.connect(self.savefile)
        self.btnSelectSong.clicked.connect(self.selectfile)
        self.lblSelectedSong.setText('Choose a Song')
        self.user = getpass.getuser()
        self.musicpath = f'/Users/{self.user}/Music'
        self.populatebox()
        self.cmbGenre.setCurrentIndex(192)

    def selectfile(self):
        self.lblStatus.setText('')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Select Music File",
                                                  self.musicpath,
                                                  "Music Files (*.mp3)",
                                                  options=options)
        if fileName:
            self.audiofile = eyed3.load(fileName)
            self.lblSelectedSong.setText(
                fileName.rsplit('/', 1)[1].split('.')[0])
            self.txtArtist.setText(self.audiofile.tag.artist)
            self.txtAlbum.setText(self.audiofile.tag.album)
            self.txtTitle.setText(self.audiofile.tag.title)
            self.txtTrack.setText(str(self.audiofile.tag.track_num[0]))
            self.txtReleaseDate.setText(
                str(self.audiofile.tag.original_release_date))
            self.genre = self.audiofile.tag.genre
            if not self.genre:
                self.cmbGenre.setCurrentIndex(192)
            else:
                self.cmbGenre.setCurrentIndex(
                    int(str(self.genre).split('(')[1].split(')')[0]))

    def populatebox(self):
        genrelist = os.popen('eyeD3 --plugin=genres -1').read().split('\n')
        for item in genrelist:
            if item == '':
                continue
            genre = item.split(':')[1]
            num = item.split(':')[0]
            self.cmbGenre.addItem(genre, num)

    def savefile(self):
        self.lblStatus.setText('File Saved.')
        self.audiofile.tag.artist = self.txtArtist.text()
        self.audiofile.tag.album = self.txtAlbum.text()
        self.audiofile.tag.Title = self.txtTitle.text()
        self.audiofile.tag.Track = int(self.txtTrack.text())
        if self.txtReleaseDate.text() == 'None':
            self.audiofile.tag.original_release_date = ''
        else:
            self.audiofile.tag.original_release_date = int(
                self.txtReleaseDate.text())
        self.audiofile.tag.genre = self.cmbGenre.currentData()
        self.audiofile.tag.save()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Meta()
    win.show()
    sys.exit(app.exec())
