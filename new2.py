# ---------------------------------
# POS Transaction Tracker Bot (CSV Version)
# ---------------------------------
import csv
from datetime import datetime

class POSTrackerBot:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    # Load transactions from CSV
    def load_transactions(self):
        try:
            with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.transactions = [row for row in reader]
            print(f"📂 Loaded {len(self.transactions)} transactions from '{self.filename}'.")
        except FileNotFoundError:
            print("⚠️ No existing transaction file found. Starting fresh.")
            self.transactions = []

    # Save transactions to CSV
    def save_transactions(self):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["item", "quantity", "price", "total", "time"])
            writer.writeheader()
            writer.writerows(self.transactions)
        print("💾 Transactions saved to file.")

    # Add new transaction
    def add_transaction(self):
        print("\n--- Add New Transaction ---")
        item_name = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per item: "))
        total = quantity * price
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        transaction = {
            "item": item_name,
            "quantity": str(quantity),
            "price": str(price),
            "total": str(total),
            "time": time
        }

        self.transactions.append(transaction)
        self.save_transactions()
        print(f"✅ Transaction for '{item_name}' added successfully!")

    # View transactions
    def view_transactions(self):
        print("\n--- Transaction History ---")
        if not self.transactions:
            print("No transactions recorded yet.")
            return

        for i, t in enumerate(self.transactions, start=1):
            print(f"{i}. {t['item']} - Qty: {t['quantity']} - "
                  f"Price: ₦{t['price']} - Total: ₦{t['total']} - "
                  f"Time: {t['time']}")

    # Calculate total sales
    def total_sales(self):
        print("\n--- Total Sales ---")
        total = sum(float(t["total"]) for t in self.transactions)
        print(f"💰 Total sales amount: ₦{total:.2f}")

    # Search for transactions by item name
    def search_transaction(self):
        print("\n--- Search Transaction ---")
        search_item = input("Enter item name to search: ").lower()
        found = [t for t in self.transactions if t["item"].lower() == search_item]

        if found:
            print(f"Found {len(found)} record(s) for '{search_item}':")
            for t in found:
                print(f"{t['item']} - Qty: {t['quantity']} - Total: ₦{t['total']} - Time: {t['time']}")
        else:
            print(f"No transactions found for '{search_item}'.")

    # Main menu loop
    def run(self):
        while True:
            print("\n====== POS TRANSACTION TRACKER BOT ======")
            print("1. Add Transaction")
            print("2. View Transactions")
            print("3. Total Sales")
            print("4. Search Transaction")
            print("5. Exit")
            choice = input("Choose an option (1-5): ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.total_sales()
            elif choice == "4":
                self.search_transaction()
            elif choice == "5":
                print("👋 Exiting")
# Run the bot
if __name__ == "__main__":
    bot = POSTrackerBot()
    bot.run()
