import random

from torpedo.products.models import Category, Product


def get_products(number_of_products_to_return):
    """
    Helper function to return a specified number of products

    # NOTE when enough products are inserted remove this later
    """

    products = Product.objects()
    number_of_products = len(products)

    # FAKE IT TILL YOU MAKE IT
    fake_products = []
    if number_of_products < number_of_products_to_return:
        for i in range(0, number_of_products_to_return):
            # Randomly insert items into list to make it longer
            fake_products.append(
                    products[random.randint(0, number_of_products - 1)])

    return fake_products


def get_category_list(number_of_categories):
    """
    Helper function to query the Categories and return a number of Categories
    sorted by some metric
    """

    categories = Category.objects()

    return categories[:number_of_categories]
