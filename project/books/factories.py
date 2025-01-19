import factory
from .models import Author, Book
from faker import Faker

fake = Faker()

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.LazyAttribute(lambda _: fake.name())
    birth_date = factory.LazyAttribute(lambda _: fake.date_of_birth())

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=5))
    description = factory.LazyAttribute(lambda _: fake.text())
    published = factory.LazyAttribute(lambda _: fake.boolean())
    published_date = factory.LazyAttribute(lambda _: fake.date_this_century())
    author = factory.SubFactory(AuthorFactory)
