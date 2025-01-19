import pytest
from rest_framework import status
from django.urls import reverse
from books.models import Author, Book
from books.serializers import AuthorSerializer, BookSerializer
from books.factories import AuthorFactory, BookFactory

@pytest.mark.django_db
def test_author_serializer():
    author = AuthorFactory()  
    serializer = AuthorSerializer(author)
    
    assert serializer.data['name'] == author.name
    assert serializer.data['birth_date'] == str(author.birth_date)

@pytest.mark.django_db
def test_book_serializer():
    book = BookFactory()  #
    serializer = BookSerializer(book)
    
    assert serializer.data['title'] == book.title
    assert serializer.data['author']['name'] == book.author.name
    assert serializer.data['published'] == book.published
    assert serializer.data['published_date'] == str(book.published_date)

@pytest.mark.django_db
def test_author_viewset_list(client):
    AuthorFactory.create_batch(5)
    
    url = reverse('author-list')
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5

@pytest.mark.django_db
def test_book_viewset_create(client):
    author = AuthorFactory()
    book_data = {
        'title': 'New Book Title',
        'description': 'Book Description',
        'published': True,
        'published_date': '2025-01-01',
        'author': author.id
    }
    
    url = reverse('book-list')
    response = client.post(url, book_data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == book_data['title']
    assert response.data['author']['name'] == author.name

@pytest.mark.django_db
def test_book_viewset_update(client):
    book = BookFactory()
    updated_data = {
        'title': 'Updated Book Title',
        'description': 'Updated Description',
        'published': True,
        'published_date': '2025-01-01',
        'author': book.author.id
    }
    
    url = reverse('book-detail', args=[book.id])
    response = client.put(url, updated_data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == updated_data['title']

@pytest.mark.django_db
def test_book_viewset_delete(client):
    book = BookFactory()
    
    url = reverse('book-detail', args=[book.id])
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Book.objects.filter(id=book.id).exists()

@pytest.mark.django_db
def test_book_viewset_filter(client):
    author1 = AuthorFactory(name="Author One")
    author2 = AuthorFactory(name="Author Two")
    BookFactory.create_batch(5, author=author1)
    BookFactory.create_batch(3, author=author2)
    
    url = reverse('book-list') + '?author=' + author1.name
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5

@pytest.mark.django_db
def test_book_viewset_pagination(client):
    author = AuthorFactory()
    BookFactory.create_batch(20, author=author)
    
    url = reverse('book-list')
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5  
    assert 'next' in response.data  

@pytest.mark.django_db
@pytest.mark.parametrize(
    'author_data, expected_name',
    [
        ({"name": "J.K. Rowling", "birth_date": "1965-07-31"}, "J.K. Rowling"),
        ({"name": "George R.R. Martin", "birth_date": "1948-09-20"}, "George R.R. Martin"),
    ]
)
def test_author_serializer_with_params(author_data, expected_name):
    author = Author.objects.create(**author_data)
    serializer = AuthorSerializer(author)
    
    assert serializer.data['name'] == expected_name

@pytest.fixture
def author():
    return AuthorFactory()

@pytest.fixture
def book(author):
    return BookFactory(author=author)

@pytest.mark.django_db
def test_book_serializer_with_fixture(book):
    serializer = BookSerializer(book)
    assert serializer.data['title'] == book.title
    assert serializer.data['author']['name'] == book.author.name

