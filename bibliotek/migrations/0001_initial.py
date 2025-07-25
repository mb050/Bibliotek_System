# Generated by Django 5.1.6 on 2025-07-24 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('isbn_10', models.CharField(blank=True, max_length=10, null=True)),
                ('isbn_13', models.CharField(blank=True, max_length=13, null=True)),
                ('individual_id', models.SmallIntegerField(blank=True, default=1)),
                ('available', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Borrowed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_lending_period', models.SmallIntegerField(blank=True, default=14)),
                ('lending_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('extentions', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('overdue', models.CharField(blank=True, default='no', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Borrowed',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=252, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_info', models.CharField(blank=True, max_length=100, null=True)),
                ('membership_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('library_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_info', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Libraries',
            },
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotek.author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotek.book')),
            ],
            options={
                'verbose_name_plural': 'Book_Author',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(through='bibliotek.BookAuthor', to='bibliotek.author'),
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bibliotek.book')),
                ('borrow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotek.borrowed')),
            ],
            options={
                'verbose_name_plural': 'Borrowed_Book',
            },
        ),
        migrations.AddField(
            model_name='borrowed',
            name='book_id',
            field=models.ManyToManyField(through='bibliotek.BorrowedBook', to='bibliotek.book'),
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotek.book')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotek.category')),
            ],
            options={
                'verbose_name_plural': 'Book_category',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(through='bibliotek.BookCategory', to='bibliotek.category'),
        ),
        migrations.CreateModel(
            name='BorrowingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowing_id', models.CharField(blank=True, max_length=100, null=True)),
                ('library_id', models.CharField(blank=True, max_length=100, null=True)),
                ('book_id', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('isbn_10', models.CharField(blank=True, max_length=10, null=True)),
                ('isbn_13', models.CharField(blank=True, max_length=13, null=True)),
                ('unique_id', models.CharField(blank=True, max_length=100, null=True)),
                ('default_lending_period', models.SmallIntegerField(blank=True, null=True)),
                ('lending_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('extentions', models.SmallIntegerField(blank=True, null=True)),
                ('overdue', models.CharField(blank=True, max_length=10, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bibliotek.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotek.borrowed')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bibliotek.customer')),
            ],
            options={
                'verbose_name_plural': 'Borrowed_Customer',
            },
        ),
        migrations.AddField(
            model_name='borrowed',
            name='customer',
            field=models.ManyToManyField(through='bibliotek.BorrowedCustomer', to='bibliotek.customer'),
        ),
        migrations.AddField(
            model_name='book',
            name='library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bibliotek.library'),
        ),
    ]
