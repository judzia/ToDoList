import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QComboBox, QListWidget, QLineEdit, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import json




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To Do List")
        self.setFixedSize(700,850)
        self.setGeometry(600,100, 700, 850)

        self.task_list = QListWidget()  
        self.load_tasks()  
        
        
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
            "background-color: #f09ecb;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #c272bd;"
            "}"
        )
        add_button.clicked.connect(self.add_task)

        #self.task_list = QListWidget()
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
            "background-color: #8d2ac7;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #7c21b0;"
            "}"
        )
        remove_button.clicked.connect(self.remove_task)

        edit_button = QPushButton("Edit Priority")
        edit_button.setFont(QFont("Arial", 12))
        edit_button.setFixedSize(250, 40)
        edit_button.setStyleSheet(
            "QPushButton {"
            "background-color: #eb86ce;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #c76fae;"
            "}"
        )
        edit_button.clicked.connect(self.edit_priority)
        
        edit_status_button = QPushButton("Edit Status")
        edit_status_button.setFont(QFont("Arial", 12))
        edit_status_button.setFixedSize(250, 40)
        edit_status_button.setStyleSheet(
            "QPushButton {"
            "background-color: #ad8ef5;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #c575c9;"
            "}")
        edit_status_button.clicked.connect(self.edit_status)
        


        # Assemble layouts
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.priority_selector)
        input_layout.addWidget(self.status_selector) 
        input_layout.addWidget(add_button)

        tasks_label = QLabel("               ˖⁺‧₊˚⊹♡ 𝗬𝗼𝘂𝗿 𝗧𝗮𝘀𝗸𝘀 ♡⊹˚₊‧⁺˖")
        tasks_label.setFont(QFont("Arial", 18))  
        task_list_layout.addWidget(tasks_label)
        task_list_layout.addWidget(self.task_list)
       
        button_layout.addWidget(edit_button)
        button_layout.addWidget(edit_status_button)

        remove_button_layout.addWidget(remove_button)

        # Adjusting positions
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
            self.task_input.clear()  # Clear the input field
            self.update_json()


    def remove_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))
        self.update_json()


    def edit_priority(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        task_details = item.text().split(" - ")
        if len(task_details) < 3:
            return

        task, current_priority,status = task_details[0], task_details[1].replace("Priority: ", ""), task_details[2].replace("Status: ", "")

        priorities = ["Low", "Medium", "High"]
        new_priority, ok = QInputDialog.getItem(
            self, "Edit Priority", "Select new priority:", priorities, priorities.index(current_priority), False)
        if ok:
            item.setText(f"{task} - Priority: {new_priority} - Status: {status}")
            self.update_json()


    def edit_status(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        task_details = item.text().split(" - ")
        if len(task_details) != 3:
            return

        task, priority, current_status = task_details[0], task_details[1].replace("Priority: ", ""), task_details[2].replace("Status: ", "")

        statuses = ["To Do", "In Progress", "Done"]
        new_status, ok = QInputDialog.getItem(
            self, "Edit Status", "Select new status:", statuses, statuses.index(current_status), False)
        if ok:
            item.setText(f"{task} - Priority: {priority} - Status: {new_status}")
            self.update_json()

        
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                for task in tasks:
                    task_text = f"{task['task']} - Priority: {task['priority']} - Status: {task['status']}"
                    self.task_list.addItem(task_text)
        except (FileNotFoundError, json.JSONDecodeError):
            pass


    def update_json(self):
        tasks = []
        for index in range(self.task_list.count()):
            item = self.task_list.item(index).text()
            task_details = item.split(" - ")
            if len(task_details) == 3:
                task = task_details[0]
                priority = task_details[1].replace("Priority: ", "")
                status = task_details[2].replace("Status: ", "")
                tasks.append({"task": task, "priority": priority, "status": status})

        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
