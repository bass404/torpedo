from torpedo.products.models import Category


def get_category_list(number_of_categories):
    """
    Helper function to query the Categories and return a number of Categories
    sorted by some metric
    """

    categories = Category.objects()

    return categories[:number_of_categories]
