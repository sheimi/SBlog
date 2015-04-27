from datetime import datetime
from os import path, listdir

from django.core.management.base import BaseCommand
from django.conf import settings
import markdown
import textile
import yaml

from sblog.models import Post, Tag, Category


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument('--post_dir',
                            dest='post_dir',
                            default=settings.DEFAULT_IMPORT_PATH,
                            help='Import path of posts')

    def handle(self, *args, **options):
        self.blog_path = path.abspath(options['post_dir'])
        # clear all post, tag and category data
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        print(self.blog_path)
        self._work_dir('')

    def _abspath(self, rpath: str) -> str:
        return path.join(self.blog_path, rpath)

    def _work_dir(self, dir_path: str):
        abs_dir_path = self._abspath(dir_path)
        files = listdir(abs_dir_path)
        for f in files:
            file_path = path.join(dir_path, f)
            abs_file_path = self._abspath(file_path)
            if path.isdir(abs_file_path):
                self._work_dir(file_path)
                continue
            if file_path.endswith('.md'):
                _save_post(MarkdownContentUtil(self._abspath(file_path)))
                continue
            if file_path.endswith('.textile'):
                _save_post(TextileContentUtil(self._abspath(file_path)))
                continue


class ContentUtil:
    def __init__(self, abs_file_path: str):
        self._abs_file_path = abs_file_path
        self._date_str = None
        self._metas = None
        self._content = None
        self._thumbnail = None

    @property
    def date_str(self) -> (str, str, str):
        if self._date_str is None:
            self._date_str = self.filename.split('-')[:3]
        return self._date_str

    @property
    def filename(self) -> str:
        return path.basename(self._abs_file_path)

    @property
    def year(self) -> str:
        return self.date_str[0]

    @property
    def month(self) -> str:
        return self.date_str[1]

    @property
    def day(self) -> str:
        return self.date_str[2]

    @property
    def metas(self) -> dict:
        if self._metas is None:
            self._read_file()
        return self._metas

    @property
    def tags(self) -> list:
        return self.metas.get('tags', [])

    @property
    def location(self) -> str:
        return self.metas.get('meta', {}).get('location', 'Home')

    @property
    def show_in_home(self) -> bool:
        return self.metas.get('home', True)

    @property
    def title(self) -> str:
        return self.metas.get('title')

    @property
    def category(self) -> str:
        return self.metas.get('category')

    @property
    def published(self) -> bool:
        return self.metas.get('published', True)

    @property
    def author(self) -> bool:
        return self.metas.get('author', 'sheimi')

    @property
    def date(self) -> datetime:
        return datetime(year=int(self.year),
                        month=int(self.month),
                        day=int(self.day))

    @property
    def url(self) -> str:
        return '/'.join(('', self.category, self.year, self.month, self.day,
                         self._html_filename()))

    @property
    def content(self) -> str:
        if self._content is None:
            self._read_file()
        return self._content

    @property
    def thumbnail(self) -> str:
        if self._thumbnail is None:
            self._read_file()
        return self._thumbnail

    def _read_file(self):
        yaml_lines = []
        content_lines = []
        with open(self._abs_file_path) as f:
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
        self._metas = yaml.load(yam_content)
        self._content = self._parse_content(''.join(content_lines))
        self._thumbnail = self._parse_content(''.join(content_thumbnail_lines))

    def _parse_content(self, content: str) -> str:
        raise NotImplementedError()

    def _html_filename(self) -> str:
        raise NotImplementedError()


class MarkdownContentUtil(ContentUtil):
    def _parse_content(self, content: str) -> str:
        return markdown.markdown(content, output_format='html5')

    def _html_filename(self):
        return self.filename[11:-2] + 'html'


class TextileContentUtil(ContentUtil):
    def _parse_content(self, content: str) -> str:
        return textile.textile(content)

    def _html_filename(self) -> str:
        return self.filename[11:-7] + 'html'


def _save_post(post: ContentUtil):
    category_obj = Category.objects.filter(name=post.category).first()
    if category_obj is None:
        category_obj = Category(name=post.category)
        category_obj.save()
    tags = []
    for tag in post.tags:
        tag_obj = Tag.objects.filter(name=tag).first()
        if tag_obj is None:
            tag_obj = Tag(name=tag)
            tag_obj.save()
        tags.append(tag_obj)

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
    for tag_obj in tags:
        post_obj.tags.add(tag_obj)
