from getpass import getpass
from mysql.connector import connect, Error


def create_db():
    """Requests MySQL login info, creates a db called bestseller_books, and lists all available db's."""
    try:
        # connect to mysql server with login info
        with connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
        ) as connection:

            # create db
            create_db_query = "CREATE DATABASE bestseller_books"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)

            # list all available db's
            show_db_query = "SHOW DATABASES"
            with connection.cursor() as cursor:
                cursor.execute(show_db_query)
                for db in cursor:
                    print(db)
    except Error as e:
        print(e)


def connect_to_db():
    """Requests MySQL login info and then """
    try:
        with connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
                database="bestseller_books",
        ) as connection:
            con = connection
            return con
    except Error as e:
        print(e)


class CreateTables:
    def __init__(self):
        self.connection = connect_to_db()

    def new_db_with_fields(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute(table_name)
            self.connection.commit()

    def create_country_table(self):
        bestseller_books_country_query = """
        CREATE TABLE country(
            id INT AUTO_INCREMENT PRIMARY KEY,
            country VARCHAR(100),
        )
        """
        self.new_db_with_fields(bestseller_books_country_query)

    def create_source_table(self):
        bestseller_books_source_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            country_id INT,
            FOREIGN KEY(country_id) REFERENCES country(id),
        )
        """
        self.new_db_with_fields(bestseller_books_source_query)

    def create_top_table(self):
        bestseller_books_top_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            book_id INT,
            rank INT,
            source_id INT,
            FOREIGN KEY(book_id) REFERENCES book(id),
            FOREIGN KEY(source_id) REFERENCES source(id),
        )
        """
        self.new_db_with_fields(bestseller_books_top_query)

    def create_book_table(self):
        bestseller_books_book_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            isbn INT,
            title VARCHAR(100),
            binding INT,
            price DECIMAL(5, 4),
            author_id INT,
            genre_id INT,
            publish_date DATE,
            series_no INT,
            language_id INT,
            imprint_id INT,
            illustrator_id INT,
            pages INT,
            FOREIGN KEY(author_id) REFERENCES author(id),
            FOREIGN KEY(genre_id) REFERENCES genre(id),
            FOREIGN KEY(language_id) REFERENCES language(id),
            FOREIGN KEY(imprint_id) REFERENCES imprint(id),
            FOREIGN KEY(illustrator_id) REFERENCES illustrator(id),
        )
        """
        self.new_db_with_fields(bestseller_books_book_query)

    def create_author_table(self):
        bestseller_books_author_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
        )
        """
        self.new_db_with_fields(bestseller_books_author_query)

    def create_genre_table(self):
        bestseller_books_genre_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            genre VARCHAR(100),
        )
        """
        self.new_db_with_fields(bestseller_books_genre_query)

    def create_language_table(self):
        bestseller_books_language_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            language VARCHAR(100),
        )
        """
        self.new_db_with_fields(bestseller_books_language_query)

    def create_imprint_table(self):
        bestseller_books_imprint_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            publisher_id INT,
            imprint VARCHAR(100),
            FOREIGN KEY(publisher_id) REFERENCES publisher(id),
        )
        """
        self.new_db_with_fields(bestseller_books_imprint_query)

    def create_publisher_table(self):
        bestseller_books_publisher_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            publisher VARCHAR(100),
        )
        """
        self.new_db_with_fields(bestseller_books_publisher_query)

    def create_illustrator_table(self):
        bestseller_books_illustrator_query = """
        CREATE TABLE source(
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
        )
        """
        self.new_db_with_fields(bestseller_books_illustrator_query)

    def create_all_tables(self):
        self.create_country_table()
        self.create_source_table()
        self.create_top_table()
        self.create_book_table()
        self.create_author_table()
        self.create_genre_table()
        self.create_language_table()
        self.create_imprint_table()
        self.create_publisher_table()
        self.create_illustrator_table()
