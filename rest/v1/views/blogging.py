from django.conf.urls import url
from django.shortcuts import get_object_or_404
from rest.v1.views import BlogView
from rest_framework.response import Response
from core.models import Post, Tag
from datetime import datetime


INDEX_POST_LIMIT = 7


class ListPostsView(BlogView):

    def get(self, request):
        posts = Post.objects.filter(published=True,
                                    show_in_home=True).order_by('-date').all()[:INDEX_POST_LIMIT]
        return Response(post.partial_serialize() for post in posts)


class ArchivesPostView(BlogView):

    def get(self, request):
        posts = Post.objects.order_by('-date').all()
        return Response(post.min_serialize() for post in posts)


class GetRecentPost(BlogView):

    def get(self, request):
        limit = int(request.GET.get('limit', 6))
        posts = Post.objects.filter(published=True,
                                    show_in_home=True)\
                            .order_by('-date')\
                .all()[:limit]
        return Response(post.min_serialize() for post in posts)


class GetPostDetailsView(BlogView):

    def get(self, request):
        category = request.GET.get('category', '')
        year = request.GET.get('year', '')
        month = request.GET.get('month', '')
        day = request.GET.get('day', '')
        file_ = request.GET.get('file', '')
        url = '/'.join(('', category, year, month, day, file_))
        post = get_object_or_404(Post, url=url)
        return Response(post.serialize())


class GetTagsPosts(BlogView):

    def get(self, request):
        posts = Post.objects.order_by('-date').all()
        return Response({
            'posts': (post.min_serialize() for post in posts),
            'tags': Tag.tag_cloud_data(),
        })


# url patterns for blogging related apis
urls = [
    url(r'^/?$', ListPostsView.as_view()),
    url(r'^/details/?$', GetPostDetailsView.as_view()),
    url(r'^/recent/?$', GetRecentPost.as_view()),
    url(r'^/archives/?$', ArchivesPostView.as_view()),
    url(r'^/tags/?$', GetTagsPosts.as_view()),
]
