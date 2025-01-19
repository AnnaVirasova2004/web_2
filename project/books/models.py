from django.db import models

class BookManager(models.Manager):
    def published(self):
        return self.filter(published=True)

    def by_author(self, author_name):
        return self.filter(author__name=author_name)

#две модели (связь через ForeignKey: 1 автор - 1 книга)
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published = models.BooleanField(default=False)
    published_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
    
    