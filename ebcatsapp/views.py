from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache
from forms import CategoriesForm
from eventbrite import Eventbrite

eventbrite = Eventbrite(settings.EVENTBRITE_API_TOKEN)

"""
Shows a list of categories to select
"""
def index(request):
    categories = cache.get('categories')
    if categories is None:
        categories = eventbrite.get_categories()
        cache.set('categories', categories)

    categories_form = CategoriesForm()
    categories_form.fields['checkboxes'].choices = categories
    return render(request, 'ebcatsapp/index.html',
                  {'categories_form': categories_form})

"""
Uses the three selected category ids to create
a paginated page of events

The query in eventbrite.get_category_events is
very expensive due to the page size being fixed at
50 for event search. If the cache is cold this
takes up to 15 seconds.

Params: cats - list of cat ids,
        page - page number for pagination, default 1
"""
def results(request):
    if 'cats[]' not in request.GET:
        return Http404()
    # get page num
    page_num = 1
    if 'page' in request.GET:
        page_num = request.GET.get('page')
    # get sorted list of cat ids
    # and use as cache key
    category_ids = map(int, request.GET.getlist('cats[]'))
    if len(category_ids) != 3:
        return Http404()
    category_ids.sort()
    category_ids = map(str, category_ids)

    cache_key = 'events' + ','.join(category_ids) + 'pg' + page_num

    events = cache.get(cache_key)
    if events is None:
        events = eventbrite.get_category_events(category_ids, page_num)
        cache.set(cache_key, events)
    return render(request, 'ebcatsapp/results.html', {
        'events': events['events'],
        'num_pages': events['pagination']['page_count'],
        'page_num': page_num
    })