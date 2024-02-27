from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from collections import defaultdict

@dataclass
class OrderItem:
    """Order Item requested by a customer."""
    customer: str
    name: str
    quantity: int
    one_item_volume: int

    @property
    def total_volume(self) -> int:
        """Calculate and return total volume of all order items together."""
        return self.quantity * self.one_item_volume


@dataclass
class Order:
    """Combination of order items of one customer."""
    order_items: List[OrderItem]
    destination: str = None

    @property
    def total_quantity(self) -> int:
        """Calculate and return the sum of quantities of all items in the order."""
        return sum(item.quantity for item in self.order_items)

    @property
    def total_volume(self) -> int:
        """Calculate and return the total volume of all items in the order."""
        return sum(item.total_volume for item in self.order_items)


@dataclass
class Container:
    """Container to transport orders."""
    volume: int
    orders: List[Order] = field(default_factory=list)

    @property
    def volume_left(self) -> int:
        """Return the remaining volume in the container."""
        return self.volume - sum(order.total_volume for order in self.orders)


class OrderAggregator:
    """Algorithm of aggregating orders."""
    
    def __init__(self):
        """Initialize order aggregator."""
        self.order_items = []

    def add_item(self, item: OrderItem):
        """
        Add order item to the aggregator.

        :param item: Item to add.
        :return: None
        """
        self.order_items.append(item)

    def remove_items(self, items: List[OrderItem]):
        """
        Remove order items from the aggregator.

        :param items: List of items to remove.
        :return: None
        """
        for item in items:
            self.order_items.remove(item)

    def aggregate_order(self, customer: str, max_items_quantity: int, max_volume: int) -> Order:
        """
        Create an order for a customer containing order lines added by add_item method.

        Iterate over added orders items and add them to order if they are for the given customer
        and can fit into the order.

        :param customer: Customer's name to create an order for.
        :param max_items_quantity: Maximum amount of items in the order.
        :param max_volume: Maximum volume of the order. All item volumes must not exceed this value.
        :return: Order.
        """
        items = [item for item in self.order_items if item.customer == customer]
        total_quantity = sum(item.quantity for item in items)
        total_volume = sum(item.total_volume for item in items)

        if total_quantity <= max_items_quantity and total_volume <= max_volume:
            order = Order(items)
            self.remove_items(items)
            return order
        else:
            return None


class ContainerAggregator:
    """Algorithm to prepare containers."""

    def __init__(self, container_volume: int):
        """
        Initialize Container Aggregator.

        :param container_volume: Volume of each container created by this aggregator.
        """
        self.container_volume = container_volume
        self.not_used_orders: List[Order] = []

    def prepare_containers(self, orders: Tuple[Order]) -> Dict[str, List[Container]]:
        """
        Create containers and put orders into them.

        If an order cannot be put into a container, it is added to self.not_used_orders list.

        :param orders: tuple of orders.
        :return: dict where keys are destinations and values are lists of containers with orders.
        """
        containers: Dict[str, List[Container]] = defaultdict(list)

        for order in orders:
            placed = False
            for destination, container_list in containers.items():
                container = next((c for c in container_list if order.total_volume <= c.volume_left and order.destination == destination), None)
                if container:
                    container.orders.append(order)
                    placed = True
                    break

            if not placed:
                container = Container(self.container_volume)
                container.orders.append(order)
                containers[order.destination].append(container)

        return containers