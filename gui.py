import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QSpinBox, QLineEdit, QComboBox, QDialog, QMessageBox, QTextEdit,
    QGroupBox, QGridLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt as QtCore
import json
from bankers_algorithm import BankersAlgorithm, AllocationStatus


class ResourceAllocationDialog(QDialog):
    """Dialog for adding/modifying resource allocation"""
    
    def __init__(self, parent=None, resources=None, process_id=None):
        super().__init__(parent)
        self.resources = resources or {}
        self.process_id = process_id
        self.result = {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Resource Allocation - Process {self.process_id}")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Create input fields for each resource
        self.resource_inputs = {}
        grid = QGridLayout()
        
        for i, resource in enumerate(self.resources.keys()):
            label = QLabel(f"{resource}:")
            spinbox = QSpinBox()
            spinbox.setMaximum(1000)
            spinbox.setValue(0)
            
            self.resource_inputs[resource] = spinbox
            grid.addWidget(label, i, 0)
            grid.addWidget(spinbox, i, 1)
        
        layout.addLayout(grid)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_result(self):
        return {res: self.resource_inputs[res].value() for res in self.resources}


class BankersVisualizerGUI(QMainWindow):
    """Main GUI for Banker's Algorithm Visualizer"""
    
    def __init__(self):
        super().__init__()
        self.banker = None
        self.resources = {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Banker's Algorithm Visualizer - Safe State Explorer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left panel - System Setup
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel - Tabs
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        central_widget.setLayout(main_layout)
        self.show()
    
    def create_left_panel(self):
        """Create left panel for system setup"""
        group = QGroupBox("System Configuration")
        layout = QVBoxLayout()
        
        # Resource setup
        res_group = QGroupBox("Resources")
        res_layout = QVBoxLayout()
        
        self.resource_inputs = {}
        for res_name in ['CPU', 'Memory', 'Disk', 'Network']:
            h_layout = QHBoxLayout()
            label = QLabel(f"{res_name}:")
            spinbox = QSpinBox()
            spinbox.setMaximum(100)
            spinbox.setValue(10)
            self.resource_inputs[res_name] = spinbox
            h_layout.addWidget(label)
            h_layout.addWidget(spinbox)
            res_layout.addLayout(h_layout)
        
        res_group.setLayout(res_layout)
        layout.addWidget(res_group)
        
        # Initialize button
        init_btn = QPushButton("Initialize System")
        init_btn.clicked.connect(self.initialize_system)
        layout.addWidget(init_btn)
        
        # Process management
        proc_group = QGroupBox("Process Management")
        proc_layout = QVBoxLayout()
        
        pid_layout = QHBoxLayout()
        pid_layout.addWidget(QLabel("Process ID:"))
        self.pid_input = QSpinBox()
        self.pid_input.setMaximum(100)
        self.pid_input.setValue(1)
        pid_layout.addWidget(self.pid_input)
        proc_layout.addLayout(pid_layout)
        
        add_proc_btn = QPushButton("Add Process")
        add_proc_btn.clicked.connect(self.add_process_dialog)
        proc_layout.addWidget(add_proc_btn)
        
        remove_proc_btn = QPushButton("Remove Process")
        remove_proc_btn.clicked.connect(self.remove_process)
        proc_layout.addWidget(remove_proc_btn)
        
        proc_group.setLayout(proc_layout)
        layout.addWidget(proc_group)
        
        # Request resources
        req_group = QGroupBox("Resource Request")
        req_layout = QVBoxLayout()
        
        req_layout.addWidget(QLabel("Request resources for selected process:"))
        
        request_btn = QPushButton("Request Resources")
        request_btn.clicked.connect(self.request_resources_dialog)
        req_layout.addWidget(request_btn)
        
        release_btn = QPushButton("Release All Resources")
        release_btn.clicked.connect(self.release_all_resources)
        req_layout.addWidget(release_btn)
        
        req_group.setLayout(req_layout)
        layout.addWidget(req_group)
        
        # What-if explorer
        whatif_group = QGroupBox("What-If Explorer")
        whatif_layout = QVBoxLayout()
        
        whatif_layout.addWidget(QLabel("Test hypothetical requests:"))
        
        explore_btn = QPushButton("Explore Request")
        explore_btn.clicked.connect(self.explore_what_if_dialog)
        whatif_layout.addWidget(explore_btn)
        
        whatif_group.setLayout(whatif_layout)
        layout.addWidget(whatif_group)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def create_right_panel(self):
        """Create right panel with tabs"""
        tabs = QTabWidget()
        
        # System State tab
        self.state_table = QTableWidget()
        self.state_table.setColumnCount(5)
        self.state_table.setHorizontalHeaderLabels(["PID", "Max Claim", "Allocated", "Needed", "Status"])
        tabs.addTab(self.state_table, "System State")
        
        # Resource Allocation Graph tab
        self.graph_view = QChartView()
        self.graph_view.setRenderHint(self.graph_view.Antialiasing)
        tabs.addTab(self.graph_view, "Resource Graph")
        
        # Safe Sequence tab
        self.safe_seq_text = QTextEdit()
        self.safe_seq_text.setReadOnly(True)
        tabs.addTab(self.safe_seq_text, "Safe Sequence")
        
        # History tab
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Action", "Process ID", "Details", "Result"])
        tabs.addTab(self.history_table, "History")
        
        return tabs
    
    def initialize_system(self):
        """Initialize the Banker's Algorithm system"""
        resources = {
            name: spinbox.value() 
            for name, spinbox in self.resource_inputs.items()
        }
        
        if all(v > 0 for v in resources.values()):
            self.banker = BankersAlgorithm(resources)
            self.resources = resources
            QMessageBox.information(self, "Success", "System initialized successfully!")
            self.update_display()
        else:
            QMessageBox.warning(self, "Error", "All resources must be > 0")
    
    def add_process_dialog(self):
        """Show dialog to add a new process"""
        if not self.banker:
            QMessageBox.warning(self, "Error", "Initialize system first!")
            return
        
        pid = self.pid_input.value()
        
        # Create dialog for max claim
        dialog = ResourceAllocationDialog(self, self.resources, pid)
        if dialog.exec_() == QDialog.Accepted:
            max_claim = dialog.get_result()
            try:
                self.banker.add_process(pid, max_claim)
                QMessageBox.information(self, "Success", f"Process {pid} added!")
                self.update_display()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
    
    def remove_process(self):
        """Remove selected process"""
        if not self.banker:
            QMessageBox.warning(self, "Error", "Initialize system first!")
            return
        
        pid = self.pid_input.value()
        try:
            self.banker.remove_process(pid)
            QMessageBox.information(self, "Success", f"Process {pid} removed!")
            self.update_display()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def request_resources_dialog(self):
        """Show dialog to request resources"""
        if not self.banker:
            QMessageBox.warning(self, "Error", "Initialize system first!")
            return
        
        pid = self.pid_input.value()
        dialog = ResourceAllocationDialog(self, self.resources, pid)
        
        if dialog.exec_() == QDialog.Accepted:
            request = dialog.get_result()
            status, message = self.banker.request_resources(pid, request)
            
            color = "green" if status == AllocationStatus.GRANTED else "red"
            QMessageBox.information(
                self, 
                f"Request {status.value}",
                f"<b style='color:{color}'>{message}</b>"
            )
            self.update_display()
    
    def release_all_resources(self):
        """Release all resources for selected process"""
        if not self.banker:
            QMessageBox.warning(self, "Error", "Initialize system first!")
            return
        
        pid = self.pid_input.value()
        if self.banker.release_resources(pid):
            QMessageBox.information(self, "Success", f"Resources released for Process {pid}")
            self.update_display()
        else:
            QMessageBox.warning(self, "Error", f"Process {pid} not found")
    
    def explore_what_if_dialog(self):
        """Explore what-if scenarios"""
        if not self.banker:
            QMessageBox.warning(self, "Error", "Initialize system first!")
            return
        
        pid = self.pid_input.value()
        dialog = ResourceAllocationDialog(self, self.resources, pid)
        
        if dialog.exec_() == QDialog.Accepted:
            request = dialog.get_result()
            result = self.banker.explore_what_if(pid, request)
            
            feasible = result['feasible']
            message = result['message']
            safe_seq = result['safe_sequence']
            
            color = "green" if feasible else "red"
            details = f"<b style='color:{color}'>{message}</b><br><br>"
            
            if safe_seq:
                details += f"<b>Safe Sequence:</b> {' → '.join(map(str, safe_seq))}"
            
            QMessageBox.information(self, "What-If Analysis", details)
    
    def update_display(self):
        """Update all display elements"""
        if not self.banker:
            return
        
        state = self.banker.get_system_state()
        
        # Update system state table
        self.state_table.setRowCount(0)
        for pid, proc_info in state['processes'].items():
            row = self.state_table.rowCount()
            self.state_table.insertRow(row)
            
            self.state_table.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.state_table.setItem(row, 1, QTableWidgetItem(str(proc_info['max_claim'])))
            self.state_table.setItem(row, 2, QTableWidgetItem(str(proc_info['allocated'])))
            self.state_table.setItem(row, 3, QTableWidgetItem(str(proc_info['needed'])))
            
            status = "✓ Safe" if state['is_safe'] else "✗ Unsafe"
            self.state_table.setItem(row, 4, QTableWidgetItem(status))
        
        # Update safe sequence
        safe_seq = state['safe_sequence']
        if safe_seq:
            seq_text = " → ".join(map(str, safe_seq))
            self.safe_seq_text.setText(f"Safe Sequence: {seq_text}\n\nSystem is SAFE ✓")
        else:
            self.safe_seq_text.setText("No safe sequence found.\nSystem is UNSAFE ✗")
        
        # Update resource graph
        self.update_resource_graph(state)
    
    def update_resource_graph(self, state):
        """Update resource allocation graph"""
        chart = QChart()
        chart.setTitle("Resource Allocation Overview")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Create bar sets for each resource
        resources = list(state['total_resources'].keys())
        
        available_set = QBarSet("Available")
        allocated_set = QBarSet("Allocated")
        
        for resource in resources:
            available = state['available'].get(resource, 0)
            total = state['total_resources'].get(resource, 0)
            allocated = total - available
            
            available_set.append(available)
            allocated_set.append(allocated)
        
        available_set.setColor(QColor(52, 211, 153))
        allocated_set.setColor(QColor(239, 68, 68))
        
        series = QBarSeries()
        series.append(available_set)
        series.append(allocated_set)
        
        chart.addSeries(series)
        
        # Axes
        axis_x = QBarCategoryAxis()
        axis_x.append(resources)
        chart.addAxis(axis_x, QtCore.Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        chart.addAxis(axis_y, QtCore.Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        self.graph_view.setChart(chart)


def main():
    app = QApplication(sys.argv)
    gui = BankersVisualizerGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
