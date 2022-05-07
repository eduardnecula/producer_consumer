Topic 1 - ASC
Necula Eduard-Ionut, 332CA

Theme explanation:



Producer:

Implemented in the producer.py file.

Manufacturer logic:
        Each manufacturer tries to publish indefinitely, until the number of published products reaches a maximum
    is given in the marketplace.
        Each manufacturer iterates through the number of products it can publish, of each type. If this
    says he can produce 5 tea products and 2 coffee products, he will put 5 tea products in a row
    then the 2 coffee products.
        If a manufacturer cannot publish, it will wait until a product is purchased from its list.

How does the program know how many products each manufacturer has?
        In the marketplace, there is a list, in which, for each manufacturer that appears on the market, an id is added to the list
    for the manufacturer, and its number of products with the structure: {manufacturer_id: product_no}. If no_products arrive
    at the maximum defined in the marketplace, then the manufacturer waits until it can publish again.
        After each product you can add, wait a period of time, which is the creation time
    of the product.
        Each manufacturer receives an id, which is synchronized with Lock () because it is unique, and is incremented
    with each appearance of a new manufacturer.



Consumer:

Implemented in the consumer.py file.

Consumer logic:
        Every consumer tries to buy a certain type of product, a number of times.
        Because the consumer has multiple infinite strollers, iterates through each stroller.
        Through each stroller, you search for what product you want and how many times you want this product, then iterate through the number
    of desired products.
        The consumer calls add_to_cart () from the marketplace, which returns True / False. True if the product exists on
    market, and false otherwise.
        If the consumer finds the product on the market, which means that he receives True from add_to_cart (), then
    the consumer will add the product to his shopping list.
        If the consumer adds the product to his cart, he knows from which manufacturer he bought this product, and in
    the list of the number of products of each manufacturer will decrease the number of products by 1.
        If the consumer changes his mind and deletes a product from his shopping list, then the product will go away
    returns to the marketplace, and the number of products in the list of the manufacturer from which it was purchased will increase by 1.
        When the consumer does not find the product anywhere on the market, he waits for a predefined time, and more
    he tries until his shopping list is over.
        When a consumer completes his shopping list, he will display the list. The list is displayed in sync
    by using Lock (), so that the prints do not intersperse.



Marketplace:

Implemented in the marketplace.py file

Marketplace logic:
    This is the file with the functions called by the manufacturer and the consumer.
    It contains the following functions:

        1. register_producer (): returns an id for the producer, being synchronized, to have a unique id

        2. publish (): if a manufacturer can publish a product, it will return True. If the number of products entered
        by the manufacturer is less than a predefined maximum in the marketplace, then the product will be published

        3. add_to_cart (): if a product is in the marketplace, this function will return True, that product
        will be taken from the marketplace, and the number of products of a manufacturer will be decremented

        4. remove_from_cart (): if the product that a consumer removes can be placed in the marketplace, it will return
        True, the number of products a manufacturer will increase


Logging:
        The received parameters were displayed at the beginning of each function.
        At the end of each function, what returns the function is displayed.
        Each INFO logging message contains the time in gmtime format, the function name and a short description of
    displayed parameters.


UnitTesting:
    For each function in the marketplace class, 1 test has been implemented, which verifies the functionalities of the function

    1. For register_producer (), check that a manufacturer's index is returned correctly

    2. For the publish () function, make sure that the products are added to the marketplace, as far as possible.
    otherwise it fails

    3. For the add_to_cart () function, it is verified that an existing product in the marketplace can be added to the
    shopping of a consumer, otherwise the function fails

    4. For the remove_from_cart () function, check if a product in a consumer list is added
    in the marketplace

        Each test checks several cases, both positive and negative, if they do not give True / False, it means that
    the logic of the function is not good.


        Program logicui is fully implemented, the id functions for the cart and the list from the id of a cart not
     were implemented, due to the lack of logic for the final display. If the card ID was required on display,
     these could also be implemented.

     Useful resources:
         https://ocw.cs.pub.ro/courses/asc/laboratoare/01https://ocw.cs.pub.ro/courses/asc/laboratoare/01
         https://ocw.cs.pub.ro/courses/asc/laboratoare/02
         https://ocw.cs.pub.ro/courses/asc/laboratoare/03
