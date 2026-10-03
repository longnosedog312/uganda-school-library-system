# Database Schema

## Overview
The library management system uses PostgreSQL for data storage with the following core models.

## Models

### 1. Book Model
Stores all book information in the library inventory.

```python
class Book(models.Model):
    isbn = CharField(unique=True, max_length=13)
    title = CharField(max_length=255)
    author = CharField(max_length=255)
    publisher = CharField(max_length=255)
    publication_year = IntegerField()
    category = ForeignKey(BookCategory)
    quantity_total = IntegerField()
    quantity_available = IntegerField()
    location_shelf = CharField(max_length=50)
    description = TextField(blank=True)
    book_cover = ImageField(upload_to='book_covers/')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### 2. BookCategory Model
Categorizes books for better organization.

```python
class BookCategory(models.Model):
    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True)
    code = CharField(max_length=10, unique=True)
```

### 3. Student Model
Manages student information and library accounts.

```python
class Student(models.Model):
    user = OneToOneField(User)
    student_id = CharField(unique=True, max_length=20)
    admission_number = CharField(unique=True, max_length=20)
    form = IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)])
    stream = CharField(max_length=50)  # Science, Arts, etc.
    date_of_birth = DateField()
    phone_number = CharField(max_length=20, blank=True)
    parents_contact = CharField(max_length=20)
    address = TextField()
    fine_balance = DecimalField(max_digits=10, decimal_places=2, default=0)
    account_status = CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')])
    registration_date = DateTimeField(auto_now_add=True)
```

### 4. Staff Model
Manages library staff and administrators.

```python
class Staff(models.Model):
    ROLE_CHOICES = [
        ('librarian', 'Librarian'),
        ('assistant', 'Assistant Librarian'),
        ('admin', 'Administrator'),
    ]
    
    user = OneToOneField(User)
    staff_id = CharField(unique=True, max_length=20)
    role = CharField(max_length=50, choices=ROLE_CHOICES)
    department = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    hire_date = DateField()
    is_active = BooleanField(default=True)
```

### 5. BorrowingRecord Model
Tracks book loans and returns.

```python
class BorrowingRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    book = ForeignKey(Book)
    student = ForeignKey(Student)
    borrowed_by = ForeignKey(Staff, related_name='borrowed_books')
    borrow_date = DateTimeField(auto_now_add=True)
    due_date = DateField()
    return_date = DateTimeField(null=True, blank=True)
    returned_by = ForeignKey(Staff, null=True, blank=True, related_name='returned_books')
    status = CharField(max_length=20, choices=STATUS_CHOICES)
    notes = TextField(blank=True)
```

### 6. FineRecord Model
Manages fine calculations for overdue books.

```python
class FineRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('forgiven', 'Forgiven'),
    ]
    
    borrowing_record = OneToOneField(BorrowingRecord)
    student = ForeignKey(Student)
    amount = DecimalField(max_digits=10, decimal_places=2)
    reason = CharField(max_length=255)
    status = CharField(max_length=20, choices=STATUS_CHOICES)
    created_date = DateTimeField(auto_now_add=True)
    paid_date = DateTimeField(null=True, blank=True)
    paid_by = CharField(max_length=100, null=True, blank=True)
```

### 7. LibrarySettings Model
Stores system configuration.

```python
class LibrarySettings(models.Model):
    school_name = CharField(max_length=255)
    school_email = EmailField()
    school_phone = CharField(max_length=20)
    borrow_limit = IntegerField(default=5)  # Max books per student
    borrow_duration = IntegerField(default=14)  # Days
    fine_per_day = DecimalField(max_digits=5, decimal_places=2, default=500)  # UGX
    late_fee_max = DecimalField(max_digits=10, decimal_places=2, default=10000)  # UGX
    max_overdue_days = IntegerField(default=30)
```

## Relationships Summary

```
Student ←→ BorrowingRecord ←→ Book
           ↓
        FineRecord
           ↓
         Staff (returned_by)

Staff ←→ BorrowingRecord (borrowed_by, returned_by)

Book ←→ BookCategory
```

## Indices
- Book: isbn, title, author, category
- Student: student_id, admission_number, form, stream
- BorrowingRecord: student, book, status, due_date
- FineRecord: student, status, created_date

