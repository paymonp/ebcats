import requests

"""
A wrapper for the Eventbrite API to be used in the app
"""
class Eventbrite:
    API_PREFIX = 'https://www.eventbriteapi.com/v3/'

    def __init__(self, token):
        self.token = token

    """
    Returns a list of tuples with the format:
    (category id, category name)
    """
    def get_categories(self):
        categories_json = self.make_api_request('categories/')
        if 'categories' not in categories_json:
            return []
        # filter out just the name and id
        categories = [(cat['id'], cat['name'])
                      for cat in categories_json['categories']]
        return categories

    """
    Returns a list of events

    Params: list of cat ids
    """
    def get_category_events(self, category_ids, page=1):
        args = {'categories': ','.join(map(str, category_ids)),
                'page': page,
                'sort_by': 'date'}
        events_json = self.make_api_request('events/search/', args)
        if 'events' not in events_json:
            return []
        return events_json

    def make_api_request(self, path, args={}):
        args['token'] = self.token
        args['format'] = 'json'
        return requests.get(self.API_PREFIX + path, params=args).json()
