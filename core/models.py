from django.db import models

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=64, primary_key=True)

    def serialize(self):
        cat_dict = {
            'name': self.name,
        }
        return cat_dict


class Tag(models.Model):

    name = models.CharField(max_length=64, primary_key=True)

    def serialize(self):
        tag_dict = {
            'name': self.name
        }
        return tag_dict

    @staticmethod
    def tag_cloud_data():
        tags = Tag.objects.all()
        max_count = 0
        min_count = -1
        for tag in tags:
            count = tag.posts.count()
            if count > max_count:
                max_count = count
            if min_count == -1 or min_count > count:
                min_count = count
        return (tag.serialize_tag_cloud(max_count, min_count) for tag in tags)

    def serialize_tag_cloud(self, max_count, min_count):
        size = (self.posts.count() - min_count) / (max_count - min_count) * 1.2 + 0.8
        tag = {
            'name': self.name,
            'size': size,
        }
        return tag


class Post(models.Model):

    title = models.CharField(max_length=128)
    url = models.CharField(max_length=128, primary_key=True)
    author = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    date = models.DateTimeField()
    content = models.TextField()
    content_thumbnail = models.TextField()
    category = models.ForeignKey(Category, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="posts")
    show_in_home = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def serialize(self):
        post = self.min_serialize()
        post['content'] = self.content
        return post 

    def partial_serialize(self):
        post = self.min_serialize()
        post['thumbnail'] = self.content_thumbnail
        return post

    def min_serialize(self):
        post = {
            'title': self.title,
            'author': self.author,
            'location': self.location,
            'date': self.date.isoformat(),
            'category': self.category.serialize(),
            'tags': (tag.serialize() for tag in self.tags.all()),
            'url': self.url,
        }
        return post
