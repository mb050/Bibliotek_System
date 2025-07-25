from bibliotek.models import BookCategory
from bibliotek.models import Category
from classes.base import Base

from sys import exit
import numpy as np

class Category_query(Base):
    """
    containts queries related to categories.
    
    methods:
        add_category: register a new category.
        update_id: updates a given id.
        check_id: checks all id and updates them.
        category_table: get a table of all registered categories.
        edit_name: edit name
        get_category_obj: verifies the existence of a category.
        edit_category: initiates the editing of category fields.
    """
    
    def add_category(self, category_name):
        """
        register a new category to the database.
        
        args:
            category_name (str): name of category.
        """
        self.check_id()
        id_list = [i[0] for i in Category.objects.values_list('id')]
        idx = max(id_list) + 1
        del(id_list)
        
        category_name = category_name.lower().capitalize()
        try:
            new_category = Category(id=idx, name=category_name)
            new_category.save()
        except:
            pass
        return
    
    def update_id(self, idx, id_list, new_idx):
        """
        rearange category id and reassigns all related books to the new
        category id.
        
        args:
            idx (np.array): indexes for id that are out of order.
            id_list (np.array): array with original id.
            new_idx (np.array): array with new id.
        """
        for I in idx:
            category_obj = Category.objects.get(id=id_list[I])
            new_obj = Category(id=new_idx[I], name=category_obj.name)
        
            temp = []
            bc = BookCategory.objects.filter(category=category_obj) 
            for i in bc:
                temp.append([i.id, i.book])
                
            category_obj.delete()
            new_obj.save()
            
            for (j, k) in temp:
                BookCategory(id=j, book=k, category=new_obj).save()
    
    def check_id(self):
        """
        checks if all id are in increasing order, and not skipping any numbers.
        """
        category_obj = Category.objects.all()
        id_list = np.array([i[0] for i in category_obj.values_list('id')])
        new_idx = np.arange(len(id_list)) + 1
        location_arr = id_list - new_idx
        idx = np.where(location_arr != 0)[0]
        
        if len(idx) > 0:
            self.update_id(idx, id_list, new_idx)
        return
    
    def category_table(self, get_table=False):
        """
        get a table containing the name of category, and amount of books with
        said category.
        
        args:
            get_table (bool): controls if a table is printed to terminal.
        """
        categories = Category.objects.all()
        headers = ['id', 'category_name', 'books_in_category']
        entries = [''] * len(categories)
        
        for i, j in enumerate(categories):
            amount = categories.filter(bookcategory__category=j).count()
            entries[i] = [j.id, j.name, amount]
        
        table = self.make_table(entries, headers)
        
        if get_table is not False:
            print(table)

    # =========================================================================

    def edit_name(self, category_obj, new_name):
        """
        edit name for a given category.
        
        args:
            category_obj (query_object): query object to be edited.
            new_name (str): new name.
            edit (bool): controls if the field is edited or set to None.
        """
        try:
            category_obj.name = new_name.lower().capitalize()
            category_obj.save()
        except:
            pass
        
    def get_category_obj(self, category_name):
        """
        will check if a given category name exist, and will get the query
        object with said name.
        
        args:
            category_name (str): name of category
        
        returns:
            (bool) or (query_object): if no category with given name is found,
                                      the it returns None, else a query_object.
        """
        try:
            category_name = category_name.lower().capitalize()
        except:
            return
        
        try:
            return Category.objects.get(name=category_name)
        except:
            pass

    def edit_category(self, category_id):
        """
        initiate editing of the fields for a given category.
        
        args:
            category_obj (query_object): query object to be edited.
        """
        try:
            category_obj = Category.objects.get(id=category_id)
        except:
            category_obj = self.get_category_obj(category_id)
        
        if category_obj is None:
            print('no category with that name or id')
            return 
        
        data = self.read_help_file('edit_menu.json')
        text, help_str = self.support_text('category', data)
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
                self.category_table(True)
                continue
            elif input_str == 'delete':
                category_obj.delete()
                break
            
            if input_str == 'name':
                self.str_shortcut('enter new name')
                input_str = input()
                self.edit_name(category_obj, input_str)
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
            
        self.make_title('main/category')


