from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Property(models.Model):
    
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(choices=PROPERTY_TYPES, max_length=50)
    location = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_feet = models.IntegerField()
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):    
        return self.title        
    

# ==========================================================================

# class Author(models.Model):
#     name = models.CharField(max_length=100)

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)

# # 1 ) Without select_related:
# books = Book.objects.all()
# for book in books:
#     print(book.title, book.author.name)

# # SELECT * FROM book;
# # SELECT * FROM author WHERE id = <author_id>;    (multiple)    

# # 2 ) With select_related:                                                                            
# books = Book.objects.select_related('author')
# for book in books:
#     print(book.title, book.author.name)

# # executes a single query with a join:
# # SELECT book.*, author.* 
# # FROM book 
# # INNER JOIN author 
# # ON book.author_id = author.id;


# # Prefatch related :

# class Author(models.Model):
#     name = models.CharField(max_length=100)

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')


# # 1 ) Without prefetch_related:
# # authors = Author.objects.all()

# # for author in authors:
# #     books = author.books.all()  # Triggers a query for each author
# #     print(author.name, [book.title for book in books])

# # This results in N+1 queries (1 query for fetching authors + 1 query for each author's books):
  
# # SELECT * FROM author;                  -- Fetch all authors
# # SELECT * FROM book WHERE author_id=1;  -- Fetch books for author 1
# # SELECT * FROM book WHERE author_id=2;  -- Fetch books for author 2
# # ...


# # 2 ) With prefetch_related:

# authors = Author.objects.prefetch_related('books')
# for author in authors:
#     books = author.books.all()  # No additional queries
#     print(author.name, [book.title for book in books])

# # This fetches all authors and their related books in two queries:

# # SELECT * FROM author;                -- Fetch all authors
# # SELECT * FROM book WHERE author_id IN (1, 2, 3);  -- Fetch all books for these authors
    
