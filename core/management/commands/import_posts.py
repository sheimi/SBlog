from django.core.management.base import BaseCommand
from os import path, listdir
from core.models import Post, Tag, Category
from datetime import datetime
from sblog.settings import DEFAULT_IMPORT_PATH
import yaml
import markdown
import textile


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.blog_path = DEFAULT_IMPORT_PATH
        if len(args) != 0:
            self.blog_path = path.abspath(args[0])
        # clear all post, tag and category data
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        self.work_dir('')

    def abspath(self, rpath):
        return path.join(self.blog_path, rpath)

    def work_dir(self, dirpath):
        abs_dirpath = self.abspath(dirpath)
        files = listdir(abs_dirpath)
        for f in files:
            filepath = path.join(dirpath, f)
            abs_filepath = self.abspath(filepath)
            if path.isdir(abs_filepath):
                self.work_dir(filepath)
                continue
            if filepath.endswith('.md'):
                self.save_post(MarkdownContentUtil(self.abspath(filepath)))
                continue
            if filepath.endswith('.textile'):
                self.save_post(TextileContentUtil(self.abspath(filepath)))
                continue

    def save_post(self, post):
        category_obj = Category.objects.filter(name=post.category).first()
        if category_obj is None:
            category_obj = Category(name=post.category)
            category_obj.save()
        tag_objs = []
        for tag in post.tags:
            tag_obj = Tag.objects.filter(name=tag).first()
            if tag_obj is None:
                tag_obj = Tag(name=tag)
                tag_obj.save()
            tag_objs.append(tag_obj)

        post_obj = Post(title=post.title,
                        author=post.author,
                        location=post.location,
                        date=post.date,
                        content=post.content,
                        content_thumbnail=post.thumbnail,
                        category=category_obj,
                        url=post.url,
                        show_in_home=post.show_in_home,
                        published=post.published)
        post_obj.save()
        for tag_obj in tag_objs:
            post_obj.tags.add(tag_obj)


class ContentUtil:

    def __init__(self, abs_filepath):
        self.read_file(abs_filepath)
        self.filename = path.basename(abs_filepath)
        date_str = self.filename[:10]
        year, month, day = date_str.split('-')

        self.tags = self.metas.get('tags', [])
        self.location = self.metas.get('meta', {}).get('location', 'Home')
        self.show_in_home = self.metas.get('home', True)
        self.title = self.metas.get('title')
        self.category = self.metas.get('category')
        self.published = self.metas.get('published', True)
        self.author = self.metas.get('author', 'sheimi')
        self.date = datetime(year=int(year),
                             month=int(month),
                             day=int(day))
        self.url = '/'.join(('', self.category, year, month, day,
                             self.html_filename(self.filename)))

    def read_file(self, abs_filepath):
        yaml_lines = []
        content_lines = []
        with open(abs_filepath) as f:
            yaml_start = False
            yaml_end = False
            for line in f:
                if not yaml_start:
                    if line.startswith('---'):
                        yaml_start = True
                    continue
                if not yaml_end:
                    if line.startswith('---'):
                        yaml_end = True
                    else:
                        yaml_lines.append(line)
                    continue
                content_lines.append(line)
        content_thumbnail_lines = content_lines
        if len(content_lines) > 10:
            content_thumbnail_lines = content_thumbnail_lines[:10]
        yam_content = ''.join(yaml_lines)
        self.metas = yaml.load(yam_content)
        self.content = self.parse_content(''.join(content_lines))
        self.thumbnail = self.parse_content(''.join(content_thumbnail_lines))


class MarkdownContentUtil(ContentUtil):

    def parse_content(self, content):
        return markdown.markdown(content, output_format='html5')

    def html_filename(self, filename):
        return filename[11:-2] + 'html'


class TextileContentUtil(ContentUtil):

    def parse_content(self, content):
        return textile.textile(content)

    def html_filename(self, filename):
        return filename[11:-7] + 'html'
