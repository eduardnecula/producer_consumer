"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread, Lock


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        pass
        """
        """
        print()
        print("Consumer:")
        print("carts: ", carts)
        print("market: ", marketplace)
        print("retry: ", retry_wait_time)
        print("kwargs: ", kwargs)
        print()
        """

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

        # lista de cumparaturi
        self.shopping_list = []

        carts_type = {}
        # trec prin fiecare cart

        pass

    def run(self):
        my_lock = Lock()
        lock_print = Lock()

        for i in self.carts:
            # in caz ca sunt mai multe carucioare in caracioare
            for j in i:
                carts_type = j
                action_type = carts_type['type']
                product_type = carts_type['product']
                quantity = carts_type['quantity']
                if action_type == 'add':
                    # adaug in cos daca gasesc produsul in lista
                    # se adauga de quantity ori
                    for k in range(quantity):
                        while True:
                            add_cart = self.marketplace.add_to_cart(0, product_type)
                            if add_cart:
                                name_consumer = self.kwargs['name']
                                # print(name_consumer, " bought ", product_type)
                                to_append = str(name_consumer) + " bought " + str(product_type)
                                with my_lock:
                                    self.shopping_list.append(to_append)
                                break
                            time.sleep(self.retry_wait_time)
                else:
                    # adaug produsul in lista de la marketplace
                    for k in range(quantity):
                        with my_lock:
                            while True:
                                remove_cart = self.marketplace.remove_from_cart(0, product_type)
                                if remove_cart:
                                    name_consumer = self.kwargs['name']
                                    to_append = str(name_consumer) + " bought " + str(product_type)
                                    self.shopping_list.remove(to_append)
                                    break
                            time.sleep(self.retry_wait_time)

        with lock_print:
            for i in self.shopping_list:
                print(i)
