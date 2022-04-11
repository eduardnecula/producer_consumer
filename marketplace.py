"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import logging
import time
import unittest

from logging.handlers import RotatingFileHandler
from threading import Lock


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

        # initializare numar max de produse pentru fiecare producator
        self.queue_size_per_producer = queue_size_per_producer

        # lista in care se vor pune produsele de catre producatori
        # vor avea structura [{id-producator1, produs1}, ... {id-producatorn, produsn}]
        self.market_list = []

        # id-ul producatorului initial, ce va fi incrementat treptat
        self.id_producer = -1

        # lista cu numarul de produse pentru fiecare producator
        self.number_products_producers = []

        # pentru logging:
        logging.basicConfig(filename="marketplace.log",
                            format='%(asctime)s %(message)s', filemode='a')
        # convertire timp in standard gmtime
        logging.Formatter.converter = time.gmtime

        # acest logger va fi apelat pt mesaje de info
        self.logger = logging.getLogger('marketplace.log')
        # pot sa scriu maxBytes intr-un fisier numit marketplace.log
        # iar cand se depaseste maxBytes, se trece la urmatorul fisier
        # pana la max 100 de fisier
        handler = RotatingFileHandler("marketplace.log", maxBytes=20000000, backupCount=100)

        # handle pentru logging
        self.logger.addHandler(handler)

        # modul INFO, va fi apelat cu acest handler rotativ
        self.logger.setLevel(logging.INFO)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # setare id producator
        # fiecare producator primeste un numar unic
        lock = Lock()
        with lock:
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

        self.logger.info('Function In: publish, Args: Id of producer: %s,'
                         'Product type: %s', producer_id, product)

        # daca producatorul poate pune in marketplace
        can_publish = False

        # produsul este format din {id_producator si nume_produs}
        product_published = {producer_id: product}

        # verific cate produse are producatorul in cos
        products = self.number_products_producers[producer_id]

        if products[producer_id] < self.queue_size_per_producer:
            can_publish = True
            products[producer_id] += 1

        # produsul este adaugat
        if can_publish:
            self.market_list.append(product_published)

        self.logger.info('Function Out: publish,'
                         'Args: T/F (If the product can be added in the market): %s', can_publish)
        return can_publish

    def add_to_cart(self, product):
        """
        Adds a product to the given cart. The method returns

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        self.logger.info('Function In: add_to_cart, Args: Product type: %s', product)

        # daca bautura nu exista, se intoarce false
        find_drink = False

        product_string = str(product)

        # se trece prin lista de produse, si se cauta produsul adaugat
        # de un anumit producator
        for i in self.market_list:
            if str(i).find(product_string) != -1:
                # daca producatorul avea 5 produse, acum o sa aiba 4
                for j in i.keys():
                    dictionar = self.number_products_producers[j]
                    dictionar[j] -= 1

                    # daca produsul a fost gasit
                    find_drink = True

                    # se elimina 1 produs din lista, in caz ca exista
                    self.market_list.remove(i)

        self.logger.info('Function Out: add_to_cart,'
                         'Args: If the product can be bought: %s', find_drink)

        return find_drink

    def remove_from_cart(self, product):
        """
        Removes a product from cart.

        :type product: Product
        :param product: the product to remove from cart
        """
        self.logger.info('Function In: remove_from_cart, Args: Product type: %s', product)

        # daca produsul poate fi eliminat din lista consumatorului
        # si adaugat in market
        can_be_removed = False
        lock = Lock()

        product_published = {0: product}
        product = self.number_products_producers[0]

        # adaugarea este sincronizata, deoarece mai multi consumatori
        # pot sa adauge la acelasi id
        with lock:
            if product[0] < self.queue_size_per_producer:
                self.market_list.append(product_published)
                can_be_removed = True
                product[0] += 1

        self.logger.info('Function In: remove_from_cart,'
                         'Args: If the product can be removed: %s', can_be_removed)

        return can_be_removed


class MyProduct:
    """
        Clasa copiata din product, deoarece dadea eroare de import
    folosita pentru testare
    Class that represents a product.
    """
    name: str
    price: int


class MyTea(MyProduct):
    """
        Clasa copiata din product, deoarece dadea eroare de import
    folosita pentru testare
    Tea products
    """
    type: str


class MyCoffee(MyProduct):
    """
        Clasa copiata din product, deoarece dadea eroare de import
    folosita pentru testare
    Coffee products
    """
    acidity: str
    roast_level: str


class TestMarketplace(unittest.TestCase):
    """
    Clasa ce testeaza functiile din clasa marketplace
    """

    # Initializare date necesare pentru teste
    @classmethod
    def setUpClass(cls):
        # Marketplace initializat cu max 2 produse pentru fiecare producator
        cls.marketplace = Marketplace(2)

        # produs de tip ceai
        tea = MyTea()
        tea.name = 'Linden'
        tea.price = 9
        tea.type = 'Herbal'

        # produs de tip cafea
        coffee = MyCoffee
        coffee.name = 'Indonezia'
        coffee.price = 1
        coffee.acidity = 5.05
        coffee.roast_level = 'MEDIUM'

        # produs de tip ceai, pus ca in structura din tema
        cls.product_tea = (tea, 2, 0.18)

        # produs de tip cafea, pus ca in structura din tema
        cls.product_coffee = (coffee, 1, 0.23)

    # test pentru metoda register_producer()
    def test_register_producer(self):
        """
            Test pentru metoda register_producer()
            Se verifica de 1000 de ori, daca se returneaza un id
        cu 1 mai mare decat cel precedent, acest id se da unui producator
        atunci cand este apelat de un producator
        """
        i = 1000
        while i:
            marketplace = Marketplace(10)

            producer_id = marketplace.register_producer()
            self.assertEqual(producer_id, 0)

            producer_id = marketplace.register_producer()
            self.assertEqual(producer_id, 1)

            producer_id = marketplace.register_producer()
            self.assertEqual(producer_id, 2)

            producer_id = marketplace.register_producer()
            self.assertEqual(producer_id, 3)

            i -= 1

    # Test pentru metoda publish()
    def test_publish(self):
        """
            Se adauga 4 produse in market.
        Deoarece marketul poate sa tina doar 2 produse pentru acest producator,
        primele 2 adaugari dau True, iar restul False, deoarece marketul este plin
        """
        producer_id = self.marketplace.register_producer()

        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_tea)
        # acest test trebuie sa dea True, deoarece in market se accepta 2 produs
        self.assertEqual(been_put, True)

        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_tea)
        # acest test trebuie sa dea True, deoarece in market se accepta 2 produs
        self.assertEqual(been_put, True)

        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_tea)
        # acest test trebuie sa dea False, deoarece in market se accepta 2 produs
        self.assertEqual(been_put, False)

        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_tea)
        # acest test trebuie sa dea False, deoarece in market se accepta 2 produs
        self.assertEqual(been_put, False)

    # test pentru metoda add_to_cart()
    def test_add_to_cart(self):
        """
            Functia testeaza daca produsele din cos, exista si pot sa fie luate
        caz in care se afiseaza True, daca produsele nu exista se afiseaza False
        se adauga 2 produse, apoi se iau 4, primele 2 apelari trebuie sa fie True
        iar restu False
        """
        self.marketplace = Marketplace(2)
        producer_id = self.marketplace.register_producer()

        # pun in market 1 produs de tip ceai
        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_tea)
        # acest test trebuie sa dea True, deoarece in market se accepta 2 produs
        self.assertEqual(been_put, True)

        # pun in market 1 produs de tip cafea
        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_coffee)
        # acest test trebuie sa dea True, deoarece in market se accepta 2 produs
        self.assertEqual(been_put, True)

        # caut sa vad exista in market 1 produs de tip cafea
        # deoarece l-am pus mai sus, acesta exista
        product_in_market = self.marketplace.add_to_cart(self.product_coffee)
        self.assertEqual(product_in_market, True)

        # caut sa vad exista in market 1 produs de tip ceai
        # deoarece l-am pus mai sus, acesta exista
        product_in_market = self.marketplace.add_to_cart(self.product_tea)
        self.assertEqual(product_in_market, True)

        # acum teoretic, nu mai exista produse in market
        # urmatoarele 2 apeluri ar trebui sa intoarca False
        product_in_market = self.marketplace.add_to_cart(self.product_tea)
        self.assertEqual(product_in_market, False)

        product_in_market = self.marketplace.add_to_cart(self.product_coffee)
        self.assertEqual(product_in_market, False)

    # test pentru metoda remove_from_cart()
    def test_remove_from_cart(self):
        """
            Functia adauga 1 produs de tip ceai.
            Apoi 1 consumator elimina un produs din cosul lui de tip ceai.
            In market sunt 2 produse de tip ceai, iar la final se extra cele 2 produse,
            pentru a se testa existenta celor 2 produe in marketplace.
        """
        self.marketplace = Marketplace(4)
        producer_id = self.marketplace.register_producer()

        # pun in market 1 produs de tip ceai
        self.marketplace.number_products_producers.append({producer_id: 0})
        been_put = self.marketplace.publish(producer_id, self.product_tea)
        self.assertEqual(been_put, True)

        # se elimina din cosul de cumparaturi al consumatorului
        # si se pune iar in marketplace
        has_been_removed = self.marketplace.remove_from_cart(self.product_tea)
        # testul este True, deoarece elementul a fost pus in marketplace
        self.assertEqual(has_been_removed, True)

        # acum in marketplace sunt 2 produse de tip ceai
        # se ia primul produs
        product_in_market = self.marketplace.add_to_cart(self.product_tea)
        self.assertEqual(product_in_market, True)

        # se ia al 2-lea produs
        product_in_market = self.marketplace.add_to_cart(self.product_tea)
        self.assertEqual(product_in_market, True)
