"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread, Lock
from product import Product, Coffee, Tea
# pentru split pe un string
import re
# pentru sleep
import time
"""
Primeste o linie dintr-o lista de produse,
si intorce o lista cu fiecare camp din ea:
(Tea(name='Linden', price=9, type='Herbal'), 2, 0.18)
Va intoarce lista cuprinsa din urmatoarele elemente:
(Tea(name='Linden', price=9, type='Herbal')
2
0.18
"""


def decompose(product):
    # lista in care se va scrie
    list_product = []
    # produsul de convertit element cu element in lista
    convstring = str(product)
    splitstring = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', convstring)
    # numele produsului
    productname = splitstring.pop(0)
    # numarul de produse de produs
    numberproducts = splitstring.pop(1)
    # timpul de producere al unui produs
    waittime = splitstring.pop(1)

    # convertire elemente lista, la tipul lor nativ, din string in int/float
    stringnumberproducts = str(numberproducts)
    stringnumberproducts = stringnumberproducts[0:len(numberproducts) - 1]

    stringwaittime = str(waittime)
    stringwaittime = stringwaittime[0:len(stringwaittime) - 1]

    intnumberproducts = int(stringnumberproducts)
    floatwaittime = float(stringwaittime)

    # adaugare in lista
    list_product.append(productname)
    list_product.append(intnumberproducts)
    list_product.append(floatwaittime)

    return list_product


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        pass
        """

        """
        print()
        print("producer:")
        print("products: ", products)
        print("market: ", marketplace)
        print("republish wait time: ", republish_wait_time)
        print("kwargs: ", kwargs)
        print()
        """

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

        pass

    def run(self):
        my_lock = Lock()
        while True:
            if self.marketplace.number_products < self.marketplace.queue_size_per_producer:
                for i in self.products:
                    list_param = decompose(i)
                    product_name = list_param.pop(0)
                    product_number = list_param.pop(0)
                    sleep_time = list_param.pop(0)

                    #incerc sa pun in market produsele
                    for j in range(product_number):
                        with my_lock:
                            self.marketplace.publish(0, product_name)
                            self.marketplace.number_products += 1
                            # print(product_name)
                            time.sleep(sleep_time)

        pass
