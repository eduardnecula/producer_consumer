"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import unittest

from threading import Lock, Semaphore


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
        """

        self.queue_size_per_producer = queue_size_per_producer
        # lista in care voi pune
        self.market_list = []

        # semafor gol
        self.semaphore_empty = Semaphore(1)

        # pt id producatori
        self.id_producer = 0

        # lista cu numarul de produse pentru fiecare producator
        self.number_products_producers = []

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        pass
        """
        self.id_producer += 1
        return self.id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        can_publish = False

        # cate un producator adauga in lista de produse

        # produsul este format din {id_producator si nume_produs}
        product_published = {producer_id: product}

        # verific cate produse are producatorul in cos
        products = self.number_products_producers[producer_id - 1]
        if products[producer_id] < self.queue_size_per_producer:
            can_publish = True
            products[producer_id] += 1

        # produsul este adaugat
        if can_publish:
            self.market_list.append(product_published)

        # se elibereaza lista pentru a se scrie in ea de urmatorul producator

        return can_publish

    def add_to_cart(self, product):
        """
        Adds a product to the given cart. The method returns

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        find_drink = False
        lock = Lock()
        with lock:

            product_string = str(product)

            for i in self.market_list:
                if str(i).find(product_string) != -1:
                    # scade din lista vanzatorului
                    for j in i.keys():
                        cheia = j
                        dictionar = self.number_products_producers[cheia - 1]
                        dictionar[cheia] -= 1
                    find_drink = True
                    self.market_list.remove(i)

        return find_drink

    def remove_from_cart(self, product):
        """
        Removes a product from cart.

        :type product: Product
        :param product: the product to remove from cart
        """

        lock = Lock()

        product_published = {1: product}
        product = self.number_products_producers[0]

        with lock:
            product[1] += 1

        if product[1] <= self.queue_size_per_producer:
            self.market_list.append(product_published)
            return True

        return False


class TestMarketplace(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
