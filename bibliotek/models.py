# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the 
#   * desired behavior Remove `managed = False` lines if
#   *  you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or 
# field names.
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    membership_date = models.DateField(blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=252, blank=True, null=True, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

class Library(models.Model):
    library_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Libraries"

    
class Author(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)    
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    category = models.ManyToManyField(Category, through='BookCategory')
    authors = models.ManyToManyField(Author, through='BookAuthor')
    isbn_10 = models.CharField(max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, 
                                blank=True, null=True)
    individual_id = models.SmallIntegerField(blank=True, default=1)
    available = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title


class Borrowed(models.Model):
    book_id = models.ManyToManyField(Book, through='BorrowedBook')
    customer = models.ManyToManyField(Customer, through='BorrowedCustomer')
    default_lending_period = models.SmallIntegerField(blank=True, default=14)
    lending_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    extentions = models.SmallIntegerField(blank=True, null=True, default=0)
    overdue = models.CharField(max_length=10, blank=True, default='no')

    class Meta:
        verbose_name_plural = "Borrowed"


class BorrowingLog(models.Model):
    borrowing_id = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, 
                                 blank=True, null=True)    
    
    library_id = models.CharField(max_length=100, blank=True, null=True)
    book_id = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    isbn_10 = models.CharField(max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    default_lending_period = models.SmallIntegerField(blank=True, null=True)
    lending_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    extentions = models.SmallIntegerField(blank=True, null=True)
    overdue = models.CharField(max_length=10, blank=True, null=True)
    

class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Book_Author"
    
class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, models.DO_NOTHING)
    borrow = models.ForeignKey(Borrowed, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Borrowed_Book"


class BorrowedCustomer(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    borrow = models.ForeignKey(Borrowed, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Borrowed_Customer"


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Book_category"


