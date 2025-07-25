from bibliotek.models import BorrowedCustomer
from bibliotek.models import BorrowedBook
from bibliotek.models import BorrowingLog
from bibliotek.models import Borrowed
from bibliotek.models import Customer
from bibliotek.models import Library
from bibliotek.models import Book

from classes.book_query import Book_query

from datetime import datetime, timedelta, date
import numpy as np

class Borrowing_query(Book_query):
    """
    containts queries related to borrowing books.
    
    methods:
        get_customer_obj: checks if a customer object exist.
        get_book_obj: checks if a book object exist.
        get_borrowed_obj: checks if a borrowed object exist.
        print_message: method to control if a message is given or not.
        edit_overdue: updates overdue for a single object.
        update_overdue_status: update all overdue statuses.
        check_limit: check if a customer have reached max amount for a library.
        book_customer_id: check if both book and customer object exist.
        borrow_customer_id: check if both borrow and customer object exist.
        lend_book: lend a book.
        extend_lending: extend the lending period of a book.
        return_book: return a book.
        get_borrowed_books: get a table of all borrowed books.
        get_overdue: get a table of all books that are overdue.
        customer_active_overview: table with the active overview for a customer.
        customer_history_overview: table with the log overview for a customer.
        customer_full_overview: table with the full overview for a customer.
        log_overview: get a table with the general borrowing log.
        delete_borrowing_obj: delete a borrowed object.
    """
    
    def __init__(self):
        """
        checks all overdue statuses and creates an instance.
        """
        self.update_overdue_status()
        self.date_today = datetime.today().strftime('%Y-%m-%d')
    
    def get_customer_obj(self, customer_id, default_message=True):
        """
        check if a customer object exist given a customer id.
        
        args:
            customer_id (str): id of customer.
            default_message (bool): control if an error message is given.
        
        returns:
            customer_obj (query object) or None (bool)
        """
        try:
            return Customer.objects.get(id=customer_id)
        except:
            message = 'no customer with that id'
            self.print_message(message, default_message)
            return
        
    def get_book_obj(self, book_id, default_message=True):
        """
        check if a book object exist given a book id.
        
        args:
            book_id (str): id of book.
            default_message (bool): control if an error message is given.
        
        returns:
            book_obj (query object) or None (bool)
        """
        try:
            return Book.objects.get(id=book_id)
        except:                
            message = 'no book or books with that id'
            self.print_message(message, default_message)
            return
    
    def get_borrowed_obj(self, borrow_id, default_message=True):
        """
        check if a borrow object exist given a borrow id.
        
        args:
            borrow_id (str): id of borrowed book.
            default_message (bool): control if an error message is given.
        
        returns:
            borrow_obj (query object) or None (bool)
        """
        try:
            return Borrowed.objects.get(id=borrow_id)
        except:
            message = 'no borrow object with that id'
            self.print_message(message, default_message)
            return
    
    def print_message(self, message, default_message=True):
        """
        method for easier control of output of error messages.
        
        args:
            message (str): message to be given.
            default_message (bool): control if an error message is given.
        """
        if default_message is True:
            print(message)
    
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
    
    def check_limit(self, customer_id):
        """
        check if a given customer have borrowed a maximum of 5 books from a 
        single library.
        
        args:
            customer_id (str): id of customer.
        
        returns:
            limit (list): list containing the library_id if the limit has been
                          been reached for said library.
        """
        borrow_obj = Borrowed.objects.all() 
        borrow_obj = borrow_obj.filter(borrowedcustomer__customer=customer_id)
        lib = Library.objects.all().values_list('library_id')
        lib_dict = {}
        limit = []
        
        for i in lib:
            lib_dict[i[0]] = 0

        for i in borrow_obj:
            bb = BorrowedBook.objects.get(borrow=i)
            lib_dict[bb.book.library_id] += 1
        
        for i in lib_dict.keys():
            if lib_dict[i] >= 5:
                limit.append(i)

        return limit
    
    def book_customer_id(self, book_id, customer_id, default_message=True):
        """
        check if both book and customer object exist, given their respective 
        id.
        
        args:
            book_id (str): id of book.
            customer_id (str): id of customer.
            default_message (bool): control if an error message is given.
        
        returns:
            touple of (query object, query object) or None (bool)
        """
        customer_obj = self.get_customer_obj(customer_id, default_message)
        book_obj = self.get_book_obj(book_id, default_message)
        
        if book_obj is not None and customer_obj is not None:
            return (book_obj, customer_obj)
        
    def borrow_customer_id(self, borrow_id, customer_id, default_message):
        """
        check if both borrowed and customer object exist, given their 
        respective id.
        
        args:
            borrow_id (str): id of borrowed book.
            customer_id (str): id of customer.
            default_message (bool): control if an error message is given.
        
        returns:
            touple of (query object, query object) or None (bool)
        """
        customer_obj = self.get_customer_obj(customer_id, default_message)
        borrow_obj = self.get_borrowed_obj(borrow_id, default_message)
        
        if borrow_obj is not None and customer_obj is not None:
            return (borrow_obj, customer_obj)
    
# =============================================================================
    
    def lend_book(self, book_id, customer_id, default_message=True):
        """
        lend a book.
        
        args:
            book_id (str): id of book.
            customer_id (str): id of customer.
            default_message (bool): control if an error message is given.
        
        returns:
            borrow_obj.id (int) or None (bool)
        """
        objects_tuple = self.book_customer_id(book_id, customer_id, 
                                              default_message)
        if objects_tuple is None:
            return
        
        book_obj, customer_obj = objects_tuple
        
        if book_obj.library_id in self.check_limit(customer_id):
            message = str('cannot borrow more than 5 books from library: {}'
                          ).format(book_obj.library_id)
                  
            self.print_message(message, default_message)
            return
        elif book_obj.available in ['yes', 1]:
            self.edit_available(book_obj)
        else:
            self.print_message('book is not available', default_message)
            return
        
        date_today = datetime.today()
        borrow_obj = Borrowed(lending_date=date_today.strftime('%Y-%m-%d'))
        lending_time = borrow_obj.default_lending_period
        return_date = date_today + timedelta(days=lending_time)
        borrow_obj.due_date = return_date.strftime('%Y-%m-%d')
        
        if borrow_obj.extentions != 0:
            borrow_obj.extentions = 0
        
        borrow_obj.save()
        
        BorrowedBook(book=book_obj, borrow=borrow_obj).save()
        BorrowedCustomer(customer=customer_obj, borrow=borrow_obj).save()
        return borrow_obj.id

    def extend_lending(self, borrow_id, n_days, default_message=True):
        """
        extend the lending period for a book.
        
        args:
            borrow_id (str): id for the borrowed book.
            n_days (int): amount of days to extend the period with.
            default_message (bool): control if an error message is given.
        """
        borrow_obj = self.get_borrowed_obj(borrow_id, default_message)
        if borrow_obj is None:
            return
        
        return_date = borrow_obj.due_date
        new_date = return_date + timedelta(days=n_days)
        borrow_obj.due_date = new_date.strftime('%Y-%m-%d')
        
        borrow_obj.extentions += 1
        borrow_obj.save()

    def return_book(self, borrow_id, default_message=True):
        """
        return a borrowed book.
        
        args:
            borrow_id (str): id for the borrowed book.
            default_message (bool): control if an error message is given.
        """
        borrow_obj = self.get_borrowed_obj(borrow_id, default_message)
        if borrow_obj is None:
            return
        
        bc = BorrowedCustomer.objects.get(borrow=borrow_obj)
        bb = BorrowedBook.objects.get(borrow=borrow_obj)
        book_obj_id = bb.book.id
        
        expected_return = borrow_obj.due_date
        current_date =  date.today()
        diff_date = expected_return - current_date
        
        is_overdue = 'no'
        if diff_date.days < 0:
            is_overdue = 'yes'
        
        var = {'borrowing_id':borrow_obj.id, 'customer': bc.customer,
               'library_id': bb.book.library.library_id, 'overdue': is_overdue,
               'unique_id': bb.book.individual_id, 'isbn_13': bb.book.isbn_13, 
               'default_lending_period': borrow_obj.default_lending_period,
               'lending_date': borrow_obj.lending_date, 'book_id': book_obj_id,
               'due_date': expected_return, 'title': bb.book.title,
               'return_date': current_date, 'isbn_10': bb.book.isbn_10,
               'extentions': borrow_obj.extentions}
        
        borrow_log = BorrowingLog(**var)
        self.edit_available(bb.book)
        
        borrow_log.save()
        borrow_obj.delete()
        
    def get_borrowed_books(self, borrow_obj=None, get_table=False, 
                           write_to_file=True, default_message=True,
                           filename='active_lending_table.txt'):
        """
        makes a table with all borrowed books with their borrow_id, 
        customer_id, library_id, book_id, title, isbn_10, isbn_13, 
        default_lending_period,lending_date, due_date, extentions and overdue.
        
        args:
            borrow_obj (query_object): filtered query objects, optional.
            get_table (bool): controls if a table is printed to terminal.
            write_to_file (bool): writes to a txt file if set to True.
            default_message (bool): control if an error message is given.
            filename (str): filename for the file.
        
        returns:
            table (str): table with all borrowed books.
        """
        current_date =  date.today()
        
        if borrow_obj is None:
            borrow_obj = Borrowed.objects.all()
        
        fields = ['id', 'customer_id', 'library_id', 'book_id', 'title',
                  'isbn_10', 'isbn_13', 'default_lending_period', 
                  'lending_date', 'due_date', 'extentions', 
                  'overdue']
        try:
            borrow_obj.values()[0].keys()
        except:
            message = 'no book or books are being borrowed'
            self.print_message(message, default_message)
            return

        entries = list(borrow_obj.values_list())
        for i, j in enumerate(entries):
            entries[i] = list(j)
        
        for i, j in enumerate(borrow_obj):
            temp = []
            bc = BorrowedCustomer.objects.get(borrow=j)
            bb = BorrowedBook.objects.get(borrow=j)
            
            temp = [bc.customer.id]
            try:
                temp += [bb.book.library.library_id]
            except:
                temp += [None]
            
            temp += [bb.book.id, bb.book.title, bb.book.isbn_10, 
                     bb.book.isbn_13]
            
            date_diff = entries[i][3] - current_date  
            if date_diff.days < 0: 
                entries[i][-1] = 'yes'
                
            entries[i][1:1] = temp
        
        table = self.make_table(entries, fields)
        if get_table is not False:
            print(table)
        
        if write_to_file is True:
            with open('txt_files/' + filename, 'w') as file:
                file.write(table)
        
        return table
    
    def get_overdue(self, customer_id=None, write_to_file=True, 
                    get_table=False, default_message=True):
        """
        makes a table with only those books that are ovrdue. the table
        contains borrow_id, customer_id, library_id, book_id, title, isbn_10,
        isbn_13, default_lending_period, lending_date, due_date, extentions 
        and overdue.
        
        args:
            customer_id (str): id for a customer, optional.
            write_to_file (bool): writes to a txt file if set to True.
            get_table (bool): controls if a table is printed to terminal.
            default_message (bool): control if an error message is given.
        
        returns:
            table (str): table with all books that are overdue.
        """
        query_obj = Borrowed.objects.all()
        
        if customer_id is not None:
            customer_obj = self.get_customer_obj(customer_id, default_message)
        
            if customer_obj is None:
                return
            
            query_obj = query_obj.filter(borrowedcustomer__customer=
                                         customer_obj)
        
        borrow_obj = query_obj.filter(overdue='yes')
        table = self.get_borrowed_books(borrow_obj, get_table, write_to_file, 
                                        default_message, 'books_overdue.txt')
        return table
    
    def customer_active_overview(self, customer_id, write_to_file=True, 
                                 default_message=True, get_table=False):
        """
        makes a table with all currently borrowed books for a given customer. 
        the table contains borrow_id, customer_id, library_id, book_id, title, 
        isbn_10, isbn_13, default_lending_period, lending_date, due_date, 
        extentions and overdue.
        
        args:
            customer_id (str): id for a customer.
            write_to_file (bool): writes to a txt file if set to True.
            get_table (bool): controls if a table is printed to terminal.
            default_message (bool): control if an error message is given.
        
        returns:
            table (str): table with all books that are overdue.
        """
        customer_obj = self.get_customer_obj(customer_id, default_message)
        
        if customer_obj is None:
            return

        query_obj = Borrowed.objects.all()
        borrow_obj = query_obj.filter(borrowedcustomer__customer=customer_obj)
        
        if len(borrow_obj) == 0:
            self.print_message('No books being borrowed by this customer', 
                               default_message)
            return
        
        table = self.get_borrowed_books(borrow_obj, write_to_file=False)       
        
        if get_table is not False:
            print(table)

        if write_to_file is True:
            with open('txt_files/customer_active_overview.txt', 'w') as file:
                file.write(table)
        
        return table
    
    def customer_history_overview(self, customer_id, write_to_file=True, 
                                  default_message=True, get_table=False):
        """
        makes a table with all previously borrowed books for a given customer. 
        the table contains borrow_log_id, borrowing_id, customer_id, 
        library_id, book_id, title, isbn_10, isbn_13, unique_id, 
        default_lending_period, lending_date, due_date, return_date, 
        extentions and overdue.
        
        args:
            customer_id (str): id for a customer.
            write_to_file (bool): writes to a txt file if set to True.
            get_table (bool): controls if a table is printed to terminal.
            default_message (bool): control if an error message is given.
        
        returns:
            table (str): table with all books that are overdue.
        """
        customer_obj = self.get_customer_obj(customer_id, default_message)
        
        if customer_obj is None:
            return
        
        borrow_log = BorrowingLog.objects.filter(customer_id=customer_obj)
        
        if len(borrow_log) == 0:
            self.print_message('No history found for this customer', 
                               default_message)
            return
        
        filename = 'customer_history_overview.txt'
        table = self.log_overview(borrow_log, write_to_file, False, 
                                  default_message, filename)
        
        if get_table is not False:
            print(table)

        return table
        
    def customer_full_overview(self, customer_id, get_table=False,
                               write_to_file=True, default_message=True):
        """
        makes a table with all currently and previously borrowed books for a 
        given customer, including a table containing only those books that are
        overdue.
        
        args:
            customer_id (str): id for a customer.
            write_to_file (bool): writes to a txt file if set to True.
            get_table (bool): controls if a table is printed to terminal.
            default_message (bool): control if an error message is given.
        
        returns:
            table (str): table with all books that are overdue.
        """
        history_table = self.customer_history_overview(customer_id, 0, 0)
        active_table = self.customer_active_overview(customer_id, 0, 0)
        overdue = self.get_overdue(customer_id, 0, False, 0)
        
        data = [overdue, active_table, history_table]
        replace = {None: '\tNo records to display'}.get
        data = list(map(replace, data, data))
        data = np.array(data, dtype=str)

        table_list = np.array(['Overdue:\n', '\n\nBooks currently borrowed:\n', 
                               '\n\nBooks previously borrowed:\n'], dtype=str)
        
        table = ''.join(np.char.add(table_list, data))
        
        if get_table is not False:
            print(table)

        if write_to_file is True:
            with open('txt_files/customer_full_overview.txt', 'w') as file:
                file.write(table)

    def log_overview(self, borrow_log=None, write_to_file=True, 
                     get_table=False, default_message=True,
                     filename='general_borrowing_log.txt'):
        """        
        makes a table with all previously borrowed books. the table contains
        borrow_log_id, borrowing_id, customer_id, library_id, book_id, title,
        isbn_10, isbn_13, unique_id, default_lending_period, lending_date,
        due_date, return_date, extentions and overdue.
        
        args:
            borrow_log (query_object): filtered query objects, optional.
            get_table (bool): controls if a table is printed to terminal.
            write_to_file (bool): writes to a txt file if set to True.
            default_message (bool): control if an error message is given.
            filename (str): filename for the file.
        
        returns:
            table (str): table with all borrowed books.
        """
        if borrow_log is None:
            borrow_log = BorrowingLog.objects.all()
        
        try:
            fields = list(borrow_log.values()[0].keys())
        except:
            self.print_message('no history to show', default_message)
            return
        
        entries = list(borrow_log.values_list())
        
        for i, j in enumerate(entries):
            entries[i] = list(j)
        
        table = self.make_table(entries, fields)
        if get_table is not False:
            print(table)

        if write_to_file is True:
            with open('txt_files/' + filename, 'w') as file:
                file.write(table)
                
        return table

    def delete_borrowing_obj(self, borrow_id, customer_id):
        """
        delete a borrowed object.
        
        args:
            borrow_id (str): id for the borrowed book object.
            customer_id (str): id of a customer.
        """
        objects_tuple = self.borrow_customer_id(borrow_id, customer_id)
        
        if objects_tuple is None:
            return
        
        borrow_obj, customer_obj = objects_tuple
        bc_obj = BorrowedCustomer.objects.filter(customer=customer_obj, 
                                                 borrow=borrow_obj)   
        if len(bc_obj) != 0:
            bb = BorrowedBook.objects.get(borrow=borrow_obj)
            
            if bb.book.available == 'no':
                self.edit_available(bb.book)
                
            borrow_obj.delete()
        


