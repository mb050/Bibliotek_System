from classes.borrowing_query import Borrowing_query
from classes.category_query import Category_query
from classes.customer_query import Customer_query
from classes.library_query import Library_query
from classes.author_query import Author_query
from classes.book_query import Book_query
from classes.analytic import Analytic

from sys import exit

class Interface_Methods():
    """
    contains all methods for the interface.
    
    methods:
        category_menu: menu for category.
        library_menu: menu for library.
        book_menu: menu for book.
        author_menu: menu for author.
        customer_menu: menu for customer.
        borrowing_menu: menu for borrowing.
        analytic_menu: menu for analytic.
        book_serach: sub menu for book search.
        lending_functions: sub menu for lending functions.
        borrow_overview_menu: sub menu for borrowing overview.
        customer_history_menu: sub menu for customer borrowing overview.
        author_publication_sub_menu: sub menu for author publication.
    """
    
    def category_menu(self, input_str):
        """
        interface method for category.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        class_obj = Category_query()
        
        if input_str[:1] == 'a' or input_str == 'add':
            self.str_shortcut('Enter category name')
            class_obj.add_category(input())
        
        elif input_str[:1] == 'o' or input_str == 'overview':
            self.str_shortcut('Get table, type "yes" or "no"')
            get_table = self.request_yes_no(input())    
            class_obj.category_table(get_table)
        
        elif input_str[:1] == 'e' or input_str == 'edit':
            self.str_shortcut('Enter category name or id')
            class_obj.edit_category(input())
        else:
            return False

    def library_menu(self, input_str):
        """
        interface method for library.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        class_obj = Library_query()
        
        if input_str[:1] == 'a' or input_str == 'add':
            self.str_shortcut('Enter library_id')
            library_id = input()
            
            self.str_shortcut('Enter a library_name')
            name = input()
            
            self.str_shortcut('Enter an address')
            address = input()
            
            self.str_shortcut('Enter contact_information')
            contact_info = input()

            class_obj.add_library(library_id, name, address, contact_info)
        
        elif input_str[:1] == 'o' or input_str == 'overview':
            self.str_shortcut('Get table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            class_obj.overview(get_table)
        
        elif input_str[:1] == 'e' or input_str == 'edit':
            self.str_shortcut('Enter a library_id')
            class_obj.edit_library(input())
        
        elif input_str[:1] == 'l' or input_str == 'lookup_books':
            self.str_shortcut('Get table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            self.str_shortcut('Enter a library_id')
            class_obj.lookup_books(input(), get_table)        
        else:
            return False

    def book_menu(self, input_str):
        """
        interface method for books.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        class_obj = Book_query()
        
        if input_str[:1] == 'a' or input_str == 'add':
            self.str_shortcut('Enter a title')
            title = input()
            
            date_message = 'Enter publish date in the format year-month-day'
            self.str_shortcut(date_message)
            publish_date = self.check_date(input())
            
            self.str_shortcut('Enter book category')
            book_category = input()
            
            self.str_shortcut('Enter author_name')
            author_name = input()
            
            self.str_shortcut('Enter isbn_10, can be left empty or '
                              'must be 10 characters long')
            isbn_10 = self.check_lenght(input(), 10)
            
            self.str_shortcut('Enter isbn_13, can be left empty or '
                              'must be 13 characters long')
            isbn_13 = self.check_lenght(input(), 13)
            
            self.str_shortcut('Enter library_id')
            library_id = input()
            
            if library_id == '':
                library_id = None

            class_obj.add_book(title, publish_date, book_category, author_name, 
                               isbn_10, isbn_13, library_id)
        
        elif input_str[:1] == 'o' or input_str == 'overview':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            self.str_shortcut('Write_to_file, type "yes" or "no"')
            write_to_file = self.request_yes_no(input())
            
            if write_to_file is True:
                default = 'book_table.txt'
                
                self.str_shortcut('Change filename book_table.txt, type '
                                  '"yes" or "no"')
                custom_name = self.request_yes_no(input())
                filename = self.set_filename(custom_name, default)

            class_obj.book_catalog(None, get_table, write_to_file, filename)
        
        elif input_str[:1] == 'e' or input_str == 'edit':
            self.str_shortcut('Enter book_id')
            class_obj.edit_book(input())
        
        elif input_str[:1] == 's' or input_str == 'search_books':
            self.book_serach()
        else:
            return False
    
    def author_menu(self, input_str):
        """
        interface method for authors.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        class_obj = Author_query()
        
        if input_str[:1] == 'a' or input_str == 'add':
            self.str_shortcut('Enter author_name')
            name = input()
            
            self.str_shortcut('Enter nationality')
            nationality = input().lower().capitalize()
            
            self.str_shortcut('Enter birthdate in the format year-month-day')
            birthdate = self.check_date(input())
            
            class_obj.add_author(name, nationality, birthdate)
        
        elif input_str[:1] == 'o' or input_str == 'overview':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            class_obj.get_overview(get_table)
        
        elif input_str[:1] == 'e' or input_str == 'edit':
            self.str_shortcut('Enter author_id')
            class_obj.edit_author(input())
        
        elif input_str[:1] == 'p' or input_str == 'publications':
            self.author_publication_sub_menu(class_obj)
        else:
            return False
 
    def customer_menu(self, input_str):
        """
        interface method for customers.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        borrow_obj = Borrowing_query()
        class_obj = Customer_query()
        
        if input_str[:1] == 'a' or input_str == 'add':
            self.str_shortcut('Enter a name')
            name = input().lower()
            
            self.str_shortcut('Enter an address')
            address = input().lower()
            
            if address == '':
                address = None
                
            self.str_shortcut('Enter contact_information')
            contact_info = input()
            
            if contact_info == '':
                contact_info = None
            
            self.str_shortcut('Use current date as signup date, '
                              'type "yes" or "no"')
            default_date = self.request_yes_no(input())
            
            if default_date is False:
                self.str_shortcut('Enter date in the format year-month-day')
                signup_date = self.check_date(input())
            else:
                signup_date = None
                
            class_obj.add_customer(name, address, contact_info, signup_date)
        
        elif input_str[:1] == 'o' or input_str == 'overview':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            class_obj.get_overview(get_table=get_table)
        
        elif input_str[:1] == 'e' or input_str == 'edit':
            self.str_shortcut('Enter customer_id')
            class_obj.edit_category(input())
        
        elif input_str[:1] == 's' or input_str == 'search':
            self.str_shortcut('Search by using customer_id or customer_name.'
                              '\nType "id" or "name"')
            
            if input().lower()[:1] == 'i':
                self.str_shortcut('Enter customer_id')
                variable = [input(), '']
            else:
                self.str_shortcut('Enter customer_name')
                variable = ['', input()]
            
            class_obj.search_customer(*variable)
        
        elif self.lending_functions(borrow_obj, input_str) is None:
            return
        
        elif input_str[:1] == 'h' or input_str == 'history':
            self.str_shortcut('Enter customer_id')
            customer_id = input()
            
            self.customer_history_menu(customer_id, borrow_obj)
        
        elif input_str[:1] == 'b' or input_str == 'book_search':
            self.book_serach()
        else:
            return False

    def borrowing_menu(self, input_str):
        """
        interface method for borrowing.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        borrow_obj = Borrowing_query()
        
        if input_str[:1] == 'o' or input_str == 'overview':
            self.borrow_overview_menu(borrow_obj)
        elif self.lending_functions(borrow_obj, input_str) is None:
            return
        elif input_str[:1] == 'c' or input_str == 'customer_related':
            self.str_shortcut('Enter customer_id')
            customer_id = input()
            
            self.customer_history_menu(customer_id, borrow_obj)
        elif input_str[:1] == 'd' or input_str == 'delete':
            self.str_shortcut('Enter borrow_id')
            borrow_id = input()
            
            self.str_shortcut('Enter customer_id')
            customer_id = input()
            
            borrow_obj.delete_borrowing_obj(borrow_id, customer_id)
        elif input_str[:1] == 'b' or input_str == 'book_search':
            self.book_serach()
        else:
            return False

    def analytic_menu(self, input_str):
        """
        interface method for analytics.
        
        args:
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        class_obj = Analytic()
        
        if input_str[0] == 'g' or input_str == 'general':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            class_obj.generic_overview(get_table)
       
        elif input_str[0] == 'b' or input_str == 'book':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            class_obj.book_analytic(get_table)
        
        elif input_str[0] == 'a' or input_str == 'author':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            class_obj.generic_query_analytic(get_table=get_table)
        
        elif input_str[0] == 'c' or input_str == 'category':
            self.str_shortcut('Get_table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            class_obj.generic_query_analytic('category', get_table)
        else:
            return False
    
    def book_serach(self):
        """
        interface method for book search.
        """
        self.str_shortcut('Enter a title')
        title = input()
        
        self.str_shortcut('Enter author_name')
        author_name = input()
        
        self.str_shortcut('Enter isbn 10, can be left empty or '
                          'must be 10 characters long')
        isbn_10 = self.check_lenght(input(), 10, '')
        
        self.str_shortcut('Enter isbn 13, can be left empty or '
                          'must be 13 characters long')
        isbn_13 = self.check_lenght(input(), 13, '')
        
        self.str_shortcut('Enter library_id')
        library_id = input()
        
        self.str_shortcut('Enter category_name')
        category_name = input()
        
        self.str_shortcut('Get table, type "yes" or "no"')
        get_table = self.request_yes_no(input())
        
        Book_query().lookup_book(title, isbn_10, isbn_13, library_id, 
                                 author_name, category_name, get_table)
            
    def lending_functions(self, class_obj, input_str):
        """
        interface method for lending functions.
        
        args:
            class_obj (class object): which class is used.
            input_str (str): input that decide which function in the menu to
                             use.
        returns:
            False (bool) or None (bool)
        """
        if input_str[:1] == 'l' or input_str == 'lend_book':
            self.str_shortcut('Enter book_id')
            book_id = input()
            
            self.str_shortcut('Enter customer_id')
            customer_id = input()
            
            class_obj.lend_book(book_id, customer_id)
            
        elif input_str[:1] == 'r' or input_str == 'return_book':
            self.str_shortcut('Enter borrow_id')
            borrow_id = input()
            
            class_obj.return_book(borrow_id)
            
        elif input_str[:1] == 'p' or input_str == 'prolong_period':
            self.str_shortcut('Enter borrow_id')
            borrow_id = input()
            
            message = str('\nSelect amount of days to extend the loaning '
                          'period:\n>')
            n_days = self.request_number(message, 7)
            
            class_obj.extend_lending(borrow_id, n_days)
        else:
            return False
    
    def borrow_overview_menu(self, class_obj):
        """
        interface method for lending functions.
        
        args:
            class_obj (class object): which class is used.
        """
        
        self.str_shortcut('general -> general overview.\n'
                          'overdue -> overdue books.\n'
                          'history -> previousely borrowed books.\n\n'
                          'Type "general", "overdue" or "history"')
       
        input_str = input().lower()
        
        if input_str[:1] == 'g' or input_str == 'general':
            self.str_shortcut('Get table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            class_obj.get_borrowed_books(get_table=get_table)
        
        elif input_str[:1] == 'o' or input_str == 'overdue':
            self.str_shortcut('Get table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            class_obj.get_overdue(get_table=get_table)
        
        elif input_str[:1] == 'h' or input_str == 'history':
            self.str_shortcut('Get table, type "yes" or "no"')
            get_table = self.request_yes_no(input())
            
            class_obj.log_overview(get_table=get_table)

    def customer_history_menu(self, customer_id, class_obj):
        """
        interface method for borrowing overviews related to a given customer.
        
        args:
            customer_id (str): id for a customer.
            class_obj (class object): which class is used.
        """
        text, help_str = self.support_text('customer_history_menu')
        title, invalid, input_message = text[:3]
        command_str, overview, option = text[3:]

        run_loop = True
        was_invalid = False
        while run_loop is True:
            if was_invalid is not True:
                print(input_message, end=' ')
            else:
                was_invalid = False
            
            user_input = input().lower()
            
            if user_input in ['', 'stop', 'break', 'cancel']:
                break
            elif user_input in ['q', 'quit']:
                exit()
            elif user_input == 'help':
                print(help_str)
                continue
            elif user_input == 'option':
                print(option)
                continue
            
            if user_input[:1] in ['a', 'f'] or user_input in ['all', 'full']:
                self.str_shortcut('Get table, type "yes" or "no"')
                get_table = self.request_yes_no(input())
                class_obj.customer_full_overview(customer_id, get_table)
                break
            
            elif user_input[:1] == 'o' or user_input == 'overdue':
                self.str_shortcut('Get table, type "yes" or "no"')
                get_table = self.request_yes_no(input())
                class_obj.get_overdue(customer_id, get_table=get_table)
                break
            
            elif user_input[:1] == 'c' or user_input == 'currently_borrowed':
                self.str_shortcut('Get table, type "yes" or "no"')
                get_table = self.request_yes_no(input())
                class_obj.customer_active_overview(customer_id, 
                                                   get_table=get_table)
                break
            
            elif user_input[:1] == 'h' or user_input == 'history':
                self.str_shortcut('Get table, type "yes" or "no"')
                get_table = self.request_yes_no(input())
                class_obj.customer_history_overview(customer_id, 
                                                    get_table=get_table)
                break
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
            
    def author_publication_sub_menu(self, class_obj):
        """
        interface method for author publication.
        
        args:
            class_obj (class object): which class is used.
        """
        self.str_shortcut('Do you want publicated books for all authors or'
                          'for a single author.\nType "all" or "single"')
        
        if input().lower()[:1] == 'a':
            self.str_shortcut('Display horizontal, type "yes" or "no"')
            display_horizontal = self.request_yes_no(input())
            class_obj.all_publications(display_horizontal)
        else:
            self.str_shortcut('Search by using author_id or author_name.'
                              '\nType "id" or "name"')
            
            if input().lower()[:1] == 'i':
                self.str_shortcut('Enter author_id')
                variable = [input(), '']
            else:
                self.str_shortcut('Enter author_name')
                variable = ['', input()]
            
            class_obj.author_publication(*variable)

