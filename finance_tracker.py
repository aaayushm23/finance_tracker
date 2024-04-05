import json
import getpass
import os

class FinanceTracker:
    def __init__(self, username):
        self.username = username
        self.expenses = self.load_expenses()

    def load_expenses(self):
        filename = f"{self.username}_expenses.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

    def save_expenses(self):
        filename = f"{self.username}_expenses.json"
        with open(filename, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, category, amount, description):
        if category not in self.expenses:
            self.expenses[category] = []
        self.expenses[category].append({'amount': amount, 'description': description})
        self.save_expenses()

    def view_expenses(self):
        for category, expenses in self.expenses.items():
            print(f"Category: {category}")
            for idx, expense in enumerate(expenses):
                print(f"  {idx + 1}. Amount: ${expense['amount']}, Description: {expense['description']}")
    
    def get_total_expenses(self):
        total = 0
        for expenses in self.expenses.values():
            for expense in expenses:
                total += expense['amount']
        return total
    
    def get_expenses_by_category(self):
        category_totals = {category: sum(expense['amount'] for expense in expenses) for category, expenses in self.expenses.items()}
        return category_totals

    def edit_expense(self, category, expense_index, new_amount, new_description):
        if category in self.expenses and 0 <= expense_index < len(self.expenses[category]):
            self.expenses[category][expense_index] = {'amount': new_amount, 'description': new_description}
            self.save_expenses()
        else:
            print("Invalid category or expense index.")
    
    def delete_expense(self, category, expense_index):
        if category in self.expenses and 0 <= expense_index < len(self.expenses[category]):
            del self.expenses[category][expense_index]
            if not self.expenses[category]:
                del self.expenses[category]
            self.save_expenses()
        else:
            print("Invalid category or expense index.")
    
    def generate_report(self, period):
        # This is a simplified version. In a real application, you would parse dates and filter expenses accordingly.
        print(f"Generating {period} report...")
        self.view_expenses()

def authenticate_user():
    users = load_users()
    username = input("Username: ")
    if username in users:
        password = getpass.getpass("Password: ")
        if users[username] == password:
            print("Login successful.")
            return username
        else:
            print("Incorrect password.")
            return None
    else:
        print("User not found. Creating a new account.")
        password = getpass.getpass("Set a password: ")
        users[username] = password
        save_users(users)
        print("Account created.")
        return username

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open("users.json", 'w') as file:
        json.dump(users, file, indent=4)

def main():
    username = authenticate_user()
    if username:
        tracker = FinanceTracker(username)
        
        while True:
            print("\nPersonal Finance Tracker")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Get Total Expenses")
            print("4. Get Expenses by Category")
            print("5. Edit Expense")
            print("6. Delete Expense")
            print("7. Generate Report")
            print("8. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == '1':
                category = input("Enter category: ")
                amount = float(input("Enter amount: "))
                description = input("Enter description: ")
                tracker.add_expense(category, amount, description)
            elif choice == '2':
                tracker.view_expenses()
            elif choice == '3':
                total = tracker.get_total_expenses()
                print(f"Total Expenses: ${total}")
            elif choice == '4':
                category_totals = tracker.get_expenses_by_category()
                for category, total in category_totals.items():
                    print(f"Category: {category}, Total: ${total}")
            elif choice == '5':
                category = input("Enter category of the expense to edit: ")
                tracker.view_expenses()
                expense_index = int(input("Enter the expense index to edit: ")) - 1
                new_amount = float(input("Enter new amount: "))
                new_description = input("Enter new description: ")
                tracker.edit_expense(category, expense_index, new_amount, new_description)
            elif choice == '6':
                category = input("Enter category of the expense to delete: ")
                tracker.view_expenses()
                expense_index = int(input("Enter the expense index to delete: ")) - 1
                tracker.delete_expense(category, expense_index)
            elif choice == '7':
                period = input("Enter period (e.g., monthly, yearly): ")
                tracker.generate_report(period)
            elif choice == '8':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
