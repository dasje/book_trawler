class Book:
    pages = None
    rank_in_list = None
    illustrators_last_name = None
    illustrators_first_name = None
    publisher = None
    imprint = None
    language = None
    series_no = None
    publish_date = None
    genre = None
    authors_last_name = None
    authors_first_name = None
    price = None
    currency = None
    binding = None
    title = None
    isbn = None

    def __init__(self):
        pass

    def __str__(self):
        return f"This is book {self.isbn} {self.title} by {self.authors_last_name}"

        # methods to check integrity of info
