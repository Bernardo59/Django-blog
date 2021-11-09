from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import BlogPost
from django.contrib.auth.decorators import login_required


# create home page with ListView class
class BlogHome(ListView):
    # model is BlogPost (in models.py)
    model = BlogPost
    # context variable
    context_object_name = "posts"

    def get_queryset(self):
        # super() replace ListView.get_qu..
        queryset = super().get_queryset()
        # if user is authenticated return all list of articles
        if self.request.user.is_authenticated:
            return queryset
        # else all articles with published is True
        return queryset.filter(published=True)


@method_decorator(login_required, name='dispatch')
class BlogHomeCreate(CreateView):
    model = BlogPost
    template_name = "posts/blogpost_create.html"
    fields = ["title", "content"]


@method_decorator(login_required, name='dispatch')
class BlogPostUpdate(UpdateView):
    model = BlogPost
    template_name = "posts/blogpost_edit.html"
    fields = ["title", "content", "published"]


class BlogPostDetail(DetailView):
    model = BlogPost
    context_object_name = "post"


@method_decorator(login_required, name='dispatch')
class BlogPostDelete(DeleteView):
    model = BlogPost
    # return home page
    success_url = reverse_lazy("posts:home")
    context_object_name = "post"


