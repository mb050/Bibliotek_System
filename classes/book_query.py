from bibliotek.models import BookCategory
from bibliotek.models import BookAuthor
from bibliotek.models import Category
from bibliotek.models import Author
from bibliotek.models import Book
from classes.base import Base

from sys import exit

class Book_query(Base):
    """
    containts queries related to books.
    
    methods:
        check_category: checks if a category exist.
        add_book: register new book.
        dict_object: makes default dict used for lookup_book.
        update_all_individual_id: updates individual id.
        add_individual_id: add individual id.
        book_catalog: get table of all books.
        lookup_book: search for a book.
        edit_title: edit title.
        edit_publication_date: edit publication date.
        edit_category: edit categories asscociated to a given book.
        edit_author: edit author asscociated to a given book.
        edit_isbn_10: edit isbn_10
        edit_isbn_13: edit isbn_13.
        edit_library: edit library association.
        edit_individual_id: edit individual id.
        edit_available: edit availability.
        edit_conditions: method for deciding which field to edit.
        edit_book: initiates the editing of book fields.
    """
    
    def check_category(self, category, save_category=False):
        """
        check if a category exist.
        
        args:
            category (str): name of category.
            save_category (bool): will register the category if it does not
                                  exist.
        returns:
            None (bool) or (query object)
        """
        category = category.lower().capitalize()
        
        if save_category is False:
            categories = list(Category.objects.all().values_list())
            for i, j in enumerate(categories):
                categories[i] = j[1]
            
            if category in categories:
                return Category.objects.get(name=category)
        else:
            try:
                new_category = Category(name=category)
                new_category.save()
            except:
                pass

    def add_book(self, title, publish_date=None, book_category='', 
                 author_name='', isbn_10=None, isbn_13=None, library_id=None, 
                 Individual_id=1):
        """
        register new book.
        
        args:
            title (str): title of the book. 
            publish_date (date): optional.
            book_category (str): optional. 
            author_name (str): optional.
            isbn_10 (str): optional.
            isbn_13 (str): optional.
            library_id (str): optional. 
            Individual_id (int): optional.
        """
        new_book = Book(title=title, publication_date=publish_date, 
                        isbn_10=isbn_10, isbn_13=isbn_13, 
                        individual_id=Individual_id, available='yes')
        new_book.save()
        
        book_category = book_category.lower().capitalize()
        if book_category != '':
            self.check_category(book_category, True)
            book_category = Category.objects.filter(name=book_category)[0]
            BookCategory(book=new_book, category=book_category).save()
        
        author_name = author_name.lower()
        if author_name != '':
            author_obj = self.check_author(author_name)
            
            if author_obj is not None:
                BookAuthor(author=author_obj, book=new_book).save()
        
        if library_id is not None:
            library_id = str(library_id).lower()
            library_obj = self.check_library_id(library_id)
            
            if library_obj is not None:
                new_book.library = library_obj
                new_book.save()
        
        new_book.available = 'yes'
        new_book.save()
        
        self.add_individual_id(new_book)
        return
    
    def dict_object(self, query_obj, include_none=True):
        """
        default dict object used for lookup_book.
        
        args:
            query_obj (query object): query object of book.
            include_none (bool): will remove None if set to False.
        
        returns:
            (query_object)
        """
        filter_dict = {'title': query_obj.title, 
                       'isbn_10': query_obj.isbn_10, 
                       'isbn_13': query_obj.isbn_13,
                       'library_id': query_obj.library_id}
        
        if include_none is True:
            return filter_dict
        else:
            return self.remove_empty_values(filter_dict)
            
    
    def update_all_individual_id(self, query_obj, include_none=True):
        """
        updates all individual id.
        
        args:
            query_obj (query object): query object of book.
            include_none (bool): will remove None if set to False.
        """
        filter_dict = self.dict_object(query_obj, include_none)
        search_obj = Book.objects.all().filter(**filter_dict)
        
        for i, j in enumerate(search_obj):
            j.individual_id = i + 1
            j.save()

    
    def add_individual_id(self, query_obj, include_none=True):
        """
        add individual id to a book.
        
        args:
            query_obj (query object): query object of book.
            include_none (bool): will remove None if set to False.
        """
        filter_dict = self.dict_object(query_obj, include_none)
        search_obj = Book.objects.all().filter(**filter_dict)
        n = len(search_obj)
            
        if n == 1:
            query_obj.individual_id = 1
        elif n > 0:
            id_list = list(search_obj.values_list('individual_id'))
            
            for i, j in enumerate(id_list):
                try:
                    id_list[i] = int(j[0])
                except:
                    id_list[i] = 1
                
            query_obj.individual_id = max(id_list) + 1            

        query_obj.save()
        return
        
    def book_catalog(self, query_object=None, get_table=False, 
                     write_to_file=True, filename='book_table.txt'):
        """
        makes a table of all books with their id, title, publication_date, 
        category, author, isbn_10, isbn_13, library_id, individual_id and 
        available.
        
        args:
            query_obj (query_object): filtered query objects, optional.
            get_table (bool): controls if a table is printed to terminal.
            write_to_file (bool): writes to a txt file if set to True.
            filename (str): filename for the file.
        """
        if query_object is None:
            book = Book.objects.all()
        else:
            book = query_object
        
        try:
            fields = list(book.values()[0].keys())
        except:
            print('no registered books')
            return

        fields.insert(3, 'author')
        fields.insert(3, 'category')
        
        entries = [list(i) for i in book.values_list()]
        for k, i in enumerate(book):
            author = Author.objects.filter(bookauthor__book=i)
            category = Category.objects.filter(bookcategory__book=i)
            
            author_list = [j.name for j in author]
            category_list = [j.name for j in category]
            
            entries[k].insert(3, ', '.join(author_list))
            entries[k].insert(3, ', '.join(category_list))
        
        table = self.make_table(entries, fields)
        if get_table is not False:
            print(table)
        
        if write_to_file is True:
            with open('txt_files/' + filename, 'w') as file:
                file.write(table)

    def lookup_book(self, title='', isbn_10='', isbn_13='', library_id='',
                    author_name='', category_name='', get_table=False):
        """
        search for books given the title, isbn_10, isbn_13, library_id, and or
        author_name. The result as a table either in a file or in the terminal. 
        variables used for the search can be any number of them.
        
        args:
            title (str): title of the book.
            isbn_10 (str): isbn_10 of the book.
            isbn_13 (str): isbn_10 of the book.
            library_id (str): library id.
            author_name (str): name of an author.
            category_name (str): name of a category/genre.
            get_table (bool): controls if a table is printed to terminal.
        """
        function_argument = locals()
        function_argument.pop('self')
        function_argument.pop('get_table')
        
        book_obj = self.search_book(**function_argument)
        self.book_catalog(book_obj, filename='book_search.txt')
            
        if book_obj is None:
            print('no book or books found')
        else:
            self.book_catalog(book_obj, get_table, filename='book_search.txt')

    # =========================================================================
    
    def edit_title(self, book_obj, new_title, edit=True):
        """
        edit name for a given book.
        
        args:
            book_obj (query_object): query object to be edited.
            title (str): new title.
            edit (bool): controls if field is edited or set to None.
        """
        if edit is True:
            book_obj.title = new_title
        else:
            book_obj.title = None
        
        book_obj.save()
        self.update_all_individual_id(book_obj)

    def edit_publication_date(self, book_obj, new_date, edit=True):
        """
        edit the publication date for a given book.
        
        args:
            book_obj (query_object): query object to be edited.
            new_date (date): new publication date.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            try:
                book_obj.publication_date = new_date
            except:
                print('given date was not correctly formatted')
        else:
            book_obj.publication_date = None
        
        book_obj.save()

    def edit_category(self, book_obj, category_name, new_category='', 
                      remove=False,  change=False, del_all=False):
        """
        edit the categories for a given book. 
        if remove, change, del_all are all set to False, then a new category 
        will be added.
        
        args:
            book_obj (query_object): query object to be edited.
            category_name (str): category to edit, either removed or changed.
            new_category (str): category to be added.
            remove (bool): remove the name of a given category.
            change (bool): change the name of a given category.
            del_all (bool): removes all categories for the given book if True.
        """
        category_name = category_name.lower().capitalize()
        new_category = new_category.lower().capitalize()
        
        if True not in [remove, change, del_all]:
            book_categories = list(BookCategory.objects.filter(book=book_obj))
            
            for i, j in enumerate(book_categories):
                book_categories[i] = j.category.name

            if category_name not in book_categories:
                self.check_category(category_name, True)
                category_obj = Category.objects.get(name=category_name)
                BookCategory(category=category_obj, book=book_obj).save()
        
        elif change is True and new_category != '':
            old_category = self.check_category(category_name)
            bk_category = BookCategory.objects.all()
            bk_category = bk_category.get(category=old_category, book=book_obj)

            new_category = self.check_category(new_category)
            if new_category is not None:
                bk_category.category = new_category
                bk_category.save()
        
        elif remove is True:
            old_category = self.check_category(category_name)
            bk_category = BookCategory.objects.all()
            bk_category = bk_category.get(category=old_category, book=book_obj)
            bk_category.delete()
        
        elif del_all is True:
            book_category = BookCategory.objects.all().filter(book=book_obj)
            for i in book_category:
                i.delete()

    def edit_author(self, book_obj, author_name, new_name='', remove=False, 
                    change=False, del_all=False):
        """
        edit the authors for a given book. if remove, change, del_all are all
        set to False, then a new author will be added.
        
        args:
            book_obj (query_object): query object to be edited.
            author_name (str): author to edit, either removed or changed.
            new_name (str): author to be added.
            remove (bool): remove the name of a given author.
            change (bool): change the name of a given author.
            del_all (bool): removes all authors for the given book if True.
        """
        new_name = self.check_author(new_name.lower())
    
        if True not in [remove, change, del_all]:
            book_author = list(BookAuthor.objects.filter(book=book_obj))
            for i, j in enumerate(book_author):
                book_author[i] = j.author
            
            author_obj = self.check_author(author_name)
            if author_obj not in book_author:
                BookAuthor(author=author_obj, book=book_obj).save()
                
        elif change is True and new_name != '':
            old_name = self.check_author(author_name)
            book_author = BookAuthor.objects.all()
            book_author = book_author.get(author=old_name, book=book_obj)
            book_author.author = new_name
            book_author.save()
        
        elif remove is True:
            author_obj = self.check_author(author_name)
            book_author = BookAuthor.objects.all()
            Book_author = book_author.filter(author=author_obj, book=book_obj)
            Book_author.delete()
        
        elif del_all is True:
            book_author = BookAuthor.objects.all().filter(book=book_obj)
            for i in book_author:
                i.delete()

    def edit_isbn_10(self, book_obj, new_isbn, edit=True):
        """
        edit the isbn_10 for a given given book.
        
        args:
            book_obj (query_object): query object to be edited.
            new_isbn (str): new isbn_10 number.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True and len(new_isbn) == 10:
            book_obj.isbn_10 = new_isbn
        elif edit is not True:
            book_obj.isbn_10 = None
        
        book_obj.save()
        self.update_all_individual_id(book_obj)
        
    def edit_isbn_13(self, book_obj, new_isbn, edit=True):
        """
        edit the isbn_13 for a given given book.
        
        args:
            book_obj (query_object): query object to be edited.
            new_isbn (str): new isbn_13 number.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True and len(new_isbn) == 13:
            book_obj.isbn_13 = new_isbn
        elif edit is not True:
            book_obj.isbn_13 = None
        
        book_obj.save()
        self.update_all_individual_id(book_obj)

    def edit_library(self, book_obj, Library_id, edit=True):
        """
        edit which library a given book is located at.
        
        args:
            book_obj (query_object): query object to be edited.
            Library_id (str): id of the new library.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            library_obj = self.check_library_id(Library_id)
            
            if library_obj is not None:
                book_obj.library = library_obj
        else:
            book_obj.library = None
        
        book_obj.save()
        self.update_all_individual_id(book_obj)
        
    def edit_individual_id(self, book_obj, new_id, edit=True):
        """
        edit individual id for a given given book.
        
        args:
            book_obj (query_object): query object to be edited.
            new_id (str): new individual id.
            edit (bool): controls if the field is edited or set to None.
        """
        self.update_all_individual_id(book_obj)
        
        if edit is True:
            book_obj.individual_id = new_id
        else:
            book_obj.individual_id = None
        
        book_obj.save()
    
    def edit_available(self, book_obj):
        """
        edit availability for a given given book.
        
        args:
            book_obj (query_object): query object to be edited.
        """
        if book_obj.available == 'yes':
            book_obj.available = 'no'
        else:
            book_obj.available = 'yes'
        
        book_obj.save()

    def edit_conditions(self, book_obj, input_str):
        """
        method that controls which field to edit.
        
        args:
            book_obj (query_object): query object to be edited.
            input_str (str): which field to edit.
        
        returns:
            (bool): False, if given input_str does not match with a field.
        """
        if input_str[:1] == 't' or input_str == 'title':
            self.str_shortcut('Enter new title')
            new_title = input()
            
            arg = self.default_argument_message()
            self.edit_title(book_obj, new_title, arg)
        
        elif input_str[:1] == 'p' or input_str == 'publication_date':
            self.str_shortcut('Enter new publication_date')
            new_date = input()
            
            arg = self.default_argument_message()
            self.edit_publication_date(book_obj, new_date, arg)
        
        elif input_str[:1] == 'c' or input_str == 'category':
            self.str_shortcut('Enter category')
            category = input()
            
            self.str_shortcut('Type "remove", "change", or "del_all"')
            arg = self.check_expanded_args(input().lower(), 'new_category')
            self.edit_category(book_obj, category, *arg)
            
        elif input_str[:2] == 'au' or input_str == 'author':
            self.str_shortcut('Enter author_name')
            author = input()
            
            self.str_shortcut('Type "remove", "change", or "del_all"')
            arg = self.check_expanded_args(input().lower(), 'new_author')
            self.edit_author(book_obj, author, *arg)
            
        elif input_str == 'isbn_10':
            self.str_shortcut('Enter new isbn_10')
            new_isbn_10 = input()
            
            arg = self.default_argument_message()
            self.edit_isbn_10(book_obj, new_isbn_10, arg)
            
        elif input_str == 'isbn_13':
            self.str_shortcut('Enter new isbn_13')
            new_isbn_13 = input()
            
            arg = self.default_argument_message()
            self.edit_isbn_13(book_obj, new_isbn_13, arg)
            
        elif input_str[:1] == 'l' or input_str == 'library_id':
            self.str_shortcut('Enter new library_id')
            new_library = input()
            
            arg = self.default_argument_message()
            self.edit_library(book_obj, new_library, arg)
            
        elif input_str[:2] == 'in' or input_str == 'individual_id':
            self.str_shortcut('Enter new individual_id')
            new_individual_id = input()
            
            arg = self.default_argument_message()
            self.edit_individual_id(book_obj, new_individual_id, arg)
            
        elif input_str[:2] == 'av' or input_str == 'available':
            self.edit_available(book_obj)
        else:
            return False
        
    def edit_book(self, book_id):
        """
        initiate editing of the fields for a given book.
        
        args:
            book_obj (query_object): query object to be edited.
        """
        try:
            book = Book.objects.get(id=book_id)
        except:
            print('no book or books with that id')
            return
        
        data = self.read_help_file('edit_menu.json')
        text, help_str = self.support_text('book', data)
        title, invalid, input_message = text[:3]
        command_str, overview, option = text[3:]
        
        run_loop = True
        was_invalid = False
        while run_loop is True:
            if was_invalid is not True:
                print(input_message, end=' ')
            else:
                was_invalid = False
            
            input_str = input().lower()
            
            if input_str in ['', 'stop', 'break', 'cancel', 'back']:
                break
            elif input_str in ['q', 'quit']:
                exit()
            elif input_str == 'option':
                print(option)
                continue
            elif input_str == 'lookup':
                self.book_catalog(Book.objects.all().filter(id=book_id), True)
                continue
            elif input_str == 'delete':
                book.delete()
                break
            
            if self.edit_conditions(book, input_str) is None:
                continue
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
        
        self.make_title('main/book')
        

        