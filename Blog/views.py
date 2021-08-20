import json

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators import http

from Blog.models import Blog, Subscriber
from Yummy_site.settings import EMAIL_HOST_USER
from utility.restaurant_utility import makePaginate


@http.require_GET
def blog_page(request, page):
    """ List and paginate the all primary blogs """
    blogs = Blog.objects.filter(
        is_approved=True, is_primary=True).order_by('-created_date')
    recent = Blog.objects.filter(
        is_approved=True).order_by('-created_date')[:3]
    tags = Blog.tags.all()
    context = {
        'blogs': makePaginate(blogs, page, 3),
        'recent': recent,
        'tags': tags,
    }
    return render(request, 'blog/blogs.html', context=context)


@http.require_GET
def blog_detail(request, blog_id):
    """ Show the detail and comments of blogs """
    blog = get_object_or_404(Blog, **{'id': blog_id, 'is_approved': True})
    recent = Blog.objects.filter(
        is_approved=True).order_by('-created_date')[:3]

    context = {
        'blog': blog,
        'recent': recent,
    }
    return render(request, 'blog/post_detail.html', context=context)


@http.require_GET
def blog_tag_search(request, tag_slug, page=1):
    """ Search between tags of all blogs by tag_slug """
    blogs = Blog.objects.filter(tags__slug__in=[tag_slug]).order_by('title')
    recent = Blog.objects.filter(
        is_approved=True).order_by('-created_date')[:3]
    tags = Blog.tags.all()
    context = {
        'blogs': makePaginate(blogs, page, 3),
        'recent': recent,
        'tags': tags,
    }
    return render(request, 'blog/blogs.html', context)


@http.require_POST
def blog_search(request):
    """ Search between titles of blogs by searched_key """
    searched_key = request.POST.get('searched_key')
    if searched_key is not None:
        blogs = Blog.objects.filter(title__contains=searched_key)
        recent = Blog.objects.filter(
            is_approved=True).order_by('-created_date')[:3]
        tags = Blog.tags.all()
        context = {
            'blogs': blogs,
            'recent': recent,
            'tags': tags,
            'searched_key': searched_key,
        }
        return render(request, 'blog/blogs.html', context)
    else:
        return redirect(reverse('list_blog', kwargs={'page': 1}))


@http.require_POST
def subscribe(request):
    """ Add email to the subscriber's list """
    if request.is_ajax():
        data = {}
        received_json_data = json.loads(request.body)
        subs_email = received_json_data['email']
        if subs_email is not None:
            is_subs_exists = Subscriber.objects.filter(
                email__exact=subs_email).exists()
            if is_subs_exists is False:
                e = Subscriber.objects.create(email=subs_email)
                e.save()

                send_mail(subject="Hello new subscriber",
                          message="Now you are get the blogs via email",
                          from_email=EMAIL_HOST_USER,
                          recipient_list=[subs_email])
                data['success'] = "Subscription was successfully"

            else:
                # else => This email is on the subscriber's list.
                data['error'] = "you can't subscribe again"
        else:
            # else => Error in getting email from user
            data['error'] = 'Please try again'

        return JsonResponse(data=data, status=200)
