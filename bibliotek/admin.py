from django.contrib import admin
# Register your models here.

from .models import * 

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookAuthor)

admin.site.register(Customer)
admin.site.register(Category)

admin.site.register(Library)
admin.site.register(Borrowed)

admin.site.register(BookCategory)
admin.site.register(BorrowedCustomer)
admin.site.register(BorrowedBook)
admin.site.register(BorrowingLog)
