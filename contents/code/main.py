# -*- coding: utf-8 -*-
#
# Copyright (C) 2012  Biel Frontera <biel.fb@gmail.com>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.plasma import *
from PyKDE4 import plasmascript
from PyKDE4.kio import *
from PyKDE4.solid import *

from time import localtime
from wordyclock import *
from wordyclock_config import WordyClock_config

import sys, os, commands, glob, pickle



 
class WordyClock_plasmoid(plasmascript.Applet):
    
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
 
    def init(self): 
        self.debug = False
        
        self.setHasConfigurationInterface(True)
        self.resize(440, 440)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.TranslucentBackground)
        self.setAspectRatioMode(Plasma.Square)
        
        # Setup configuration // from http://code.google.com/p/gmail-plasmoid/source/browse/trunk/contents/code/main.py        
        vers = {}
        vers["wordyclock_plasmoid.notifyrc"] = "10"
        self.settings = {}
        gc = self.config()
        
        # General settings
        self.settings["textfont"] = self.fixType(gc.readEntry("textfont", ""))
        self.settings["textbasesize"] = int(self.fixType(gc.readEntry("textbasesize", "30")))
        self.settings["textcolor"] = self.fixType(gc.readEntry("textcolor", "blue"))
        self.settings["textbgcolor"] = self.fixType(gc.readEntry("textbgcolor", "white"))
        self.settings["lang"] = self.fixType(gc.readEntry("lang", "ca_ma"))
        self.fontSize = self.settings["textbasesize"] 
        
         # Create notifyrc file if required
        kdehome = unicode(KGlobal.dirs().localkdedir())
        if not os.path.exists(kdehome+"share/apps/wordyclock_plasmoid/wordyclock_plasmoid.notifyrc"):
            if os.path.exists(kdehome+"share/apps"):
                self.createNotifyrc(kdehome, vers)
        else:
            # Update if the version string does not match
            ver = self.fixType(gc.readEntry("wordyclock_plasmoid.notifyrc", "0"))
            if ver <> vers["wordyclock_plasmoid.notifyrc"]:
                if self.debug: print "[wordyclock_plasmoid] Update .notifyrc file..."
                self.createNotifyrc(kdehome, vers)
                
        # Get default font if font not set
        if self.settings["textfont"] == "":
            # FIXME: There must be a better way to get the default font.            
            font = QFont("DejaVu Sans Mono", self.fontSize)
            font.setStyleHint(QFont.Monospace)
            self.settings["textfont"] = unicode(font.family())
        
        #set timer interval in ms (1000=1s)
        self.startTimer(60000)
        
    #done when timer is resetted
    def timerEvent(self, event):
        #call draw method
        self.update()
            
    def constraintsEvent(self,constraint):
        # Recalculate fontSize 
        self.fontSize = int(self.size().width() / 15.0 ) + self.settings["textbasesize"] - 30
 
    def paintInterface(self, painter, option, rect):
        clock = localtime()
        hour, minutes = roundToClosest5Minutes(clock.tm_hour, clock.tm_min)
        wordyTime = convertToWords(hour, minutes,self.settings["lang"])
        
        painter.save()
        font = QFont(self.settings["textfont"], self.fontSize)
        font.setStyleHint(QFont.Monospace)
        font.setLetterSpacing(QFont.PercentageSpacing, 180)
        painter.setFont(font)
        painter.setPen(QColor(self.settings["textbgcolor"]))
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, clockFace[self.settings["lang"]])
        
        painter.setPen(QColor(self.settings["textcolor"]))
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, blankOutTargetFromBase(wordyTime.upper(), clockFace[self.settings["lang"]]))
        painter.restore()
            
    def fixType(self, val):
        # FIXME: This is needed to take care of problems with KDE 4.3 bindings, but it should be removed
        # when things are fixed.
        if type(val) == QVariant:
            return str(val.toString())
        else:
            return val    
            
    def createDirectory(self, d):
        if not os.path.isdir(d):
            try:
                os.mkdir(d)
            except:
                print "[wordyclock_plasmoid] Problem creating directory: "+d
                print "[wordyclock_plasmoid] Unexpected error:", sys.exc_info()[0]
    
    def createNotifyrc(self, kdehome, vers):
        # Output the notifyrc file to the correct location
        print "[wordyclock_plasmoid] Outputting notifyrc file"
        
        # Create gmail-plasmoid directory if required
        self.createDirectory(kdehome+"share/apps/wordyclock_plasmoid")
        
        # File to create
        fn = kdehome+"share/apps/wordyclock_plasmoid/wordyclock_plasmoid.notifyrc"
        
        # File contents
        c = []
        c.append("[Global]\n")
        c.append("Comment=wordyclock plasmoid\n")
        c.append("Name=WordyClock_plasmoid\n")
        c.append("\n")
        
        # Write file
        try:
            f = open(fn,"w")
            f.writelines(c)
            f.close()
            # Update saved version
            gc = self.config()
            gc.writeEntry("wordyclock_plasmoid.notifyrc", vers["wordyclock_plasmoid.notifyrc"])
        except:
            print "[wordyclock_plasmoid Problem writing to file: "+fn
            print "[wordyclock_plasmoid] Unexpected error:", sys.exc_info()[0]            

    #
    # ---------- Configuration ----------
    #
        
    def createConfigurationInterface(self, parent):
        # Settings page
        self.wordyclock_config = WordyClock_config(self, self.settings)        
        p = parent.addPage(self.wordyclock_config, i18n("Appearance"))        
        p.setIcon( KIcon("preferences-desktop-color") )
        
        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)
        
            
    def isKDEVersion(self, a, b, c):
      return (version() >= (a << 16) + (b << 8) + c)
    
    def showConfigurationInterface(self):
        # KDE 4.4 and above
        if self.isKDEVersion(4,3,74):
            plasmascript.Applet.showConfigurationInterface(self)
            return
        
        # KDE 4.3
        cfgId = QString('%1settings%2script').arg(self.applet.id()).arg(self.applet.name())
        if KConfigDialog.showDialog(cfgId):
            return
        self.nullManager = KConfigSkeleton()
        self.dlg = KConfigDialog(None, cfgId, self.nullManager)
        self.dlg.setFaceType(KPageDialog.Auto)
        self.dlg.setWindowTitle(i18nc('@title:window', '%1 Settings', self.applet.name()))
        self.dlg.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dlg.showButton(KDialog.Apply, False)
        self.connect(self.dlg, SIGNAL('finished()'), self.nullManager, SLOT('deleteLater()'))
        
        self.createConfigurationInterface(self.dlg)
        self.dlg.show() 
    
    def configAccepted(self):
        self.settings = self.wordyclock_config.exportSettings()
        gc = self.config()
        
        # Write general items
        gc.writeEntry("textfont", self.settings["textfont"])
        gc.writeEntry("textbasesize", str(self.settings["textbasesize"]))
        gc.writeEntry("textcolor", self.settings["textcolor"])
        gc.writeEntry("textbgcolor", self.settings["textbgcolor"])        
        gc.writeEntry("lang", self.settings["lang"])
        # fontSize is dynamic. For 440px & DejaVu Mono, 30 fits the widget. With textbasesize diferent from 30, the user can modify this value
        self.fontSize = int(self.size().width() / 15.0 ) + self.settings["textbasesize"] - 30
                
        # Clean up
        self.configDenied()        
        self.update()

    def configDenied(self):
        if self.debug: print "[wordyclock_plasmoid] Config denied."        
        
        
    #
    # ---------- End Configuration ----------
    #            
 
def CreateApplet(parent):
    return WordyClock_plasmoid(parent)
