from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
import json
# Variables
"""
notes = {"Welcome":
        {"text":"You can create notes here",
         "tags":["Smart notes","instruction"],
        }
    }
"""

with open("note_saves.json", "r", encoding = "utf-8") as jsonfile:
    notes = json.load(jsonfile)
# Functions
def show_note():
    try:
        name = notes_list.selectedItems()[0].text()
        text_edit.setText(notes[name]["text"])
        tags_list.clear()
        tags_list.addItems(notes[name]["tags"])
    except:
        tags_list.addItem(notes[name]["tags"])

def add_note():
    user_input, TF = QInputDialog.getText(window, "Adding note","Note name:")
    if TF:
        notes[user_input] = {"text":"","tags":[]}
        notes_list.clear()
        notes_list.addItems(notes)

def del_note():
    try:
        selected = notes_list.selectedItems()[0].text()
        del notes[selected]
        with open("note_saves.json", "w", encoding = "utf-8") as jsonfile:
            json.dump(notes, jsonfile)
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes)
        text_edit.clear()
    except: 
        mbox = QMessageBox()
        mbox.setWindowTitle("Error")
        mbox.setText("Select any note")
        mbox.exec_()

def save_note():
    try:
        selected = notes_list.selectedItems()[0].text()
        notes[selected]["text"] = text_edit.toPlainText()
        with open("note_saves.json", "w", encoding = "utf-8") as jsonfile:
            json.dump(notes, jsonfile)
    except: 
        mbox = QMessageBox()
        mbox.setWindowTitle("Error")
        mbox.setText("Select any note")
        mbox.exec_()

def add_tag():
    try:
        selected = notes_list.selectedItems()[0].text()
        if not tags_line.text() in notes[selected]["tags"] and tags_line.text() != '':
            notes[selected]["tags"].append(tags_line.text())
            with open("note_saves.json", "w", encoding = "utf-8") as jsonfile:
                json.dump(notes, jsonfile)
            tags_list.addItem(tags_line.text())
        print(notes)
    except:
        mbox = QMessageBox()
        mbox.setWindowTitle("Error")
        mbox.setText("Select any note")
        mbox.exec_()

def del_tag():
    try:
        selected_note = notes_list.selectedItems()[0].text()
        selected_tag = tags_list.selectedItems()[0].text()
        notes[selected_note]["tags"].remove(selected_tag)
        with open("note_saves.json", "w", encoding = "utf-8") as jsonfile:
            json.dump(notes, jsonfile)
        tags_list.clear()
        tags_list.addItems(notes[selected_note]["tags"])
    except:
        mbox = QMessageBox()
        mbox.setWindowTitle("Error")
        mbox.setText("Select any tag")
        mbox.exec_()

def search_tag():
    searching_tag = tags_line.text()
    if button_search_tag.text() == "Search note for tag" and searching_tag:
        notes_filtered = {}
        for note in notes:
            if searching_tag in notes[note]["tags"]:
                notes_filtered[note] = notes[note]
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes_filtered)
        button_search_tag.setText("Reset search")
    elif button_search_tag.text() == "Reset search":
        tags_line.clear()
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes)
        button_search_tag.setText("Search note for tag")

app = QApplication([])
window = QWidget()
window.setWindowTitle('Smart notes')
window.resize(600,400)

### Widgets ###
text_edit = QTextEdit()
label1 = QLabel('Notes list')
notes_list = QListWidget()
# Hline 1
button_create_note = QPushButton('Create note')
button_delete_note = QPushButton('Delete note')
#/
button_save_note = QPushButton('Save note')
label2 = QLabel('Tags list')
tags_list = QListWidget()
tags_line = QLineEdit()
tags_line.setPlaceholderText('Enter the tag')
# Hline 2
button_add_to_note = QPushButton('Add to note')
button_delete_from_note = QPushButton('Remove from note')
#/
button_search_tag = QPushButton('Search note for tag')
### Layouts
hlayout_main = QHBoxLayout()
vlayout = QVBoxLayout()
hlayout_1 = QHBoxLayout()
hlayout_2 = QHBoxLayout()
### Position
vlayout.addWidget(label1)
vlayout.addWidget(notes_list)
# Hline 1
hlayout_1.addWidget(button_create_note)
hlayout_1.addWidget(button_delete_note)
vlayout.addLayout(hlayout_1)
#/
vlayout.addWidget(button_save_note)
vlayout.addWidget(label2)
vlayout.addWidget(tags_list)
vlayout.addWidget(tags_line)
# Hline 2
hlayout_2.addWidget(button_add_to_note)
hlayout_2.addWidget(button_delete_from_note)
vlayout.addLayout(hlayout_2)
#/
vlayout.addWidget(button_search_tag)
#main
hlayout_main.addWidget(text_edit)
hlayout_main.addLayout(vlayout)
### Connections
notes_list.itemClicked.connect(show_note)
button_create_note.clicked.connect(add_note)
button_delete_note.clicked.connect(del_note)
button_save_note.clicked.connect(save_note)
button_add_to_note.clicked.connect(add_tag)
button_delete_from_note.clicked.connect(del_tag)
button_search_tag.clicked.connect(search_tag)
### window.setLayout()
window.setLayout(hlayout_main)
notes_list.addItems(notes)
window.show()
app.exec_()