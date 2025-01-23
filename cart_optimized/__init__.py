#Optimized code

import json
from typing import List
import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in data['contents']],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """
    Fetches the cart for a given username.

    Args:
        username (str): The username to fetch the cart for.

    Returns:
        List[Product]: A list of Product objects in the user's cart.
    """
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    try:
        # Parse and retrieve product data
        all_items = [
            products.get_product(item_id)
            for cart_detail in cart_details
            for item_id in json.loads(cart_detail['contents'])
        ]

        # Filter out any None results (e.g., if a product doesn't exist)
        return [item for item in all_items if item is not None]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error processing cart contents: {e}")
        return []


def add_to_cart(username: str, product_id: int) -> None:
    """
    Adds a product to the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The ID of the product to add.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Removes a product from the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The ID of the product to remove.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """
    Deletes the cart for a given username.

    Args:
        username (str): The username whose cart should be deleted.
    """
    dao.delete_cart(username)
