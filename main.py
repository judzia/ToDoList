import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QComboBox, QListWidget, QLineEdit, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush

import json




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")
        self.setFixedSize(700,850)
        self.setGeometry(600,100, 700, 850)

        self.task_list = QListWidget()  # Add task_list to the MainWindow object
        self.load_tasks()  # Load tasks on startup
        
        # Initialize status_selector here as part of the MainWindow class
        self.status_selector = QComboBox()
        self.status_selector.addItems(["To Do", "In Progress", "Done"])
        self.initUI()

        palette = QPalette()
        pixmap = QPixmap("images/background2.png")  
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)




    def initUI(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        task_list_layout = QVBoxLayout()
        button_layout = QHBoxLayout()  # Layout dla edit priority i edit status
        remove_button_layout = QVBoxLayout()  # Nowy layout tylko dla remove button


        
        # Widgets
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.setFont(QFont("Arial", 11))
        self.task_input.setStyleSheet("QLineEdit {"
            "padding: 5px;"
            "border: 2px solid #ccc;"
            "border-radius: 10px;"
            "}")

        self.priority_selector = QComboBox()
        self.priority_selector.addItems(["Low", "Medium", "High"])
        self.priority_selector.setFont(QFont("Arial", 11))
        self.priority_selector.setStyleSheet(
            "QComboBox {"
            "padding: 5px;"
            "border: 2px solid #ccc;"
            "border-radius: 10px;"
            "}"
        )

        # status_selector is initialized in the __init__ method, so it should be available here
        self.status_selector.setFont(QFont("Arial", 11))
        self.status_selector.setStyleSheet(
            "QComboBox {"
            "padding: 5px;"
            "border: 2px solid #ccc;"
            "border-radius: 10px;"
            "}"
        )


        add_button = QPushButton("Add Task")
        add_button.setFont(QFont("Arial", 11))
        add_button.setFixedSize(120, 40)
        add_button.setStyleSheet(
            "QPushButton {"
            "background-color: #007BFF;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #0056b3;"
            "}"
        )
        add_button.clicked.connect(self.add_task)

        self.task_list = QListWidget()
        self.task_list.setFont(QFont("Arial", 12))
        self.task_list.setStyleSheet(
            "QListWidget {"
            "background-color: #f9f9f9;"
            "border-radius: 15px;"
            "border: 2px solid #ccc;"
            "padding: 10px;"
            "max-height: 300px;"
            "}"
        )

        remove_button = QPushButton("Remove Selected Task")
        remove_button.setFont(QFont("Arial", 12))
        remove_button.setFixedSize(250, 40)
        remove_button.setStyleSheet(
            "QPushButton {"
            "background-color: #dc3545;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #a71d2a;"
            "}"
        )
        remove_button.clicked.connect(self.remove_task)

        edit_button = QPushButton("Edit Priority")
        edit_button.setFont(QFont("Arial", 12))
        edit_button.setFixedSize(250, 40)
        edit_button.setStyleSheet(
            "QPushButton {"
            "background-color: #28a745;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #218838;"
            "}"
        )
        edit_button.clicked.connect(self.edit_priority)
        
        edit_status_button = QPushButton("Edit Status")
        edit_status_button.setFont(QFont("Arial", 12))
        edit_status_button.setFixedSize(250, 40)
        edit_status_button.setStyleSheet(
            "QPushButton {"
            "background-color: #007BFF;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #0056b3;"
            "}")
        edit_status_button.clicked.connect(self.edit_status)
        


        # Assemble layouts
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.priority_selector)
        input_layout.addWidget(self.status_selector)  # Ensure this is added here
        input_layout.addWidget(add_button)

        tasks_label = QLabel("                 ˖⁺‧₊˚⊹♡ Your Tasks ♡⊹˚₊‧⁺˖")
        tasks_label.setFont(QFont("Georgia", 18))  # Bigger font size
        task_list_layout.addWidget(tasks_label)
        task_list_layout.addWidget(self.task_list)

        # Add Edit Priority and Edit Status buttons to the button layout
        button_layout.addWidget(edit_button)
        button_layout.addWidget(edit_status_button)

        # Add the Remove Task button to its own layout
        remove_button_layout.addWidget(remove_button)


        # Adjust positions
        main_layout.addLayout(input_layout)
        main_layout.addLayout(task_list_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(remove_button_layout)

        main_layout.setContentsMargins(20, 100, 20, 80)
        input_layout.setSpacing(20)
        task_list_layout.setContentsMargins(30,40,30,60)
        #task_list_layout.setSpacing(10)
        button_layout.setContentsMargins(0,10,0,0)
        remove_button_layout.setContentsMargins(200,20,0,0) #left, top, right bottom
        
        
        

        central_widget.setLayout(main_layout)


    def add_task(self):
        task = self.task_input.text().strip()
        priority = self.priority_selector.currentText()
        status = self.status_selector.currentText()
        if task:  # Check if the input is not empty            
            list_item = f"📝 {task} - Priority: {priority} - Status: {status}"
            self.task_list.addItem(list_item)
            self.save_tasks()  # Save tasks after adding
            self.task_input.clear()  # Clear the input field


    def remove_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))
        self.save_tasks()  # Save tasks after removal 


    def edit_priority(self):
        """Edit the priority of the selected task."""
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        task_details = item.text().rsplit(" - Priority: ", 1)
        if len(task_details) != 2:
            return

        task, current_priority_and_status = task_details
        current_priority = current_priority_and_status.split(" - Status: ")[0]  # Extract only the priority

        priorities = ["Low", "Medium", "High"]
        new_priority, ok = QInputDialog.getItem(
            self, "Edit Priority", "Select new priority:", priorities, priorities.index(current_priority), False)
        if ok:
            item.setText(f"{task} - Priority: {new_priority} - Status: {current_priority_and_status.split(' - Status: ')[1]}")
            self.save_tasks()  # Save tasks after edit

    def edit_status(self):
        """Edit the status of the selected task."""
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        task_details = item.text().rsplit(" - Priority: ", 1)
        if len(task_details) != 2:
            return

        task, priority_and_status = task_details
        current_status = priority_and_status.split(" - Status: ")[1]  # Extract current status

        statuses = ["To Do", "In Progress", "Done"]
        new_status, ok = QInputDialog.getItem(
            self, "Edit Status", "Select new status:", statuses, statuses.index(current_status), False)
        if ok:
            item.setText(f"{task} - Priority: {priority_and_status.split(' - Status: ')[0]} - Status: {new_status}")
            self.save_tasks()  # Save tasks after edit

        
    def save_tasks(self):
        tasks = []
        for index in range(self.task_list.count()):
            task_text = self.task_list.item(index).text()
            tasks.append(task_text)

        with open("tasks.json", "w") as file:
            json.dump(tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                for task in tasks:
                    self.task_list.addItem(task)
        except FileNotFoundError:
            pass  # No tasks file found, it's fine




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
