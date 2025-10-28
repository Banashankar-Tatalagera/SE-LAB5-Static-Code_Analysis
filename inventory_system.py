"""
Inventory Management System

This module provides functionality to manage an inventory system with
operations for adding, removing, and checking stock levels of items.
It includes features for data persistence through JSON files and low
stock monitoring.
"""

import json
from datetime import datetime


class InventoryManager:
    """Class to manage inventory operations."""

    def __init__(self):
        """Initialize an empty inventory."""
        self.stock_data = {}

    def add_item(self, item="default", qty=0, logs=None):
        """
        Add or update an item's quantity in the inventory.

        Args:
            item: The name/identifier of the item to add
            qty: The quantity to add (can be negative)
            logs: Optional list to track operations
        """
        if not item:
            return
        if logs is None:
            logs = []
        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        logs.append(f"{datetime.now()}: Added {qty} of {item}")

    def remove_item(self, item, qty):
        """
        Remove a specified quantity of an item from inventory.

        Args:
            item: The name/identifier of the item to remove
            qty: The quantity to remove
        """
        try:
            self.stock_data[item] -= qty
            if self.stock_data[item] <= 0:
                del self.stock_data[item]
        except KeyError:
            # Item not found in stock
            pass

    def get_qty(self, item):
        """
        Get the current quantity of an item in stock.

        Args:
            item: The name/identifier of the item to check

        Returns:
            int: The current quantity in stock
        """
        return self.stock_data[item]

    def load_data(self, file="inventory.json"):
        """
        Load inventory data from a JSON file.

        Args:
            file: Path to the JSON file to load
        """
        with open(file, "r", encoding="utf-8") as f:
            self.stock_data = json.loads(f.read())

    def save_data(self, file="inventory.json"):
        """
        Save current inventory data to a JSON file.

        Args:
            file: Path to the JSON file to save
        """
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.stock_data))

    def print_data(self):
        """Print a report of all items and their quantities in stock."""
        print("Items Report")
        for item, qty in self.stock_data.items():
            print(f"{item} -> {qty}")

    def check_low_items(self, threshold=5):
        """
        Check for items with quantity below the specified threshold.

        Args:
            threshold: Minimum quantity threshold (default: 5)

        Returns:
            list: Items with quantity below threshold
        """
        return [item for item, qty in self.stock_data.items()
                if qty < threshold]


def main():
    """Main function to demonstrate the inventory system functionality."""
    inventory = InventoryManager()

    inventory.add_item("apple", 10)
    inventory.add_item("banana", -2)
    inventory.add_item(123, "ten")  # invalid types, no check
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1)
    print("Apple stock:", inventory.get_qty("apple"))
    print("Low items:", inventory.check_low_items())
    inventory.save_data()
    inventory.load_data()
    inventory.print_data()
    print("eval used")  # removed dangerous eval() call


if __name__ == "__main__":
    main()
