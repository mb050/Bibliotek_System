from os.path import exists
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotekssystem.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

def startup():
    import django
    django.setup()

try:
    from bibliotek.models import Book
except:
    startup()
    # pass

from classes.interface import Interface_Methods
from classes.base import Base
from sys import exit

class Menu(Interface_Methods, Base):
    """
    main function which allows the user to choose which queries to use.
    
    methods:
        check_folder: check if certain folder exists.
        main_menu: method for the main menu in the interface.
        universal_menu: method for the sub menus in the interface.
    """
    def __init__(self):
        self.read_help_file()
        self.check_folder()
        self.main_menu()
        return
    
    def check_folder(self):
        """
        check and creates necessary folders if they don't exist.
        """
        if exists('txt_files') is not True:
            os.mkdir('txt_files')
    
    def main_menu(self):
        """
        method for main menu.
        """
        text, help_str = self.support_text('main menu')
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
            if input_str in ['', 'stop', 'break', 'quit', 'q']:
                break
            
            if input_str[:2] == 'ca' or input_str == 'category':
                category_variable = 'category'
            elif input_str[:2] == 'li' or input_str == 'library':
                category_variable = 'library'
            elif input_str[:3] == 'boo' or input_str == 'books':
                category_variable = 'book'
            elif input_str[:2] == 'au' or input_str == 'authors':
                category_variable = 'author'
            elif input_str[:2] == 'cu' or input_str == 'customer':
                category_variable = 'customer'
            elif input_str[:2] == 'le' or input_str == 'lending':
                category_variable = 'borrowing'
            elif input_str[:3] == 'bor' or input_str == 'borrowing':
                category_variable = 'borrowing'
            elif input_str[:2] == 'an' or input_str == 'analytics':
                category_variable = 'analytic'
            elif input_str[:1] == 'h':
                print(help_str)
                continue
            elif input_str[:1] == 'o':
                print(option)
                continue
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
            
            self.universal_menu(category_variable)
            print(overview)
                    
        return
    
    def universal_menu(self, category_variable):
        """
        method for the sub menus of the interface.
        """
        function_dict = {'category': self.category_menu, 
                         'library': self.library_menu, 
                         'book': self.book_menu,
                         'author': self.author_menu,
                         'customer': self.customer_menu,
                         'borrowing': self.borrowing_menu,
                         'analytic': self.analytic_menu}
        
        text, help_str = self.support_text(category_variable)
        title, invalid, input_message = text[:3]
        command_str, overview, option = text[3:]

        run_loop = True
        was_invalid = False
        while run_loop is True:
            valid_variable = None
            
            if was_invalid is not True:
                print('\nEnter function or command:\n>', end=' ')
            else:
                was_invalid = False

            input_str = input().lower()
            
            if input_str == 'help':
                print(help_str)
                continue
            elif input_str == 'option':
                print(option)
                continue
            elif input_str in ['', 'stop', 'break', 'back']:
                break
            elif input_str == 'quit' or input_str[:1] == 'q':
                exit()
            
            valid_variable = function_dict[category_variable](input_str)
            
            if valid_variable is False:
                print(invalid, end=' ')
                was_invalid = True
            else:
                print(overview)

        self.make_title('main_menu')


if __name__ == '__main__':
    menu = Menu()


