from bibliotek.models import Library
from bibliotek.models import Book
from classes.base import Base

from sys import exit

class Library_query(Base):
    """
    containts queries related to libraries.
    
    methods:
        check_library_id: check if a given library_id exist.
        add_library: register a new library.
        overview: get a table of all libraries.
        lookup_books: overview of books for a given library.
        edit_id: edit id.
        edit_name: edit name.
        edit_address: edit address.
        edit_contact_info: edit contact information.
        edit_conditions: method for deciding which field to edit.
        edit_library: initiates editing of fields.
    """
    
    def check_library_id(self, compare_id):
        """
        checks if a given library id exist.
        
        args:
            compare_id (str): the id to be compared.
        
        returns:
            result (bool): True or False.
        """
        id_list = [i[0] for i in Library.objects.values_list('library_id')]
        
        if str(compare_id) in id_list:
            result = True
        else:
            result = False
        
        del(id_list)
        return result
    
    def add_library(self, library_id, name, address='', contact_info=''):
        """
        register a new library to the database.
        
        args:
            library_id (str): the id of the library.
            name (str): name of the library.
            address (str): address of the library, optional.
            contact_info (str): contact information to the library, optional.
        
        returns:
            None
        """
        if len(library_id) == 0:
            print('\nlibrary_id can not be left empty')
            return
        elif len(name) == 0:
            print('\nname can not be left empty')
            return
        
        if self.check_library_id(library_id) is True:
            print('\nGiven library_id already exist. The library_id '
                  'must be unique')
            return
        
        new_library = Library(library_id, name, address, contact_info)
        new_library.save()
    
    def overview(self, get_table=False):
        """
        makes a table of all libraries with their id, name, address and 
        contact_info.
        
        args:
            get_table (bool): controls if a table is printed to terminal.
        """
        library_obj = Library.objects.all()
        book = Book.objects.all()
        
        fields = ['library_id', 'name', 'address', 'contact_info', 'n_books']
        entries = [list(i) for i in library_obj.values_list()]
        
        for i, j in enumerate(library_obj):
            amount = book.select_related('library').filter(library=j).count()
            entries[i].append(amount)                                                    
        
        table = self.make_table(entries, fields)
        
        if get_table is not False:
            print(table)
        
    
    def lookup_books(self, Library_id, get_table=False):
        """
        makes a table of all books in a library for a given library_id.
        
        args:
            Library_id (str): id of library.
            get_table (bool): controls if a table is printed to terminal.
        """
        book = Book.objects.all().select_related('library'
                                                 ).filter(library=Library_id)
        try:
            fields = list(book.values()[0].keys())
        except:
            print('no books belongs to the given library')
            return
            
        entries = [list(i) for i in book.values_list()]        
        table = self.make_table(entries, fields)
        
        if get_table is not False:
            print(table)

    # =========================================================================

    def edit_id(self, library_obj, new_id):
        """
        edit id for a given library.
        
        args:
            library_obj (query_object): query object to be edited.
            new_id (str): new id.
        """
        if self.check_library_id(new_id) is False:
            library_obj.library_id = new_id
            library_obj.save()

    def edit_name(self, library_obj, new_name, edit=True):
        """
        edit name for a given library.
        
        args:
            library_obj (query_object): query object to be edited.
            new_name (str): new name.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            library_obj.name = new_name
        else:
            library_obj.name = None
        
        library_obj.save()

    def edit_address(self, library_obj, new_address, edit=True):
        """
        edit address for a given library.
        
        args:
            library_obj (query_object): query object to be edited.
            new_address (str): new address.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            library_obj.address = new_address
        else:
            library_obj.address = None
        
        library_obj.save()

    def edit_contact_info(self, library_obj, new_contact_info, edit=True):
        """
        edit contact information for a given library.
        
        args:
            library_obj (query_object): query object to be edited.
            new_contact_info (str): new contact information.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            library_obj.contact_info = new_contact_info
        else:
            library_obj.contact_info = None
        
        library_obj.save()
    
    def edit_conditions(self, library_obj, input_str):
        """
        method that controls which field to edit.
        
        args:
            library_obj (query_object): query object to be edited.
            input_str (str): which field to edit.
        
        returns:
            (bool): False, if given input_str does not match with a field.
        """
        
        if input_str[:1] == 'i' or input_str == 'id':
            self.str_shortcut('Enter new id')
            new_id = input()
            
            self.edit_id(library_obj, new_id)
        
        elif input_str[:1] == 'n' or input_str == 'name':
            self.str_shortcut('Enter new name')
            new_name = input()
            
            arg = self.default_argument_message()
            self.edit_name(library_obj, new_name, arg)
        
        elif input_str[:1] == 'a' or input_str == 'address':
            self.str_shortcut('Enter new address')
            new_address = input()
            
            arg = self.default_argument_message()
            self.edit_address(library_obj, new_address, arg)
        
        elif input_str[:1] == 'c' or input_str == 'contact_info':
            self.str_shortcut('Enter new contact_info')
            new_contact_info = input()
            
            arg = self.default_argument_message()
            self.edit_contact_info(library_obj, new_contact_info, arg)
        else:
            return False
            
    def edit_library(self, library_id):
        """
        initiate editing of the fields for a given library.
        
        args:
            library_obj (query_object): query object to be edited.
        """
        try:
            library = Library.objects.get(library_id=library_id)
        except:
            print('no library with that id')
            return
        
        data = self.read_help_file('edit_menu.json')
        text, help_str = self.support_text('library', data)
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
                self.overview(get_table=True)
                continue
            elif input_str == 'delete':
                library.delete()
                break
            
            if self.edit_conditions(library, input_str) is None:
                continue
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
        
        self.make_title('main/library')
        

