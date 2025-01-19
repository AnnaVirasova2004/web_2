from django.db import transaction
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import AuthorSerializer, BookSerializer
from django.shortcuts import render
from .models import Book, Author
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework import status, permissions
from rest_framework import filters
from rest_framework import generics
from .models import Book  
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination

#Сортировка по названию (ограничение 10 книг)
def book_list(request):
    books = Book.objects.select_related(published=True).order_by('title')[:10]
    return render(request, 'books/book_list.html', {'books': books})

def create_book(request):
    with transaction.atomic():
        author = Author.objects.get(name='J.K. Rowling')
        book = Book.objects.create(
            title='New Book',
            description='A new fantasy novel',
            published=True,
            published_date='2025-01-01',
            author=author
        )
    return render(request, 'books/book_created.html', {'book': book})

def author_books(request):
    authors = Author.objects.prefetch_related('books').all()
    return render(request, 'authors/author_books.html', {'authors': authors})

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']  # Фильтрация по имени автора

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'published_date']  # Фильтрация по полям
    ordering = ['title'] 

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]  

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ к данным только их владельцам.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]