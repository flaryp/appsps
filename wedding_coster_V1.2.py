import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton, QMessageBox

basic_services_prices = {
    'Cinematography': 8000,
    'Traditional Photo': 5000,
    'Traditional Video': 6000,
    'Candid Photography': 8000
}

additional_services_prices = {
    'Video Editing': 5000,
    'Cinematography Editing': 10000
}

optional_services_prices = {
    'Album': 7000,
    'Travel': 3000
}

# Function to calculate total cost for basic services
def calculate_basic_services_cost(days, selected_services):
    total_basic_cost = 0
    for service in selected_services:
        total_basic_cost += basic_services_prices[service] * days
        # Include additional service cost if corresponding basic service is selected
        if service == 'Cinematography':
            total_basic_cost += additional_services_prices['Cinematography Editing']
        elif service == 'Traditional Video':
            total_basic_cost += additional_services_prices['Video Editing']
    return total_basic_cost

# Function to calculate total cost including additional services and percentage increase
def calculate_total_cost(days, selected_services, percentage):
    total_basic_cost = calculate_basic_services_cost(days, selected_services)
    additional_services_cost = sum(additional_services_prices[service] for service in selected_services if service in additional_services_prices)
    total_cost_before_percentage = total_basic_cost + additional_services_cost
    total_cost = total_cost_before_percentage * (1 + percentage / 100)
    return total_cost

# Function to calculate total cost for optional services
def calculate_optional_services_cost():
    total_optional_cost = sum(optional_services_prices.values())
    return total_optional_cost

class WeddingCostCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create layout
        layout = QVBoxLayout()

        # Create checkbox for basic services
        self.service_checkboxes = {}
        for service in basic_services_prices.keys():
            checkbox = QCheckBox(service)
            layout.addWidget(checkbox)
            self.service_checkboxes[service] = checkbox

        # Create input for number of days
        self.days_label = QLabel("Number of days:")
        layout.addWidget(self.days_label)
        self.days_input = QLineEdit()
        layout.addWidget(self.days_input)

        # Create input for percentage increase
        self.percentage_label = QLabel("Percentage increase:")
        layout.addWidget(self.percentage_label)
        self.percentage_input = QLineEdit()
        layout.addWidget(self.percentage_input)

        # Create calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # Create label to display result
        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        try:
            # Get user inputs
            days = int(self.days_input.text())
            percentage = float(self.percentage_input.text())

            # Get selected services
            selected_services = [service for service, checkbox in self.service_checkboxes.items() if checkbox.isChecked()]

            # Calculate total cost
            total_cost = calculate_total_cost(days, selected_services, percentage)
            total_optional_cost = calculate_optional_services_cost()

            # Display result
            self.result_label.setText(f"Total cost for the selected services for {days} days with {percentage}% increase is: ₹{total_cost:.2f}\nTotal cost for optional services is: ₹{total_optional_cost+total_cost:.2f}")

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid input.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeddingCostCalculator()
    window.setWindowTitle("Wedding Cost Calculator")
    window.show()
    sys.exit(app.exec_())
