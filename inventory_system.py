"""Inventory system module for static code analysis lab.

Provides simple functions to add/remove items and persist inventory.
This version is cleaned to satisfy common static analysis checks
(pylint, flake8, bandit) used in the lab.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logger for the module
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Inventory storage: map item name -> integer quantity
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """Add a given quantity of an item to the stock_data dictionary.

    Args:
        item: name of the item to add.
        qty: integer quantity to add (can be negative to reduce).
        logs: optional list to append an operation message to.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str):
        raise TypeError("item must be a string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an integer")

    if qty == 0:
        logger.debug("add_item called with qty=0; no change made")
        return

    previous = stock_data.get(item, 0)
    stock_data[item] = previous + qty
    entry = f"{datetime.utcnow().isoformat()}Z: Added {qty} of {item} (prev={previous}, now={stock_data[item]})"
    logs.append(entry)
    logger.info(entry)


def remove_item(item: str, qty: int) -> None:
    """Remove a specified quantity of an item from the stock_data dictionary.

    Raises:
        KeyError: if the item does not exist in inventory.
        TypeError: if arguments are of wrong type.
    """
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an integer")

    if item not in stock_data:
        raise KeyError(f"Item '{item}' not found in inventory")

    new_qty = stock_data[item] - qty
    if new_qty > 0:
        stock_data[item] = new_qty
        logger.info(f"Removed {qty} of {item}; new qty={new_qty}")
    else:
        # remove the item entirely if qty <= 0
        del stock_data[item]
        logger.info(f"Item '{item}' removed from inventory (qty <= 0 after removal)")


def get_qty(item: str) -> int:
    """Return the quantity of the specified item.

    Raises:
        KeyError: if item not found.
        TypeError: if item name is not a string.
    """
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    return stock_data[item]


def load_data(file_path: str = "inventory.json") -> None:
    """Load stock data from a JSON file into the in-memory inventory.

    The function updates the existing `stock_data` dict (no global rebind).
    Non-integer quantities are coerced to int when possible, otherwise set to 0.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.warning("File %s not found; starting with empty inventory", file_path)
        return
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Failed to load inventory from %s: %s", file_path, exc)
        return

    cleaned: Dict[str, int] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            if not isinstance(k, str):
                logger.warning("Skipping non-string key in inventory: %r", k)
                continue
            try:
                cleaned[k] = int(v)
            except (TypeError, ValueError):
                logger.warning("Non-integer qty for %s; setting to 0", k)
                cleaned[k] = 0
    else:
        logger.warning("Inventory file %s did not contain a JSON object; skipping load", file_path)
        return

    # Update existing dict instead of reassigning global variable
    stock_data.clear()
    stock_data.update(cleaned)
    logger.info("Loaded inventory from %s", file_path)


def save_data(file_path: str = "inventory.json") -> None:
    """Save current stock_data to a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2, sort_keys=True)
        logger.info("Saved inventory to %s", file_path)
    except OSError as exc:
        logger.error("Failed to save inventory to %s: %s", file_path, exc)


def print_data() -> None:
    """Print all inventory items and quantities in sorted order."""
    print("Items Report")
    for name, qty in sorted(stock_data.items()):
        print(f"{name} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items whose quantity is below the threshold."""
    if not isinstance(threshold, int):
        raise TypeError("threshold must be an integer")
    return [name for name, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Small demo run (non-destructive)."""
    # seed some data safely
    add_item("apple", 10)
    # demonstrate removal with validation
    try:
        remove_item("apple", 3)
    except KeyError:
        logger.exception("Tried to remove non-existent item")

    try:
        print("Apple stock:", get_qty("apple"))
    except KeyError:
        print("Apple not found")

    print("Low items:", check_low_items())

    # Save and load to demonstrate persistence
    save_data()
    load_data()

    print_data()


if __name__ == "__main__":
    main()
