"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

# import pentru a folosi time.sleep()
import time

from threading import Thread, Lock


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
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
        """

        # initializare constructor, clasa Thread
        Thread.__init__(self, **kwargs)

        # valori primite in functie, ce vor fi folosite in metoda run()
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

        # lista de cumparaturi, a unui consumator
        # aici se vor adauga / sterge produse din marketplace
        self.shopping_list = []

    def run(self):
        # lock, pentru a afisa printurile fara probleme
        lock = Lock()

        # se trece prin fiecare carucior al consumatorului
        for i in self.carts:
            # in caz ca sunt mai multe carucioare in aceeasi lista
            for j in i:
                carts_type = j
                action_type = carts_type['type']
                product_type = carts_type['product']
                quantity = carts_type['quantity']

                # daca actiunea consumatorului este de adaugare
                if action_type == 'add':
                    # adaug in cos daca gasesc produsul in lista
                    # se adauga de quantity ori
                    while quantity:
                        # pana cand produsul nu este disponibil, nu se renunta la cumpararea lui
                        # in caz de esec, se asteapta retry_wait_time secunde
                        while True:
                            # daca se returneaza true, se adauga in lista produsul cumparat
                            add_cart = self.marketplace.add_to_cart(product_type)

                            # daca pot adauga in lista de cumparaturi
                            if add_cart:
                                name_consumer = self.kwargs['name']
                                to_append = str(name_consumer) + " bought " + str(product_type)

                                self.shopping_list.append(to_append)
                                # se trece la urmatorul produs vrut
                                break
                            time.sleep(self.retry_wait_time)

                        quantity -= 1
                else:
                    # comanda este de stergere, asa ca se adauga produsul
                    #  in lista de la marketplace
                    while quantity:
                        # se incearca adaugarea produsului inapoi in lista de la marketplace
                        # dar daca este plina lista, de la producator
                        # se asteapta retry_wait_time seconds
                        while True:
                            # daca functia returneaza true, se poate adauga produsul inapoi in lista
                            # iar in acelasi timp se sterge
                            # din lista de cumparaturi a consumatorului
                            remove_cart = self.marketplace.remove_from_cart(product_type)

                            if remove_cart:
                                name_consumer = self.kwargs['name']
                                to_append = str(name_consumer) + " bought " + str(product_type)
                                self.shopping_list.remove(to_append)
                                break

                        # asteptarea pana cand incearca consumatorul
                        # sa puna iar inapoi in marketplace
                        time.sleep(self.retry_wait_time)
                        quantity -= 1

        # dupa ce consumatorul termina cumparaturile, se afiseaza ce a cumparat
        # se foloseste un lock, pentru a nu se intercala printurile
        with lock:
            for i in self.shopping_list:
                print(i)
