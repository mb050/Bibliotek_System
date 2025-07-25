from bibliotek.models import Book
from bibliotek.models import Author
from bibliotek.models import BookAuthor
from bibliotek.models import BorrowedBook
from bibliotek.models import BookCategory
from bibliotek.models import Customer
from bibliotek.models import Borrowed
from bibliotek.models import Library
from bibliotek.models import Category

from classes.borrowing_query import Borrowing_query

import random as rng


class Generate():
    def __init__(self, Seed=10):
        self.normal_dist = [1] * 20 + [2] * 15 + [3] * 9 + [4] * 4 + [5] * 2
        rng.seed(Seed)
        
    def new_seed(self):
        from time import time
        return round(time())    
        
    def initiate_auto(self):
        self.generate_book()
        self.generate_library()
        
        self.library_book_relation()
        self.generate_author()
        self.generate_category()
        self.author_book_relation()
        
        self.category_book_relation()
        self.generate_customer()
    
    def generate_book(self):        
        for i in range(1, 101):
            text = str(i)
            isbn = '0' * (10 - len(text)) + text
            is10 = isbn
            is13 = '000' + is10
            b = Book(title=f'bok{i}', isbn_10=is10, isbn_13=is13)
            b.save()

    def generate_library(self):
        for i in range(1, 21):
            Library(name=f'lib{i}', library_id=i).save()
    
    def library_book_relation(self):        
        lib = Library.objects.all()
        
        for i in Book.objects.all():
            n = rng.randint(0, 19)
            i.library_id = lib[n]
            i.save()
    
    def generate_author(self):
        for i in range(50):
            Author(name=f'aut{i}').save()
            
    
    def generate_category(self):
        cat = ['Action', 'Sci-fi', 'Romance', 'Fantasy', 'Comedy', 'Drama',
               'Biography', 'Tragedy', 'Dystopian', 'Mystery']
        
        for i in cat:
            Category(name=i).save()
    
    def author_book_relation(self):
        aut = Author.objects.all()
        n = len(aut)
        if n <= 0:
            return
        else:
            n -= 1
        
        for i in Book.objects.all():
            idx = rng.randint(0, 49)
            n_range = self.normal_dist[idx]
            temp = [''] * n_range
            
            for j in range(n_range):
                N = rng.randint(0, n)
                
                if N in temp:
                    continue
                else:
                    temp[j] = N
                    BookAuthor(author=aut[N], book=i).save()
    
    def category_book_relation(self):
        cat = Category.objects.all()
        n = len(cat)
        if n <= 0:
            return
        else:
            n -= 1
        
        for i in Book.objects.all():
            idx = rng.randint(0, 49)
            n_range = self.normal_dist[idx]
            temp = [''] * n_range
            for j in range(n_range):
                N = rng.randint(0, n)
                if N in temp:
                    continue
                else:
                    temp[j] = N
                    BookCategory(book=i, category=cat[N]).save()
                
    
    def generate_customer(self):
        for i in range(20):
            c = Customer(name=f'customer{i}')
            c.save()
        return
    
    def adjust_amount(self, n, n_lent, n_returned):
        n_l = n_r = n

        if n_lent is not None:
            n_l = n_lent
        
        if n_returned is not None:
            n_r = n_returned
            
            if n_r > n_l:
                n_r = n_l
            elif n_r < 0:
                n_r = 0
                
        return n, n_l, n_r
    
    def convert_to_list(self, nested_list):
        for i, j in enumerate(nested_list):
            nested_list[i] = j[0]
        
        return nested_list
    
    def fisher_yates(self, int_list):
        N = len(int_list)
        n = N - 1
        
        for i in range(N):
            idx = n - i
            r_int = rng.randint(0, idx)
            
            a = int_list[idx]
            int_list[idx] = int_list[r_int]
            int_list[r_int] = a

    def set_all_to_available(self):
        book = Book.objects.all()
        for i in book:
            if i.available is None:
                i.available = 'yes'
                i.save()
            
    
    def generate_borrowing_history(self, n=0, Seed=None, n_lent=None,
                                   n_returned=None):
        if Seed is None:
           Seed = self.new_seed()
        
        rng.seed(Seed)
        n, n_l, n_r = self.adjust_amount(n, n_lent, n_returned)
        customer = list(Customer.objects.all().values_list('id'))
        book = list(Book.objects.all().values_list('id'))
        bb = list(BorrowedBook.objects.all())

        # if len(bb) != 0:
        #     bb_id = bb[-1].id

        for i, j in enumerate(bb):
            bb[i] = j.book.id
        
        for i in bb:
            if i in book:
                idx = book.index(i)
                book.pop(idx)
                
        self.convert_to_list(customer)
        self.convert_to_list(book)
        
        borrow = Borrowing_query()
        N_r = n_r - 1
        n_book = len(book) - 1
        n_customer = len(customer) - 1
        for i in range(n_l):
            cust_id = customer[rng.randint(0, n_customer)]
            id_book = book[rng.randint(0, n_book)]
            borrow_id = borrow.lend_book(id_book, cust_id, False)
            if borrow_id is not None and i <= N_r:
                borrow.return_book(borrow_id, False)
















