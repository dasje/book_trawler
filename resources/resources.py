top_markers = ['parool-top-10-fictie', 'Top 10 Kinderboeken', ]
site_nav = {
    """Key = site name | Value = list, if multiple steps needed to get to information.
    Bottom most step comes first. Else, dictionary with steps.
    Steps are for BeautifulSoup navigation: find_all, get with filter, get_text"""
    'scheltema.nl': {
        'author': [{
            'findall': 'meta',
            'filter': {
                'itemprop': 'content'
            }
        },
            {
                'findall': 'div',
                'filter': {
                    'itemprop': 'author'
                }
            }
        ],

        'title': [{
            'findall': 'meta',
            'filter': {
                'itemprop': 'name'
            }
        }],

        'isbn': [{
            'findall': 'meta',
            'filter': {
                'itemprop': 'isbn'
            }
        }],
    },

    'stumpel.nl': {
        'author': [{
            'findall': 'td',
            'filter': {
                'data-th': 'Auteur'
            },
            'get_text': 'td',
        }],
        'isbn': [{
            'findall': 'td',
            'filter': {
                'data-th': 'ISBN'
            },
            'get_text': 'td',
        }],
        'title': [{
            'findall': 'meta',
            'filter': {
                'property': 'og:title'
            },
            'get': 'content'
        }]
    },

    'bol.com': {
        'author': [{
            'findall': 'a',
            'filter': {
                'data-role': 'AUTHOR'
            },
            'get_text': 'a',
        }],
        'isbn': [{
            'findall': 'dd',
            'filter': {
                'class': 'specs__title'
            },
            'get_text': 'dd',
            'check': r'/d{9}$'
        }],
        'title': [{
            'findall': 'span',
            'filter': {
                'data-test': 'title'
            },
            'get_text': 'span'
        }]
    },

    'ako.nl': {
        'author': [{
            'findall': 'h2',
            'filter': {
                'itemprop': 'author'
            },
            'get_text': 'h2'
        }],
        'isbn': [{
            'findall': 'meta',
            'filter': {
                'property': 'product:retailer_item_id'
            },
            'get': 'content'
        }],
        'title': [{
            'findall': 'meta',
            'filter': {
                'property': 'og:title'
            },
            'get': 'content'
        }]
    },

    'bruna.nl': {
        'author': [{
            'findall': 'script',
            'filter': {
                'type': 'application/json'
            },
            'json': 'name'
        }],
        'isbn': [{
            'findall': 'meta',
            'filter': {
                'property': 'og:isbn'
            },
            'get': 'content'
        }],
        'title': [{
            'findall': 'meta',
            'filter': {
                'property': 'og:title'
            },
            'get': 'content'
        }]
    }
}
