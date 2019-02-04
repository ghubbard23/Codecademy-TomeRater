class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    #added get_name to cleanup output of positive users
    def get_name(self):
        return self.name

    def change_email(self, address):
        old_email = self.email
        self.email = address
        print("Email for user {} has been changed from {} to {}".format(self.name, old_email, self.email))

    def __repr__(self):
        return "User: {}, Email: {}, Books read: {}".format(self.name, self.email, len(self.books.keys()))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        self.book = book
        self.rating = rating
        self.books.update({self.book: self.rating})

    def get_average_rating(self):
        #modified to only count averages where books were ACTUALLY given ratings
        #rating of None should not be counted in the average rating
        i=0
        books_rated = []
        try:
            for book_rated, rating in self.books.items():
                if rating is not None:
                    i = i+rating
                    books_rated.append(book_rated)
        except:
            print("Something is wrong with the input for {}.".format(self.book))
        #adding in check to make sure a user has ANY ratings
        if (len(books_rated)) is not 0:
            return i/(len(books_rated))

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        try:
            #make sure isbn is only an integer
            self.isbn = int(isbn)
        except:
            print ("Error: ISBN should be numeric only")
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        try:
            old_isbn = self.isbn 
            self.isbn = int(new_isbn)
            print ("""The ISBN for {} has been changed...
    Old ISBN: {}
    New ISBN: {}
                """.format(self.title, old_isbn, self.isbn))
        except:
            print("Error: ISBN should be numeric only. {} - {} has not been changed".format(self.isbn, self.title))


    def add_rating(self, rating):
        self.rating = rating
        try:
            if int(rating) >= 0 and int(rating) <= 4:
                self.ratings.append(self.rating)
            else:
                print("Invalid Rating")
        except:
            print("Invalid Rating. You must enter a number between 0 and 4.")

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        i=0
        try:
            for item in self.ratings:
                i = i+item
        except:
            print("Something is wrong with the input for {}.".format(self.title))
        return i/(len(self.ratings))

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return self.title

class Fiction(Book):
    def __init__ (self, title, author, isbn):
        self.author = author
        super().__init__(title, isbn)
        

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)


class TomeRater:
    def __init__(self):
        #created list of isbns to check and make sure isbns were unique.
        #Each method should add the isbn to the list as it creates them.
        #Each creation method should check the list before creation
        self.users = {}
        self.books = {}
        self.isbns = []

    def create_book(self, title, isbn):
        if isbn in self.isbns:
            print("ISBN {} already exists in the database. Please give a unique ISBN.\n".format(isbn))
        else:
            self.isbns.append(isbn)
            print("Book {} with isbn {} created successfully!".format(title, isbn))
            return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        if isbn in self.isbns:
            print("ISBN {} already exists in the database. Please give a unique ISBN.\n".format(isbn))
        else:
            self.isbns.append(isbn)
            print("Book {} with isbn {} created successfully!".format(title, isbn))
            return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        if isbn in self.isbns:
            print("ISBN {} already exists in the database. Please give a unique ISBN.\n".format(isbn))
        else:
            self.isbns.append(isbn)
            print("Book {} with isbn {} created successfully!".format(title, isbn))
            return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users.keys():
            print("No user with email {}\n".format(email))
        else:
            user = self.users.get(email)
            user.read_book(book, rating)
            if rating is not None:
                book.add_rating(rating)
            if book not in self.books.keys():
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books=None):
        new_user = User(name, email)
        #Basically setting up a stop. If all check pass, then proceed is set to True and User can be added
        proceed = False
        #probably a better way to do this. I am splitting at the "." in the email which should confim there is a period, 
        #then comparing the result to the list of valid extensions.
        #Later, I check that the extension is valid before proceeding with add user
        valid_email_extensions = ["com", "edu", "org"]
        try:
            ext = (email.split(".")[-1])
            valid_ext = False
            for item in valid_email_extensions:
                if ext == item:
                    valid_ext = True
        except:
            print("Email not formatted correctly.")
        #check first to see if I can get the email. If not, add the user
        if self.users.get(email):
            print ("User with email address {} already exists.\n".format(email))
        elif "@" not in email:
            print("Missing @: Email address {} not valid. Try again. \n".format(email))
        elif valid_ext == False:
            print("You typed: {} - Email must end in .com, .edu or .org.\n".format(email))
        else:
            proceed = True
        if proceed == True:
            self.users.update({email: new_user})
            print("User {} with email {} added successfully!\n".format(name, email))
            if user_books is not None:
                for book in user_books:
                    self.add_book_to_user(book, email, rating=None)
        
    def print_catalog(self):
        print("Printing Catalog...")
        for book in self.books.keys():
            print(book)
        print("\n")

    def print_users(self):
        print("Printing users...")
        for user in self.users.values():
            print(user)
        print("\n")

    def most_read_book(self):
        #max would have been helpful in other methods, but they are already written and working :/
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        book_title = " "
        largest_average = float("-inf")
        average_rating_dict = {}
        for book in self.books.keys():
            average_rating = book.get_average_rating()
            average_rating_dict.update({book: average_rating})
        for key, value in average_rating_dict.items():
            if value > largest_average:
                book_title = key
                largest_average = value
        return "{} with an average rating of {}".format(book_title, largest_average)

    def most_positive_user(self):
        positive_user = " "
        largest_average = float("-inf")
        for user in self.users.values():
            average = user.get_average_rating()
            #added "average is not None" to handle any users that have no ratings
            if average is not None and average > largest_average:
                largest_average = average
                positive_user = user
        return (positive_user.get_name() + " with an avearge rating of {}".format(largest_average))