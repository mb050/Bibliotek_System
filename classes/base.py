from bibliotek.models import Category
from bibliotek.models import Library
from bibliotek.models import Author
from bibliotek.models import Book
from tabulate import tabulate
from datetime import date
import json as js

class Base():
    """
    contains methods used by several classes.
    
    methods:
        make_table: creates a standard table.
        str_shortcut: make formatted string.
        search_book: search for a book.
        remove_empty_values: removes key value pair from dictionary.
        check_category: check if a category exist.
        check_library_id: check if a library exist.
        check_author: check if an author exist.
        check_title: check if a book title exist.
        check_argument: checks for basic arguments for editing fields.
        check_expanded_args: checks for expanded arguments for editing fields.
        check_date: check if a string can be converted to a date.
        check_lenght: compare string length.
        set_filename: method for using default or custom file name.
        default_argument_message: gives a default message for editing fields.
        sort_list: sort nested list.
        request_yes_no: method for getting True or False.
        check_number: check if a given number is an int.
        request_number: method for getting and verifying an input as a number.
        read_help_file: reads the help.json
        get_json_text: turns list with strings into a single string
        get_json_help: get the help description from the json file.
        support_text: retrieves all the support text from the json file.
        make_title: method that creates a title for the interface.
    """
    
    def make_table(self, values, header_list, default_format=True, 
                   include_space=True):
        """
        creates a table.
        
        args:
            values (list): nested_list.
            header_list (list): list containing the header.
            default_format (str): format name.
            include_space (bool): wether '\n' should be included at the start. 
        
        return:
            table (table): table with the result.
        """
        if default_format is True:
            tbl_format = 'presto'
        else:
            tbl_format = default_format
        
        table = tabulate(values, headers=header_list, tablefmt=tbl_format)
        
        if include_space is True:
            table = '\n' + table
        
        return table
    
    def str_shortcut(self, message=''):
        """
        method for pre-formatted message to be printed to the terminal.
        
        args:
            message (str): message to be printed.
        """
        print(f'\n{message}:\n>', end=' ')
    
    def search_book(self, book_id='', title='', publish_date='', 
                    category_name='', author_name='', isbn_10='', isbn_13='',
                    library_id=''):
        """
        search for a book with any number of function arguments.
        
        args:
            book_id (str): id of book.
            itle (str): title of the book. 
            publish_date (date): optional.
            category_name (str): optional. 
            author_name (str): optional.
            isbn_10 (str): optional.
            isbn_13 (str): optional.
            library_id (str): optional.
        
        returns:
            filtered result (query object)
        """
        instance_arg = locals()
        instance_arg = self.remove_empty_values(instance_arg)
        key_list = list(instance_arg.keys())
        book_obj = Book.objects.all()
        
        if 'author_name' in key_list:
            author_obj = self.check_author(author_name)
            instance_arg.pop('author_name')
            
            if author_obj is not None:
                book_obj = book_obj.filter(bookauthor__author=author_obj)

        if 'category_name' in key_list:
            category_obj = self.check_category(category_name)
            instance_arg.pop('category_name')
            
            if category_obj is not None:
                book_obj = book_obj.filter(bookcategory__category=category_obj)
    
        if 'title' in key_list:
            corrected_title = self.check_title(title)
            
            if corrected_title is not None:
                instance_arg['title'] = corrected_title
            else:
                instance_arg.pop('title')
        
        if 'isbn_10' in key_list and len(isbn_10) != 10:
            instance_arg.pop('isbn_10')
        
        if 'isbn_13' in key_list and len(isbn_13) != 13:
            instance_arg.pop('isbn_13')
        
        if 'library_id' in key_list:
            library_obj = self.check_library_id(library_id)
            
            if library_obj is not None:
                instance_arg['library_id'] = library_obj
            else:
                instance_arg.pop('library_id')
            
        return book_obj.filter(**instance_arg)
        
    def remove_empty_values(self, dict_obj):
        """
        removes keys if their value pair is None or empty.
        
        args:
            dict_obj (dict): dictionary with keys and values.
        
        returns:
            dict_obj (dict): altered.
        """
        try:
            dict_obj.pop('self')
        except:
            pass
        
        key_list = list(dict_obj.keys())
 
        for i in key_list:
            if dict_obj[i] == '' or dict_obj[i] is None:
                dict_obj.pop(i)
                
        return dict_obj
    
    
    def check_category(self, category_name, return_message=False):
        """
        check if a category exist.
        
        args:
            category_name (str): name of category.
            return_message (bool): if an error message schould be returned.
        returns:
            category_object (query object) or None (bool) 
        """
        category_name = category_name.lower().capitalize()
        
        try:
            return Category.objects.get(name=category_name)
        except:
            pass
        
        if return_message is not False:
            print(f'no category named: {category_name}')
        
        
    def check_library_id(self, library_id):
        """
        checks if a given library id exist.
        
        args:
            library_id (str): the id to be compared.
        
        returns:
            library_queries (query object).
        """
        library = Library.objects.all()
        
        id_list = []
        library_dict = {}
        for i, j in enumerate(library):
            id_name = j.library_id.lower()
            library_dict[id_name] = i
            id_list.append(id_name)
            
        if library_id in id_list:
            return library[library_dict[library_id]]

            
    def check_author(self, author_name):
        """
        check if a given author exist.
        
        args:
            author_name (str): author name.
        
        returns:
            (query objects) or None.
        """
        author_query = Author.objects.all()
        name_list = []
        name_dict = {}
        
        for i, j in enumerate(author_query):
            author = j.name.lower()
            name_list.append(author)
            name_dict[author] = i
            
        if author_name in name_list:
            return author_query[name_dict[author_name]]
        
    def check_title(self, book_name, return_str=False):
        """
        check if a title for a book exist.
        
        args:
            book_name (str): book name.
            return_str (bool): control if query object will be returned.
        
        returns:
            (query objects) or None.
        """
        book_name = book_name.lower()
        books = Book.objects.all()
        
        title_list = []
        title_dict = {}
        for i, j in enumerate(books):
            book_title = j.title.lower()
            title_list.append(book_title)
            title_dict[book_title] = i
        
        if book_name in title_list and return_str is False:
            return books[title_dict[book_name]].title

    def check_argument(self, argument):
        """
        checks for simple arguments for editing fields.
        
        args:
            argument (str): argument to be used.
        
        returns:
            True (bool) or False (bool)
        """
        if argument == 'edit':
            return True
        else:
            return False

    def check_expanded_args(self, argument, var_name=''):
        """
        checks for expanded arguments for editing fields.
        
        args:
            argument (str): argument to be used.
            var_name (str): custom variable name.
        
        returns:
            args (list): contains str, and 3 bool.
        """
        args = ['', False, False, False]
                       
        if argument == 'remove':
            args[1] = True
        elif argument == 'change':
            args[2] = True
            print(f'enter input for {var_name}:')
            args[0] = input()
        elif argument == 'del_all':
            args[3] = True
        
        return args
    
    
    def check_date(self, date_str):
        """
        check if string can be turned to date.
        
        args:
            date_str (str): string to be converted.
        
        returns:
            None (bool) or date_str (date)
        """
        if date_str == '':
            return None
        
        date_list = date_str.replace('-', ' ').split()
        date_list = map(int, date_list)
        
        try:
            date_str = date(*date_list)
            return date_str
        except:
            print('not a valid date')
            return None
    
    
    def check_lenght(self, input_str, length, return_var=None):
        """
        checks if a string is a given length.
        
        args:
            input_str (str): string to be checked. 
            length (int): number for characters to check for.
            return_var (str): string to return if conditions are not met.
        
        returns:
            input_str (str) or return_var (str)
        """
        if len(input_str) == length:
            return input_str
        elif input_str == '':
            return return_var
        else:
            print(f'\nGiven input is not {length} characters long')
            return return_var
    
    
    def set_filename(self, custom_filename, default):
        """
        give default or custom filename.
        
        args:
            custom_filename (bool): control if custom filename should be used.
            default (str): default filename.
        
        returns:
            filename (str): filename to be used.
        """
        if custom_filename is True:
            self.str_shortcut('Enter filename')
            filename = input()
        else:
            filename = default
        
        return filename
    
    def default_argument_message(self):
        """
        gives default message for editing fields.
        """
        self.str_shortcut('Type "yes" to edit field, or "no" to set to None')
        return self.request_yes_no(input())
    
    def sort_list(self, value_list, idx, reverse=True):
        """
        sort nested list.
        
        args:
            value_list (list): nested list.
            idx (int): index.
            reverse (bool): True.
        
        return:
            sorted_list (list): sorted list given index.
        """
        index_to_sort = lambda x: x[idx]
        sorted_list = sorted(value_list, key=index_to_sort)
        
        if reverse is True:
            return list(reversed(sorted_list))
        else:
            return sorted_list
    
    def request_yes_no(self, input_str):
        """
        ask for the user to choose between yes/True or no/False.
        
        args:
            input_str (str): string of own choice.
        
        return:
            statement (bool): True or False.
        """
        input_str = input_str.lower()
        statement = ''
        while statement == '':
            if 'yes' in input_str or '1' in input_str or input_str[:1] == 'y':
                statement = True
            elif 'no' in input_str or '0' in input_str or input_str[:1] == 'n':
                statement = False
            elif input_str in ['', 'quit', 'exit', 'stop', 'cancel']:
                print('defaulting to "yes".\n', end=' ')
                statement = True
            else:
                print('\ninvalid input, type "yes" or "no":\n>', end=' ')
                input_str = input().lower()       
        return statement
    
    def check_number(self, x, default_number):
        """
        check if a string can be turned into an int.
        
        args:
            x (str): string of own choice to be turned into int.
            default_number (int): the default number to return if the user
                                  doesn't give anything or cancels the process.
        return:
            x (int): valid int.
        """
        message = '\ninvalid input, enter a new number or type "stop":\n>'
        break_list = ['', 'quit', 'exit', 'stop', 'cancel', 'none', 'default']
        while not(isinstance(x, int)):
            try:
                x = int(x)
            except:
                if x.lower() in break_list:
                    print(f'defaulting to {default_number}.\n', end=' ')
                    x = None
                    break
                
                print(message, end=' ')
                x = input()
        return x

    def request_number(self, message=None, set_default=None, number=''):
        """
        asks for a number.
        
        args:
            message (str): custom message to be used.
            set_default (bool or int): decides if None or a custom input is
                                       returned when the default output is 
                                       chosen.
            number (str): not to be used. just there to define the variable and
                          enable the while loop to start.
        return:
            number (int): can return None.
        """
        while not(isinstance(number, int)):
            if message is not None:
                print(message, end=' ')
            
            number = self.check_number(input().lower(), set_default)
            if number == '' or number is None:
                number = set_default
                break
        
        return number
    
    
    def read_help_file(self, filepath='help.json'):
        """
        read the help.json and saves it as an instance.
        """
        file = open('support text/' + filepath, 'r')
        data = js.load(file)
        file.close()
        
        if filepath != 'help.json':
            return data
        else:
            self.data = data
        
    
    def get_json_text(self, text):
        """
        takes in list containing strings and turns it into a single string.
        
        args:
            text (list): list of strings.
        
        return:
            a single string.
        """
        return ' '.join(text)
    
    def get_json_help(self, key, data=None):
        """
        gather all the help descriptions from the json file in a given key
        and value pair, and turn it into a single string.
        
        args:
            key (str): key for which json key value pair to use.
        
        return:
            help_str (str): complete help description
        """
        help_str = ''
        
        if data is not None:
            json_dict = data[key]['help']
        else:
            json_dict = self.data[key]['help']
            
        for i, j in zip(json_dict.keys(), json_dict.values()):
            help_str += f'{i} {self.get_json_text(j)}'
        return help_str
    
    def support_text(self, key, std_data=None):
        """
        read and returns the different support text and descriptions used in
        the interface from either the main menu, or the categories.
        
        args:
            key (str): which key value pair from the json file to use.
        
        return:
            text_list (list): list containing the different strings.
            help_text (str): the help string used when additional 
                             information is needed.
        """
        key_list = ['title', 'invalid', 'input', 'commands', 
                    'overview', 'options']
        
        if std_data is None:
            data = self.data
        else:
            data = std_data
        
        help_str = self.get_json_help(key, data)
        
        text_list = []
        for i in range(6):
            if i < 3:
                text = data[key][key_list[i]]
            else:
                text = self.get_json_text(data[key][key_list[i]])
            
            text_list.append(text)
    
        self.make_title(text_list[0])
        print(text_list[3])
        print(text_list[4])
        return text_list, help_str
    
    def make_title(self, string, default_space=20):
        """
        print out the string in a standardized manner.
        
        args:
            string (str): the title to use.
            default_space (int): the default amount of space to use.
        """
        length = len(string)
        odd = length % 2
        length = int((length - odd) / 2)
        spacing = '-' * (20 - length) 
        padding = '-'*(1 - odd)
        print('\n' + padding + f'{spacing}{string}{spacing}')
    
    
    
    
    
    
    