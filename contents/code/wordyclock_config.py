# -*- coding: utf-8 -*-
# Copyright (C) 2012  Biel Frontera <biel.fb@gmail.com>
# 
# Adapted from gmailconfig.py (http://code.google.com/p/gmail-plasmoid/source/browse/trunk/contents/code/gmailconfig.py)
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
from PyQt4 import uic
from PyKDE4.kio import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *


class WordyClock_config(QWidget):
    def __init__(self, parent, settings):
        QWidget.__init__(self)
        self.ui = uic.loadUi(parent.package().filePath('ui', 'wordyclock_configform.ui'), self)
        self.addChildrenAsMembers(self.ui)
        
        self.parent = parent
        
        self.fonTextFont.setOnlyFixed(True)
        self.fonTextFont.setCurrentFont(QFont(settings["textfont"]))
        self.intTextSize.setValue(settings["textbasesize"])
        self.colColor.setColor(QColor(settings["textcolor"]))
        self.colColor2.setColor(QColor(settings["textbgcolor"]))        
        self.langs = (
            ('Catalan - Mallorca', 'ca_ma'),
            ('English', 'en'),
            ('Español', 'es'),
            )
        self.cmbLang.clear()
        currentIndex = 0
        for i in self.langs:
            self.cmbLang.addItem(i18n(i[0]))
            if settings["lang"] == i[1]:
                self.cmbLang.setCurrentIndex(currentIndex)
            currentIndex = currentIndex + 1
        
        
    def addChildrenAsMembers(self, widget):
        for w in widget.children():
            if w.inherits('QWidget'):
                try:
                    if w.objectName() != '':
                        self.__dict__[str(w.objectName())] = self.ui.findChild(globals()[w.metaObject().className()], w.objectName())
                        self.addChildrenAsMembers(self.__dict__[str(w.objectName())])
                except:
                    print '[wordyclock_config] Not using ' + w.metaObject().className() + ':' + str(w.objectName()) + ' as child.'        
    
    
    # ---- Export Commands ---- #
    
    def getItem(self, item, key):
        # FIXME: This is a hack is used by convertAccount to get around different versions of the
        # QT bindings returning different data types.
        if item.has_key(key):
            return item[key]
        elif item.has_key(QString(key)):
            return item[QString(key)]
        else:
            raise KeyError    
    
    def exportSettings(self):
        settings = {}
        
        # General settings
        font = self.fonTextFont.currentFont()
        settings["textfont"] = unicode(font.family())
        settings["textbasesize"] = self.intTextSize.value()
        settings["textcolor"] = unicode(self.colColor.color().name())
        settings["textbgcolor"] = unicode(self.colColor2.color().name())
        settings["lang"] = self.langs[self.cmbLang.currentIndex()][1]
        
        return settings
