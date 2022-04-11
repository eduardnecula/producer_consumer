"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

# pentru split pe un string
import re
# pentru sleep
import time
from threading import Thread

def decompose(product):
    """
    Primeste o linie dintr-o lista de produse,
    si intorce o lista cu fiecare camp din ea:
    (Tea(name='Linden', price=9, type='Herbal'), 2, 0.18)
    Va intoarce lista cuprinsa din urmatoarele elemente:
    (Tea(name='Linden', price=9, type='Herbal')
    2
    0.18
    """

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
        """

        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

        # the number of products put in the basket
        self.number_products = 0

        # id producator
        self.id_producer = -1

    def run(self):

        # setare id producator
        self.id_producer = self.marketplace.register_producer()

        # producator 0, a pus 0 produse
        self.marketplace.number_products_producers.append({self.id_producer: 0})

        producer_name = self.id_producer

        # producatorul incearca sa publice la infinit
        while True:

            # se trece prin fiecare produs din lista lui de produse
            for i in self.products:

                list_param = decompose(i)
                product_name = list_param.pop(0)
                product_number = list_param.pop(0)
                sleep_time = list_param.pop(0)

                # incerc sa pun in market produsele
                # daca produce un nr multiplu de produse, se itereaza prin numarul lor
                while product_number:
                    # se publica in lista de la MarketPlace produsul, daca se poate
                    can_publish = self.marketplace.publish(producer_name, product_name)
                    if can_publish:
                        # timpul de fabricare a produsului
                        time.sleep(sleep_time)
                    else:
                        # daca producatorul nu poate sa scrie, asteapta o perioada de timp
                        time.sleep(self.republish_wait_time)
                    product_number -= 1
