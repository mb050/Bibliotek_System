from bibliotek.models import Customer
from classes.base import Base

from datetime import date
from sys import exit

class Customer_query(Base):
    """
    containts queries related to customers.
    
    methods:
        add_customer: register a new customer.
        get_overview: get a table of all customers.
        search_customer: search for a customer.
        edit_name: edit name.
        edit_address: edit address.
        edit_contact_info: edit contact information.
        edit_membership_date: edit membership date.
        edit_conditions: method for deciding which field to edit.
        edit_customer: initiates the editing of customer fields.
    """
    
    def add_customer(self, name, address=None, contact_info=None, 
                     signup_date=None):
        """
        register new customer.
        
        args:
            name (str): name, mandatory.
            address (str): optional.
            contact_info (str): optional.
            signup_date (date): optional.
        """
        if signup_date is None:
            signup_date = date.today()
        
        Customer(name=name, address=address, contact_info=contact_info, 
                 membership_date=signup_date).save()
        
    
    def get_overview(self, query_obj=None, get_table=False):
        """
        makes a table of all customers with their id, name, address, 
        contact_info and registration_date.
        
        args:
            query_obj (query_object): filtered query objects, optional.
            get_table (bool): controls if a table is printed to terminal.
        
        returns:
            None
        """
        if query_obj is None:
            customer = Customer.objects.all()
        else:
            customer = query_obj
            
        try:
            fields = list(customer.values()[0].keys())
        except:
            print('no customer')
            return
        
        entries = [list(i) for i in customer.values_list()]        
        table = self.make_table(entries, fields)
        
        if get_table is not False:
            print(table)
        return
    
    def search_customer(self, customer_id='', customer_name=''):
        """
        search for a customer given their id or name.
        
        args:
            customer_id (str): id.
            customer_name (str): name.
        """
        customer_dict = {'id': customer_id, 'name': customer_name}
        key_list = list(customer_dict.keys())
        
        for i in key_list:
            if customer_dict[i] in ['', None]:
                customer_dict.pop(i)
        
        customer_obj = Customer.objects.filter(**customer_dict)
        self.get_overview(customer_obj, get_table=True)
        
    # =========================================================================

    def edit_name(self, customer_obj, new_name, edit=True):
        """
        edit name for a given customer.
        
        args:
            customer_obj (query_object): query object to be edited.
            new_name (str): new name.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            customer_obj.name = new_name
        else:
            customer_obj.name = None
        
        customer_obj.save()

    def edit_address(self, customer_obj, new_address, edit=True):
        """
        edit address for a given customer.
        
        args:
            customer_obj (query_object): query object to be edited.
            new_address (str): new address.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            customer_obj.address = new_address
        else:
            customer_obj.address = None
        
        customer_obj.save()

    def edit_contact_info(self, customer_obj, new_contact_info, edit=True):
        """
        edit contact information for a given customer.
        
        args:
            customer_obj (query_object): query object to be edited.
            new_contact_info (str): new contact information.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            customer_obj.contact_info = new_contact_info
        else:
            customer_obj.contact_info = None
        
        customer_obj.save()

    def edit_membership_date(self, customer_obj, new_date, edit=True):
        """
        edit registration date for the membership for a given customer.
        
        args:
            customer_obj (query_object): query object to be edited.
            new_date (date): new registration date.
            edit (bool): controls if the field is edited or set to None.
        """
        if edit is True:
            try:
                customer_obj.membership_date = new_date
            except:
                print('given date was not correctly formatted')
        else:
            customer_obj.membership_date = None
        
        customer_obj.save()
    
    def edit_conditions(self, customer_obj, input_str):
        """
        method that controls which field to edit.
        
        args:
            customer_obj (query_object): query object to be edited.
            input_str (str): which field to edit.
        
        returns:
            (bool): False, if given input_str does not match with a field.
        """
        if input_str[:1] == 'n' or input_str == 'name':
            self.str_shortcut('Enter new name')
            new_name = input()
            
            arg = self.default_argument_message()
            self.edit_name(customer_obj, new_name, arg)
        
        elif input_str[:1] == 'a' or input_str == 'address':
            self.str_shortcut('Enter new address')
            new_address = input()
            
            arg = self.default_argument_message()
            self.edit_address(customer_obj, new_address, arg)
        
        elif input_str[:1] == 'c' or input_str == 'contact_info':
            self.str_shortcut('Enter new contact_info')
            new_contact_info = input()
            
            arg = self.default_argument_message()
            self.edit_contact_info(customer_obj, new_contact_info, arg)
        
        elif input_str[:1] == 'm' or input_str == 'membership_date':
            self.str_shortcut('Enter new membership_date')
            new_date = input()
            
            arg = self.default_argument_message()
            self.edit_membership_date(customer_obj, new_date, arg)
        else:
            return False
            
    def edit_customer(self, customer_id):
        """
        initiate editing of the fields for a given customer.
        
        args:
            customer_obj (query_object): query object to be edited.
        """
        try:
            customer = Customer.objects.get(id=customer_id)
        except:
            print('no customer with that id')
            return
        
        data = self.read_help_file('edit_menu.json')
        text, help_str = self.support_text('customer', data)
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
                self.get_overview(get_table=True)
                continue
            elif input_str == 'delete':
                customer.delete()
                break
            
            if self.edit_conditions(customer, input_str) is None:
                continue
            else:
                print(invalid, end=' ')
                was_invalid = True
                continue
        
        self.make_title('main/customer')
        





