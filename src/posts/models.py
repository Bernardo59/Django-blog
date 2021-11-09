from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

# return user active on project
from django.template.defaultfilters import slugify

User = get_user_model()


# create blogpost models
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # set author with foreignkey => on_delete, article is not delete
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False, verbose_name="Publié")
    content = models.TextField(blank=True, verbose_name="Contenu")
    thumbnail = models.ImageField(blank=True, upload_to='blog', verbose_name="Image de l'article")

    class Meta:
        # set order to created_on inverse
        ordering = ['-created_on']
        verbose_name = "Article"

    # return title of article
    def __str__(self):
        return self.title

    # if slug empty, crate slug automaticaly
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    # create property for author. If do not exist, define author like "L'auteur inconnu"
    @property
    def author_or_default(self):
        if self.author:
            return self.author.username
        return "L'auteur inconnu"

    def get_absolute_url(self):
        return reverse('posts:home')
