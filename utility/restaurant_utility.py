from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from Yummy.models import Restaurant


def makePaginate(objects, page_number=1, number_in_page=6):
    paginator = Paginator(objects, number_in_page)
    try:
        allObjects = paginator.page(page_number)
    except PageNotAnInteger:
        allObjects = paginator.page(1)
    except EmptyPage:
        allObjects = paginator.page(paginator.num_pages)

    return allObjects


def get_allRestaurant(searched_key, page_number=1):
    """searched_key is coming from ( tools.html OR search bar OF home.html )"""
    if searched_key is not None:
        allRestaurant = Restaurant.objects.filter(name__contains=searched_key,
                                                  is_submit=True).order_by('name')
    else:
        allRestaurant = Restaurant.objects.filter(is_submit=True).order_by('name')
    return makePaginate(allRestaurant, page_number)
