# Phone Book

import sqlite3
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from RadioButtonClass import * #provides the radio button widget


class DatabaseManager(object):
    def __init__(self):
        self.conn = sqlite3.connect("PhoneBook.db")
        self.cur = self.conn.cursor()
        self.cur.executescript('''CREATE TABLE IF NOT EXISTS
                                PhoneBook(
                                            FirstName TEXT COLLATE NOCASE,
                                            LastName TEXT COLLATE NOCASE,
                                            PhoneNumber INTEGER
                                        ); ''')
        self.cur.executescript('''CREATE TABLE IF NOT EXISTS
                                StatusBook(
                                            FirstUse INTEGER
                                        ); ''')
        self.conn.commit()

    def search_phonebook(self,keyWord):
        self.cur.execute('SELECT * FROM PhoneBook WHERE FirstName==? OR LastName==? OR PhoneNumber == ? ',(keyWord,keyWord,keyWord))
        return self.cur.fetchall()
    
    def showall_phonebook(self):
        self.cur.execute('SELECT * FROM PhoneBook GROUP BY FirstName')
        return self.cur.fetchall()


    def add_phonebook(self, firstNameEntered, lastNameEntered, phoneNumberEntered) :
        self.cur.execute('INSERT INTO PhoneBook VALUES(?,?,?)',(firstNameEntered,lastNameEntered,phoneNumberEntered))
        self.conn.commit()

    def delete_phonebook(self, firstNameEntered, lastNameEntered, phoneNumberEntered):
        self.cur.execute('DELETE FROM PhoneBook WHERE (FirstName==? OR LastName==?) AND PhoneNumber == ? ',(firstNameEntered,lastNameEntered,phoneNumberEntered))
        self.conn.commit()


#    def __del__(self) :
#        self.conn.close()


class PhoneBook(QMainWindow, DatabaseManager):
    """ this class creates the main window for the PhoneBook """

    #constructor
    def __init__(self):
        QMainWindow.__init__(self) #call super class constructor
        self.dbmgr = DatabaseManager()
        self.setWindowTitle("PhoneBook") #set window title
        
        #font properties for the text displayed inside status bar
        font = QFont()
        font.setPointSize(11)
        font.setWeight(30)
        self.statusBar_msg = QLabel()
        self.statusBar_msg.setFont(font)

        self.stacked_layout = QStackedLayout() #this holds the various layouts this window needs
        
        self.create_select_phonebookTask_layout()
        self.stacked_layout.addWidget(self.select_phonebookTask_widget)

        
#        
#        self.create_view_phonebookSearch_layout() #create the view phonebook search layout
#        self.stacked_layout.addWidget(self.view_phonebookSearch_widget) #add this to the stack
#        
#        self.create_view_phonebookShowall_layout()
#        self.stacked_layout.addWidget(self.view_phonebookShowall_widget) #add this to the stack
#        
#        self.create_view_phonebookAdd_layout() #create the view phonebook task layout
#        self.stacked_layout.addWidget(self.view_phonebookAdd_widget) #add this to the stack
#        
#        self.create_view_phonebookDelete_layout() #create the view phonebook task layout
#        self.stacked_layout.addWidget(self.view_phonebookDelete_widget) #add this to the stack

        
        #set the central widget to display the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        self.stacked_layout.setCurrentIndex(0) # change the visible layout in the task

    

    def create_select_phonebookTask_layout(self):
        #this is the initial layout of the the window - to select task type

        self.phonebook_radio_buttons = RadioButtonWidget("PhoneBook", "Please select the task", ("Search", "Show all", "Add", "Delete", "Quit"))
        self.instantiate_button = QPushButton("Select")

        #create layout to hold the widgets
        self.initial_layout = QVBoxLayout()
        self.initial_layout.addWidget(self.phonebook_radio_buttons)
        self.initial_layout.addWidget(self.instantiate_button)

        self.select_phonebookTask_widget = QWidget()
        self.select_phonebookTask_widget.setLayout(self.initial_layout)

        #connections
        self.instantiate_button.clicked.connect(self.instantiate_phonebook)
    
    def create_view_phonebookSearch_layout(self):
        #this is the second layout of the window - add the new contact

        self.keyWord_label = QLabel("Key word")

        self.keyWord_line_edit = QLineEdit()

        self.search_button = QPushButton("Search")
        self.cancel_button = QPushButton("Cancel")
        self.search_button.setFixedWidth(100)
        self.cancel_button.setFixedWidth(100)
        
        self.search_table = QTableWidget()
        self.search_table.setRowCount(0)
        self.search_table.setColumnCount(0)

        self.search_grid = QGridLayout()

        #add label and line edit widgets to the search layout
        self.search_grid.addWidget(self.keyWord_label,0,0)
        self.search_grid.addWidget(self.keyWord_line_edit,0,1)
        self.search_grid.addWidget(self.search_button,1,0)
        self.search_grid.addWidget(self.cancel_button,1,1)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.search_grid)
        self.main_layout.addWidget(self.search_table)
        
        #create a widget to display the main layout
        self.view_phonebookSearch_widget = QWidget()
        self.view_phonebookSearch_widget.setLayout(self.main_layout)
        self.view_phonebookSearch_widget.setFixedWidth(300)
        self.view_phonebookSearch_widget.setFixedHeight(300)
        
        #Message to display on status bar
        self.statusBar_msg.setText('Enter <i>First Name</i> OR <i>Last Name</i> OR <i>Phone Number</i>')
        self.statusBar().addWidget(self.statusBar_msg)

        #connections
        self.search_button.clicked.connect(self.task_search_phonebook)
        self.cancel_button.clicked.connect(self.task_cancel_phonebook)
    
    
    def create_view_phonebookShowall_layout(self):
        #this is the second layout of the window - add the new contact

        self.showall_data = self.showall_phonebook()
        self.showall_table = QTableWidget()
        self.showall_table.setRowCount(len(self.showall_data))
        self.showall_table.setColumnCount(3)
        self.showall_table.setHorizontalHeaderLabels(('First Name', 'Last Name', 'Phone Number'))
        
        row_count = 0
        column_count = 0
        for contact in self.showall_data :
            for field in contact :
                self.showall_table.setItem(row_count,column_count,QTableWidgetItem(str(field)))
                column_count=column_count+1
            column_count = 0
            row_count = row_count+1


        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.showall_table)
        
        #create a widget to display the main layout
        self.view_phonebookShowall_widget = QWidget()
        self.view_phonebookShowall_widget.setLayout(self.main_layout)
        self.view_phonebookShowall_widget.setFixedWidth(350)
        self.view_phonebookShowall_widget.setFixedHeight(350)


    def create_view_phonebookAdd_layout(self):
        #this is the second layout of the window - add the new contact

        self.firstName_label = QLabel("First Name")
        self.lastName_label = QLabel("Last Name")
        self.phoneNumber_label = QLabel("Phone Number")
        self.contactImage_label = QLabel()

        self.firstName_line_edit = QLineEdit()
        self.lastName_line_edit = QLineEdit()
        self.phoneNumber_line_edit = QLineEdit()

        #load the image and ensure for its scale
        pixmap_img = QPixmap("images/phonebook.png")
        self.contactImage_label.setPixmap(pixmap_img.scaled(182,242,Qt.KeepAspectRatio))


        self.ok_button = QPushButton("Ok")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.setFixedWidth(200)
        self.cancel_button.setFixedWidth(200)


        self.main_grid = QGridLayout()
        self.sub_grid = QGridLayout()

        #add label widgets to the sub layout
        self.sub_grid.addWidget(self.firstName_label,0,0)
        self.sub_grid.addWidget(self.lastName_label,1,0)
        self.sub_grid.addWidget(self.phoneNumber_label,2,0)
        

        #add line edit widgets to the sub layout
        self.sub_grid.addWidget(self.firstName_line_edit,0,1)
        self.sub_grid.addWidget(self.lastName_line_edit,1,1)
        self.sub_grid.addWidget(self.phoneNumber_line_edit,2,1)

        #add widgets/layouts to main layout
        self.main_grid.addWidget(self.contactImage_label,0,0)
        self.main_grid.addLayout(self.sub_grid,0,1)
        self.main_grid.addWidget(self.ok_button,1,0)
        self.main_grid.addWidget(self.cancel_button,1,1,Qt.AlignRight)
        
        #create a widget to display the main layout
        self.view_phonebookAdd_widget = QWidget()
        self.view_phonebookAdd_widget.setLayout(self.main_grid)
        self.view_phonebookAdd_widget.setFixedWidth(430)
        self.view_phonebookAdd_widget.setFixedHeight(280)
        
        #Message to display on status bar
        self.statusBar_msg.setText('Enter <i>First Name</i> OR <i>Last Name</i> AND <i>Phone Number</i>')
        self.statusBar().addWidget(self.statusBar_msg)


        #connections
        self.ok_button.clicked.connect(self.task_add_phonebook)
        self.cancel_button.clicked.connect(self.task_cancel_phonebook)
    
    
    def create_view_phonebookDelete_layout(self):
        #this is the second layout of the window - add the new contact

        self.keyWord_label = QLabel("Key word")

        self.keyWord_line_edit = QLineEdit()

        self.search_button = QPushButton("Search")
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")
        self.search_button.setFixedWidth(100)
        self.delete_button.setFixedWidth(100)
        self.cancel_button.setFixedWidth(100)
        
        self.search_table = QTableWidget()
        self.search_table.setRowCount(0)
        self.search_table.setColumnCount(0)
        
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        #add label and line edit widgets to the search layout
        self.hbox1.addWidget(self.keyWord_label)
        self.hbox1.addWidget(self.keyWord_line_edit)
        self.hbox2.addWidget(self.search_button)
        self.hbox2.addWidget(self.delete_button)
        self.hbox2.addWidget(self.cancel_button)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.hbox1)
        self.main_layout.addLayout(self.hbox2)
        self.main_layout.addWidget(self.search_table)
        
        #create a widget to display the main layout
        self.view_phonebookDelete_widget = QWidget()
        self.view_phonebookDelete_widget.setLayout(self.main_layout)
        self.view_phonebookDelete_widget.setFixedWidth(300)
        self.view_phonebookDelete_widget.setFixedHeight(300)
        
        #Message to display on status bar
        self.statusBar_msg.setText('Enter <i>First Name</i> OR <i>Last Name</i> OR <i>Phone Number</i>')
        self.statusBar().addWidget(self.statusBar_msg)


        #connections
        self.search_button.clicked.connect(self.task_search_phonebook)
        self.delete_button.clicked.connect(self.task_delete_phonebook)
        self.cancel_button.clicked.connect(self.task_cancel_phonebook)
        self.search_table.cellClicked.connect(self.cell_Selected)



    def instantiate_phonebook(self):
        self.phonebookTask_type = self.phonebook_radio_buttons.selected_button() #get the radio that was pressed
        
        if self.phonebookTask_type == 1:
            self.create_view_phonebookSearch_layout() #create the view phonebook search layout
            self.stacked_layout.addWidget(self.view_phonebookSearch_widget) #add this to the stack
        
        elif self.phonebookTask_type == 2:
            self.create_view_phonebookShowall_layout()
            self.stacked_layout.addWidget(self.view_phonebookShowall_widget) #add this to the stack
        
        elif self.phonebookTask_type == 3:
            self.create_view_phonebookAdd_layout() #create the view phonebook task layout
            self.stacked_layout.addWidget(self.view_phonebookAdd_widget) #add this to the stack
        
        elif self.phonebookTask_type == 4:
            self.create_view_phonebookDelete_layout() #create the view phonebook task layout
            self.stacked_layout.addWidget(self.view_phonebookDelete_widget) #add this to the stack
        
        else : self.close()


        self.stacked_layout.setCurrentIndex(1) # change the visible layout in the task


    def task_search_phonebook(self):
#        self.dbmgr.search_phonebook(self.keyWord_line_edit.text())
        self.search_data = self.dbmgr.search_phonebook(self.keyWord_line_edit.text())
        self.search_table.setRowCount(len(self.search_data))
        self.search_table.setColumnCount(3)
        self.search_table.setHorizontalHeaderLabels(('First Name', 'Last Name', 'Phone Number'))
        
        row_count = 0
        column_count = 0
        for contact in self.search_data :
            for field in contact :
                self.search_table.setItem(row_count,column_count,QTableWidgetItem(str(field)))
                column_count=column_count+1
            column_count = 0
            row_count = row_count+1

        if (self.phonebookTask_type==4 and self.keyWord_line_edit.text()!=''):
            #Message to display on status bar
            self.statusBar_msg.setText('Select any <b>ONE</b> row')
            self.statusBar().addWidget(self.statusBar_msg)
    
    
    
    def task_delete_phonebook(self):
        if (self.keyWord_line_edit.text()==''):
            return
    
        if QMessageBox.question(self, 'Message', 'Are you sure you want to delete?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes :
            self.dbmgr.delete_phonebook(self.delete_firstName.text(),self.delete_secondName.text(),self.delete_phoneNumber.text())
            self.keyWord_line_edit.setText('')
    
    def cell_Selected(self, row, column):
        self.delete_firstName = self.search_table.item(row, 0)
        self.delete_secondName = self.search_table.item(row, 1)
        self.delete_phoneNumber = self.search_table.item(row, 2)
    

    def task_add_phonebook(self):
        self.msgBox = QMessageBox()
        
        #if any of the below condition is satisified, don't save and popup the error msg
        if ((self.firstName_line_edit.text()=='' and self.lastName_line_edit.text()=='') or self.phoneNumber_line_edit.text() == ''):
            self.msgBox.setText("Invalid Input!")
            self.msgBox.exec_()
            return
        self.dbmgr.add_phonebook(self.firstName_line_edit.text(),self.lastName_line_edit.text(),self.phoneNumber_line_edit.text())
        
        #Acknowledge for data added success
        self.msgBox.setText("Contact Saved!")
        self.msgBox.exec_()
        self.firstName_line_edit.setText('')
        self.lastName_line_edit.setText('')
        self.phoneNumber_line_edit.setText('')


    def task_cancel_phonebook(self):
        self.close()
#        self.stacked_layout.setCurrentIndex(0) # change the visible layout in the task


def main():
        phone_book = QApplication(sys.argv) #create new application
        phone_book_window = PhoneBook() #create new instance of main window
        phone_book_window.show() #make instance visible
#        phone_book_window.setFixedSize(phone_book_window.size())
        phone_book_window.raise_() #raise instance to top of window stack
        phone_book.exec() #monitor application for events

if __name__ == "__main__":
        main()



