from django.conf.urls import url
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from sblog.models import Post, Tag


# Create your views here.
def home(request):
    return render(request, 'index.html')


INDEX_POST_LIMIT = 7


def dict_response(**kwargs) -> JsonResponse:
    return JsonResponse(kwargs)

def list_posts(request) -> JsonResponse:
    posts = Post.objects.filter(published=True,
                                show_in_home=True).order_by('-date').all()[:INDEX_POST_LIMIT]
    return dict_response(posts=[post.partial_serialize() for post in posts])

def posts_archive(request) -> JsonResponse:
    posts = Post.objects.order_by('-date').all()
    return dict_response(posts=[post.min_serialize() for post in posts])

def recent_posts(request) -> JsonResponse:
    limit = int(request.GET.get('limit', 6))
    posts = Post.objects\
                .filter(published=True, show_in_home=True)\
                .order_by('-date')\
                .all()[:limit]
    return dict_response(posts=[post.min_serialize() for post in posts])

def get_post(request) -> JsonResponse:
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    day = request.GET.get('day', '')
    file_ = request.GET.get('file', '')
    url = '/'.join(('', category, year, month, day, file_))
    post = get_object_or_404(Post, url=url)
    return dict_response(post=post.serialize())

def list_tags(request) -> JsonResponse:
    posts = Post.objects.order_by('-date').all()
    return dict_response(posts=[post.min_serialize() for post in posts],
                         tags=Tag.tag_cloud_data())

def default_404(request):
    raise Http404

def handle_404(request):
    raise JsonResponse({
        error_code: 404,
    })

api_urls = [
    url(r'^/posts$', list_posts),
    url(r'^/posts/archives$', posts_archive),
    url(r'^/posts/details$', get_post),
    url(r'^/posts/recent$', recent_posts),
    url(r'^/posts/tags$', list_tags),
    url(r'^', default_404),
]