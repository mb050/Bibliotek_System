from bibliotek.models import BorrowedBook
from bibliotek.models import BorrowingLog
from bibliotek.models import Category
from bibliotek.models import Borrowed
from bibliotek.models import Library
from bibliotek.models import Author
from bibliotek.models import Book
from classes.base import Base

from datetime import date
import numpy as np

class Analytic(Base):
    """
    containts queries related to the analytics.
    
    methods:
        get_book_objects_list: get a list with book objects.
        edit_overdue: change overdue status for a single borrowing object.
        update_overdue_status: change overdue status for all borrowing objects.
        generic_overview: general table for libraries.
        generic_query_analytic: combined method for author and category.
        book_analytic: makes a table for book analytics.
        author_analytic: makes a table for author analytics.
        category_analytic: makes a table for category analytics.
    """
    
    def get_book_objects_list(self):
        """
        get a list containing book objects from the both active borrowed books
        and books previously borrowed.
        
        returns:
            book_list (list): list with book objects.
        """
        book_list = []
        
        for i in Borrowed.objects.all():
            try:
                book_obj = BorrowedBook.objects.get(borrow=i).book
            except:
                continue
            else:
                book_list.append(book_obj)
        
        for i in BorrowingLog.objects.all():
            try:
                book_obj = Book.objects.get(id=i.book_id)
            except:
                continue
            else:
                book_list.append(book_obj)
            
        return book_list
    
    def edit_overdue(self, borrow_obj, current_date=None):
        """
        edit overdue for a given borrow object.
        
        args:
            borrow_obj (query object): borrowed object.
            current_date (date): if no date is given then current date is used.
        """
        if current_date is None:
            current_date = date.today()
        
        date_diff = borrow_obj.due_date - current_date  
        if date_diff.days < 0: 
            borrow_obj.overdue = 'yes'
            borrow_obj.save()
    
    def update_overdue_status(self):
        """
        edit overdue status for all borrowed objects.
        """
        borrow_obj = Borrowed.objects.all()
        current_date = date.today()
        
        for i in borrow_obj:
            self.edit_overdue(i, current_date)
    
    def generic_overview(self, get_table=False):
        """
        get a table for libraries containing their id, amount of books, amount
        of lent out books, and amount of books that are overdue. It sums up
        and give the total of books, lent_out_books and books_overdue, 
        including books with no library id.
        
        args:
            get_table (bool): controls if a table is printed to terminal
        """
        borrow_obj = Borrowed.objects.all()
        lib = Library.objects.all()
        book = Book.objects.all()
        
        lib_id = list(lib.values_list('library_id'))
        id_dict = {}
        
        for i, j in enumerate(lib_id):
            id_dict[j[0]] = np.zeros(3)
        id_dict[None] = np.zeros(3)
        
        self.update_overdue_status()
        
        for i in borrow_obj:
            bb = BorrowedBook.objects.get(borrow=i)
            book_obj = bb.book
            library_key = book_obj.library_id
            
            id_dict[library_key][1] += 1
            
            if i.overdue == 'yes':
                id_dict[library_key][2] += 1

        result = [''] * len(lib)
        total = np.zeros(3)
        for i, j in enumerate(lib):
            key = j.library_id
            arr = id_dict[key]
            
            id_dict[key][0] = book.filter(library_id=j).count()
            result[i] = ['', key] + list(arr)
            total += arr
        
        result = self.sort_list(result, 3)
        
        id_dict[None][0] = book.filter(library_id=None).count()
        total += id_dict[None]
        result += [['', 'missing'] + list(id_dict[None])]
        
        header = ['', 'library_id', 'books', 'lent_out_books', 'books_overdue']        
        result += [['total', None] + list(total)]
        table = self.make_table(result, header)
        
        if get_table is not False:
            print(table)
    
    def generic_query_analytic(self, var_name='author', get_table=False):
        """
        combined method for the analytics for author and category.
        
        args:
            get_table (bool): controls if a table is printed to terminal
        """
        if var_name == 'author':
            query_obj = Author.objects.all()
        else:
            query_obj = Category.objects.all()
        
        query_dict = {}
        
        for i, j in enumerate(query_obj.values_list('name')):
            query_dict[j[0]] = i
            
        query_arr = np.zeros((len(query_dict), 2))
        
        for i in self.get_book_objects_list():
            if var_name == 'author':
                queries = query_obj.filter(bookauthor__book=i)
            else:
                queries = query_obj.filter(bookcategory__book=i)
           
            for val_query in queries:
                query_name = val_query.name
                idx = query_dict[query_name]
                query_arr[idx, 0] += 1
        
        tot = sum(query_arr[:, 0])
        query_arr[:, 1] = np.round(query_arr[:, 0] / tot, 4) * 100
        result = [''] * len(query_arr)
        
        for i, j in enumerate(query_dict.keys()):
            result[i] = [j] + list(query_arr[query_dict[j]])
        
        result = self.sort_list(result, 2)        
        header = ['name', 'frequency', 'percentage']
        table = self.make_table(result, header)
        
        if get_table is not False:
            print(table)

    def book_analytic(self, get_table=False):
        """
        get a table of all the books containing their id, frequency of being 
        lent out, and percentage.
        
        args:
            get_table (bool): controls if a table is printed to terminal
        """
        book_obj = Book.objects.all()
        book_dict = {}
        
        for i, j in enumerate(book_obj.values_list('id')):
            book_dict[j[0]] = i
            
        book_arr = np.zeros((len(book_dict), 2))
        
        for i in self.get_book_objects_list():
            idx = book_dict[i.id]
            book_arr[idx, 0] += 1

        tot = sum(book_arr[:, 0])
        book_arr[:, 1] = np.round(book_arr[:, 0] / tot, 4) * 100
        result = [''] * len(book_arr)
        
        for i, j in enumerate(book_dict.keys()):
            result[i] = [j] + list(book_arr[book_dict[j]])
        
        result = self.sort_list(result, 2)
        header = ['book_id', 'frequency', 'percentage']
        table = self.make_table(result, header)
        
        if get_table is not False:
            print(table)

    def author_analytic(self, get_table=False):
        """
        get a table of all authors containing their name, frequency of being 
        lent out, and percentage.
        
        args:
            get_table (bool): controls if a table is printed to terminal
        """
        author_obj = Author.objects.all()
        author_dict = {}
        
        for i, j in enumerate(author_obj.values_list('name')):
            author_dict[j[0]] = i
            
        author_arr = np.zeros((len(author_dict), 2))
        
        for i in self.get_book_objects_list():
            authors = author_obj.filter(bookauthor__book=i)
           
            for aut_query in authors:
                author_name = aut_query.name
                idx = author_dict[author_name]
                author_arr[idx, 0] += 1
        
        tot = sum(author_arr[:, 0])
        author_arr[:, 1] = np.round(author_arr[:, 0] / tot, 4) * 100
        result = [''] * len(author_arr)
        
        for i, j in enumerate(author_dict.keys()):
            result[i] = [j] + list(author_arr[author_dict[j]])
        
        result = self.sort_list(result, 2)
        header = ['name', 'frequency', 'percentage']
        table = self.make_table(result, header)
        
        if get_table is not False:
            print(table)

    def category_analytic(self, get_table=False):
        """
        get a table of all categories containing their name, frequency of being 
        lent out, and percentage.
        
        args:
            get_table (bool): controls if a table is printed to terminal
        """
        category_obj = Category.objects.all()
        category_dict = {}
        
        for i, j in enumerate(category_obj.values_list('name')):
            category_dict[j[0]] = i
            
        category_arr = np.zeros((len(category_dict), 2))
        
        for i in self.get_book_objects_list():
            categories = category_obj.filter(bookcategory__book=i)
            
            for cat_query in categories:
                category_name = cat_query.name
                idx = category_dict[category_name]
                category_arr[idx, 0] += 1
        
        tot = sum(category_arr[:, 0])
        category_arr[:, 1] = np.round(category_arr[:, 0] / tot, 4) * 100
        result = [''] * len(category_arr)
        
        for i, j in enumerate(category_dict.keys()):
            result[i] = [j] + list(category_arr[category_dict[j]])
        
        result = self.sort_list(result, 2)
        header = ['name', 'frequency', 'percentage']
        table = self.make_table(result, header)
        
        if get_table is not False:
            print(table)

    



