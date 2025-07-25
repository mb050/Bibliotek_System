from bibliotek.models import BookAuthor
from bibliotek.models import Author
from bibliotek.models import Book
from classes.base import Base

from sys import exit

class Author_query(Base):
    """
    containts queries related to authors.
    
    methods:
        check_book_id: check if book id exist.
        add_author: register new author.
        get_overview: get a table of all authors.
        author_publication: get all books a given author have written.
        horizontal: horizontal display.
        vertical: vertical display.
        all_publications: get all the publications.
        edit_name: edit date.
        edit_birthdate: edit birthdate.
        edit_nationality: edit nationality.
        edit_publication: edit the publications.
        edit_conditions: method for deciding which field to edit.
        edit_author: initiates the editing of book fields.
    """
    
    def check_book_id(self, book_id):
        """
        check if a given book id exist.
        
        args:
            book_id (str): book id.
        
        returns:
            book (query objects) or None.
        """
        try:
            book = Book.objects.get(id=book_id)
        except:
            print(f'no book with the id: {book_id}')
        else:
            return book
    
    def add_author(self, name, nationality, birthdate):
        """
        register new author.
        
        args:
            name (str): name.
            nationality (str): nationality of the author.
            birthdate (date): birthdate of the author.
        """
        author = Author(name=name, nationality=nationality, 
                        birthdate=birthdate)
        author.save()
    
    def get_overview(self, get_table=False):
        """
        get table of all authors and their id, name, nationality and birthdate.
        
        args:
            get_table (bool): controls if a table is printed to terminal
        """
        author = Author.objects.all()
        
        try:
            fields = list(author.values()[0].keys())
        except:
            print('no authors')
            return
        
        entries = [list(i) for i in author.values_list()]
        
        table = self.make_table(entries, fields)
        if get_table is not False:
            print(table)
        return
    
    def author_publication(self, author_id='', name=''):
        """
        get all books a given author have written, given either their id or 
        name.
        
        args:
            author_id (str): id of author.
            name (str): name of author.
        """
        if author_id != '':
            try:
                author_obj = Author.objects.get(id=author_id)
            except:
                author_obj = None

        elif name != '':
            author_obj = self.check_author(name.lower())
            
        if author_obj is None:
            return
        
        book = Book.objects.filter(bookauthor__author=author_obj)
        print(f'\nAuthor:\n\t{author_obj.name}\nPublication:')
        
        for i in book:
            print(f'\t{i.title}')
        
        return

    def horizontal(self, n_author, book_list, name_list):
        """
        aranges for a horizontal display for all books for all authors.
        
        args:
            n_author (int): amount of authors.
            book_list (list of query objects): list with book objects.
            name_list (list): list with author names.
            
        returns.
            publications (nested list): list with authors and their books.
        """
        publication = [''] * n_author
        for idx, i in enumerate(publication):
            temp = [j.title for j in book_list[idx]]
            publication[idx] = [name_list[idx], ', '.join(temp)]
            
        return publication

    def vertical(self, n_author, longest, book_list):
        """
        aranges for a vertical display for all books for all authors.
        
        args:
            n_author (int): amount of authors.
            longest (int): greatest amounts of books written by one author.
            book_list (list of query objects): list with book objects.
        
        returns.
            publications (nested list): list with authors and their books.
        """
        publication = [''] * longest
        
        for i in range(longest):
            publication[i] = [None] * n_author
        
        for idx, i in enumerate(book_list):
            for j, k in enumerate(i):
                publication[j][idx] = k.title
        
        return publication

    def all_publications(self, author_horizontal=True):
        """
        get a table with authors and all books written by each.
        
        args:
            author_horizontal (bool): wether to use horizontal display or
                                      vertical.
        """
        author = Author.objects.all()
        n_author = len(author)
        lengths = []
        
        book_list = []
        name_list = []
        for i in author:
            name_list.append(i.name)
            book = Book.objects.filter(bookauthor__author=i)
            book_list.append(book)
        
        for i in book_list:
            lengths.append(len(i)) 
        
        longest = max(lengths)

        if author_horizontal is True:
            publication = self.horizontal(n_author, book_list, name_list)            
            author = ['author_name', 'publications']
        else:
            publication = self.vertical(n_author, longest, book_list)
        
        table = self.make_table(publication, author)
        print(table)

    # =========================================================================

    def edit_name(self, author_obj, new_name, edit=True):
        """
        edit name for a given author.
        
        args:
            author_obj (query_object): query object to be edited.
            new_name (str): new name.
            edit (bool): controls if field is edited or set to None.
        """
        if edit is True:
            author_obj.name = new_name
        else:
            author_obj.name = None
        
        author_obj.save()

    def edit_birthdate(self, author_obj, new_date, edit=True):
        """
        edit birthdate for a given author.
        
        args:
            author (query_object): query object to be edited.
            new_date (date): new birthdate.
            edit (bool): controls if field is edited or set to None.
        """
        if edit is True:
            try:
                author_obj.birthdate = new_date
            except:
                print('given date was not correctly formatted')
        else:
            author_obj.birthdate = None
        
        author_obj.save()

    def edit_nationality(self, author_obj, new_nationality, edit=True):
        """
        edit nationality for a given author.
        
        args:
            author (query_object): query object to be edited.
            new_nationality (str): new nationality.
            edit (bool): controls if field is edited or set to None.
        """
        if edit is True:
            author_obj.nationality = new_nationality
        else:
            author_obj.nationality = None
        
        author_obj.save()

    def edit_publication(self, author_obj, book_id, new_book_id='',
                         remove=False,  change=False, del_all=False):
        """
        edit the books a given author have publicated. if remove, change, 
        del_all are all set to False, then a new book will be added.
        
        
        args:
            author_obj (query_object): query object to be edited.
            book_id (str): id of book to edit, either removed or changed.
            new_book_id (str): book to be added.
            remove (bool): remove the name of a given author.
            change (bool): change the name of a given author.
            del_all (bool): removes all authors for the given book if True.
        """
        book_id = book_id.lower()
        new_book_id = new_book_id.lower()
        
        if True not in [remove, change, del_all]:
            book_id = self.check_book_id(book_id)
            books = list(BookAuthor.objects.filter(author=author_obj))
            
            for i, j in enumerate(books):
                books[i] = j.book
            
            if book_id not in books:
                BookAuthor(author=author_obj, book=book_id).save()
        
        elif change is True and new_book_id != '':
            old_book = self.check_book_id(book_id)
            new_book = self.check_book_id(new_book_id)
            
            if old_book is not None and new_book is not None:
                book_author = BookAuthor.objects.all()
                book_author = book_author.get(author=author_obj, book=old_book)
                book_author.book = new_book
                book_author.save()
        
        elif remove is True:
            book_id = self.check_book_id(book_id)
            
            if book_id is not None:
                book_author = BookAuthor.objects.all()
                book_author = book_author.get(author=author_obj, book=book_id)
                book_author.delete()
        
        elif del_all is True:
            books = BookAuthor.objects.filter(author=author_obj)
            for i in books:
                i.delete()
    
    def edit_conditions(self, author_obj, input_str):
        """
        method that controls which field to edit.
        
        args:
            author_obj (query_object): query object to be edited.
            input_str (str): which field to edit.
        
        returns:
            (bool): False, if given input_str does not match with a field.
        """
        if input_str[:1] == 'n' or input_str == 'name':
            self.str_shortcut('Enter new name')
            new_name = input()
            
            arg = self.default_argument_message()
            self.edit_name(author_obj, new_name, arg)
        
        elif input_str[:1] == 'b' or input_str == 'birthdate':
            self.str_shortcut('Enter new birthdate')
            new_date = input()
            arg = self.default_argument_message()
            self.edit_birthdate(author_obj, new_date, arg)
        
        elif input_str[:1] == 'n' or input_str == 'nationality':
            self.str_shortcut('Enter new nationality')
            nationality = input()
            arg = self.default_argument_message()
            self.edit_nationality(author_obj, nationality, arg)
            
        elif input_str[:1] == 'p' or input_str == 'publication':
            self.str_shortcut('Enter book_id')
            book_id = input()
            
            self.str_shortcut('Type "remove", "change", or "del_all"')
            arg = self.check_expanded_args(input().lower(), 'new_book_id')
            self.edit_publication(author_obj, book_id, *arg)
        else:
            return False
        
    def edit_author(self, author_id):
        """
        initiate editing of the fields for a given author.
        
        args:
            author_obj (query_object): query object to be edited.
        """
        try:
            author = Author.objects.get(id=author_id)
        except:
            print('no author with that id')
            exit()
        
        data = self.read_help_file('edit_menu.json')
        text, help_str = self.support_text('author', data)
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
            elif input_str == 'lookup_book':
                self.author_publication(author.id)
                continue
            elif input_str == 'lookup_general':
                self.get_overview(True)
                continue
            elif input_str == 'delete':
                author.delete()
                break
            
            if self.edit_conditions(author, input_str) is None:
                continue
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
        
        self.make_title('main/author')
        
       


















