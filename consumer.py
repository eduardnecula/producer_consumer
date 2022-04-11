"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread


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

        carts_type = {}
        # trec prin fiecare cart
        for i in carts:
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
                                break
                else:
                    # adaug produsul in lista de la marketplace
                    for k in range(quantity):
                        while True:
                            remove_cart = self.marketplace.remove_from_cart(0, product_type)
                            if remove_cart:
                                break
                    pass

        pass

    def run(self):

        pass
