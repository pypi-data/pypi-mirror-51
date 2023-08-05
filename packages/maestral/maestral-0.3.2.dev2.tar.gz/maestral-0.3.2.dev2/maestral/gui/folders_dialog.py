#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:23:13 2018

@author: samschott
"""

# external packages
from PyQt5 import QtCore, QtWidgets, uic
from dropbox import files

# maestral modules
from maestral.main import handle_disconnect
from maestral.gui.resources import FOLDERS_DIALOG_PATH, get_native_folder_icon


# noinspection PyTypeChecker
class FolderItem(QtWidgets.QListWidgetItem):

    def __init__(self, name, is_included, parent=None):
        icon = get_native_folder_icon()
        super(self.__class__, self).__init__(icon, name, parent=parent)

        self.name = name

        checked_state = 2 if is_included else 0
        self.setCheckState(checked_state)

    def setIncluded(self, is_included):
        checked_state = 2 if is_included else 0
        self.setCheckState(checked_state)

    def isIncluded(self):
        checked_state = self.checkState()
        return True if checked_state == 2 else False


class FoldersDialog(QtWidgets.QDialog):

    folder_items = []

    def __init__(self, mdbx,  parent=None):
        super(self.__class__, self).__init__(parent=parent)
        # load user interface layout from .ui file
        uic.loadUi(FOLDERS_DIALOG_PATH, self)
        self.setModal(True)

        self.mdbx = mdbx
        self.accept_button = self.buttonBox.buttons()[0]
        self.accept_button.setText('Update')

        self.listWidgetFolders.addItem("Loading your folders...")

        # connect callbacks
        self.buttonBox.accepted.connect(self.on_accepted)
        self.listWidgetFolders.itemChanged.connect(self.update_select_all_checkbox)
        self.selectAllCheckBox.clicked.connect(self.on_select_all_clicked)

    @handle_disconnect
    def populate_folders_list(self, overload=None):

        self.listWidgetFolders.clear()
        self.accept_button.setEnabled(False)

        if not self.mdbx.connected:
            self.listWidgetFolders.addItem("Cannot connect to Dropbox.")
            return

        # add new entries
        result = self.mdbx.client.list_folder("", recursive=False)
        self.folder_items = []

        for entry in result.entries:
            if isinstance(entry, files.FolderMetadata):
                is_included = not self.mdbx.sync.is_excluded_by_user(entry.path_lower)
                item = FolderItem(entry.name, is_included)
                self.folder_items.append(item)

        for item in self.folder_items:
            self.listWidgetFolders.addItem(item)

        self.update_select_all_checkbox()

        if not self.mdbx.connected:
            self.listWidgetFolders.clear()
            self.listWidgetFolders.addItem("Cannot connect to Dropbox.")
            self.accept_button.setEnabled(False)
        else:
            self.accept_button.setEnabled(True)

    def update_select_all_checkbox(self):
        is_included_list = (i.isIncluded() for i in self.folder_items)
        self.selectAllCheckBox.setChecked(all(is_included_list))

    def on_select_all_clicked(self, checked):
        for item in self.folder_items:
            item.setIncluded(checked)

    @handle_disconnect
    def on_accepted(self, overload=None):
        """
        Apply changes to local Dropbox folder.
        """

        if not self.mdbx.connected:
            return

        excluded_folders = []
        included_folders = []

        for item in self.folder_items:
            if not item.isIncluded():
                excluded_folders.append("/" + item.name.lower())
            elif item.isIncluded():
                included_folders.append("/" + item.name.lower())

        for path in excluded_folders:
            self.mdbx.exclude_folder(path)
        for path in included_folders:
            self.mdbx.include_folder(path)

        self.mdbx.sync.excluded_folders = excluded_folders

    def changeEvent(self, QEvent):

        if QEvent.type() == QtCore.QEvent.PaletteChange:
            self.update_dark_mode()

    def update_dark_mode(self):
        # update folder icons: the system may provide different icons in dark mode
        for item in self.folder_items:
            item.setIcon(get_native_folder_icon())
