"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import unittest
from multiprocessing import Semaphore, Lock

from producer import Producer

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        pass
        """
        """
        print()
        print("market:")
        print("queus_size: ", queue_size_per_producer)
        print()
         """
        self.queue_size_per_producer = queue_size_per_producer
        # lista in care voi pune
        self.market_list = []

        # semafor gol
        self.semaphore_empty = Semaphore(4)

        # semafor plin
        self.semaphore_full = Semaphore(0)

        # nr de produse in market
        self.number_products = 0
        pass

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        pass
        """
        pass

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.semaphore_empty.acquire()
        self.market_list.append(product)
        # print(self.market_list)
        self.semaphore_full.release()

        pass

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        pass

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        my_lock = Lock()

        self.semaphore_full.acquire()
        print("caut sa vad daca gasesc: ", product)

        print(self.market_list)
        with my_lock:
            self.number_products -= 1
            #print("iau din market")

        self.semaphore_empty.release()

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        print("(sterg) incerc sa adaug in marketPlace: ", product)
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass


class TestMarketplace(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')