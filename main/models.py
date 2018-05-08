#! -*- coding: utf-8 -*-

import django
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import activate
from django.db.models.signals import pre_save
from embed_video.fields import EmbedVideoField
from django.utils.translation import ugettext_lazy as _

import vinaigrette
import random, string, re
from .mailer import Mailer
from .utils import unique_slug_generator, base_slugify
from .tasks import send_verification_email

mail = Mailer()


# Setter for products queries (filters)

class ProductQuerySet(models.query.QuerySet):
    # Setter depends on live status
    def not_live(self):
        return self.filter(live=False)

    # Setter depends on published datetime
    def published(self):
        return self.filter(publish__lte=timezone.now()).not_draft()


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        return self.get_queryset().published()


def upload_location():
    return settings.PRODUCTS_ROOT


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Category(models.Model):
    name = models.CharField(max_length=60)
    en_name = models.CharField(max_length=60, default='', help_text=_('Type the english translation'),
                               verbose_name='English name')

    def __str__(self):
        return '{name}'.format(name=self.name)


# # Translations
# vinaigrette.register(Category, ['name'])

class Head(models.Model):
    title_text = models.CharField(max_length=255)
    en_title_text = models.CharField(default='', max_length=255, help_text=_('Type the english translation'),
                                     verbose_name='English title text')

    def __str__(self):
        return '{title_text}'.format(title_text=self.title_text)


class YoutubeLink(models.Model):
    embed = models.CharField(max_length=20, help_text=_('Type the youtube embeded code, for example: X8Z8okhkjv8'))

    def __str__(self):
        return '{embed}'.format(embed=self.embed)


class HeadSlider(models.Model):
    image = models.ImageField(upload_to='head_slider',
                              null=True,
                              blank=False,
                              )

    def __str__(self):
        return "{}".format(self.image)


class AboutUs(models.Model):
    title = models.CharField(max_length=50)
    en_title = models.CharField(default='', max_length=60, help_text=_('Type the english translation'),
                                verbose_name='English title text')
    content = models.TextField()
    en_content = models.TextField(default='', help_text=_('Type the english translation'),
                                  verbose_name='English content')

    experience = models.IntegerField(default=1, verbose_name=_('Years of experience'))
    employees = models.IntegerField(default=1, verbose_name=_('Number of employees'))
    orders = models.IntegerField(default=1, verbose_name=_('Number of orders'))
    clients = models.IntegerField(default=1, verbose_name=_('Number of clients'))

    youtube_vid = models.CharField(max_length=20,
                                   help_text=_('Type the youtube embeded code, for example: X8Z8okhkjv8'))

    # youtube_vid = EmbedVideoField(verbose_name=_('Youtube video link'), default=None, help_text=_('For example: https://www.youtube.com/watch?v=oBT4FR84PSg'))

    def __str__(self):
        return "{title}".format(title=self.title)


class Team(models.Model):
    name = models.CharField(max_length=60)
    en_name = models.CharField(default='', max_length=60, help_text=_('Type name in english'),
                               verbose_name=_('English employee name'))
    image = models.ImageField(upload_to='team',
                              null=True,
                              blank=False
                              )
    position = models.CharField(max_length=60, verbose_name=_('Position'))
    en_position = models.CharField(default='', max_length=60, help_text=_('Type name in english'),
                                   verbose_name=_('Position in english'))
    employee_since = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{name}".format(name=self.name)


class Client(models.Model):
    name = models.CharField(max_length=60)
    en_name = models.CharField(default='', max_length=60, help_text=_('Type name in english'),
                               verbose_name='English client name')
    image = models.ImageField(upload_to='clients',
                              null=True,
                              blank=False
                              )
    client_since = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{name}".format(name=self.name)


class Social(models.Model):
    link = models.CharField(max_length=60)
    symbol = models.CharField(max_length=13,
                              help_text=_("Available") + ": vk, odnoklassniki, facebook, twitter, instagram")

    def __str__(self):
        return "{link}".format(link=self.link)


class Principle(models.Model):
    title = models.CharField(max_length=50)
    en_title = models.CharField(default='', max_length=50, help_text=_('Type in english translation'),
                                verbose_name='English title')
    image = models.ImageField(upload_to='principles',
                              null=True,
                              blank=False
                              )
    content = models.TextField()
    en_content = models.TextField(default='', help_text=_('Type in english translation'),
                                  verbose_name='English content')
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{title}".format(title=self.title)


class Contact(models.Model):
    address = models.CharField(max_length=50)
    en_address = models.CharField(max_length=50, help_text=_('Type address in english'),
                                  verbose_name='Address in english')
    telephone = models.CharField(max_length=14)
    email = models.EmailField()

    def __str__(self):
        return "{address}".format(address=self.address)


class Product(models.Model):
    title = models.CharField(max_length=120)
    en_title = models.CharField(max_length=120, help_text=_('Type in english translation'),
                                verbose_name='English title')

    client_name = models.CharField(max_length=50, blank=True)
    en_client_name = models.CharField(default='', max_length=50, blank=True, help_text=_('Type name in english'),
                                      verbose_name='English client name')
    address = models.CharField(max_length=100, blank=True)
    en_address = models.CharField(max_length=100, blank=True, help_text=_('Type address in english'),
                                  verbose_name='English address')

    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to='products',
                              null=True,
                              blank=True,
                              # width_field="width_field",
                              # height_field="height_field"
                              )

    # These fields are using if you want to adapt the size of the image

    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)

    content = models.TextField()
    en_content = models.TextField(default='', help_text=_('Type the english translation'),
                                  verbose_name='English content')

    mini_text = models.CharField(max_length=255, default=None, verbose_name=_('Material'),
                                 help_text=_('First material, Second material'))
    en_mini_text = models.CharField(max_length=255, default='', verbose_name=_('English Material'),
                                    help_text=_('Type in english, For example: First material, Second material'))

    live = models.BooleanField(default=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # We don't need cascading because we are using soft delete.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

    objects = ProductManager()

    def save(self):
        super(Product, self).save()
        title = self.title
        self.slug = '{instance}'.format(
            instance=base_slugify(title)
        )
        super(Product, self).save()

    @models.permalink
    def get_absolute_url(self):
        return 'main:project', (self.slug,)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return "{title}".format(title=self.title)

    def as_list(self):
        if django.utils.translation.get_language() == 'en':
            return self.en_mini_text.split(',')
        else:
            return self.mini_text.split(',')

    class Meta:
        ordering = ["-publish", "-updated"]


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('The product'),
                                help_text=_('Choose a project'))
    image = models.ImageField(upload_to='projects_gallery',
                              null=True,
                              blank=False
                              )

    def __str__(self):
        return '{product}'.format(product=self.product.title)


class Service(models.Model):
    title = models.CharField(max_length=255)
    en_title = models.CharField(default='', max_length=255, help_text=_('Type in english'),
                                verbose_name='English title')
    slug = models.SlugField(unique=True)
    content = models.TextField()
    en_content = models.TextField(default='', help_text=_('Type the english translation'),
                                  verbose_name='English content')
    publish = models.DateTimeField(default=timezone.now)

    image = models.ImageField(upload_to='services',
                              null=False,
                              verbose_name='Service image'
                              )

    live = models.BooleanField(default=True)

    mini_text = models.CharField(max_length=255, default=None, verbose_name=_('Material'),
                                 help_text=_('First material, Second material'))
    en_mini_text = models.CharField(max_length=255, default='', verbose_name=_('English Material'),
                                    help_text=_('Type in english, For example: First material, Second material'))

    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, verbose_name=_('Category'))

    def save(self):
        super(Service, self).save()
        title = self.title
        self.slug = '{instance}'.format(
            instance=base_slugify(title)
        )
        super(Service, self).save()

    @models.permalink
    def get_absolute_url(self):
        return 'main:service', (self.slug,)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Service, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{title}'.format(title=self.title)

    def __str__(self):
        return '{title}'.format(title=self.title)

    def as_list(self):
        if django.utils.translation.get_language() == 'en':
            return self.en_mini_text.split(',')
        else:
            return self.mini_text.split(',')


class Letters(models.Model):
    fullname = models.CharField(max_length=255)
    telephone = models.CharField(max_length=14)
    email = models.EmailField()
    sent = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '{name}'.format(name=self.fullname)

    def __str__(self):
        return '{name}'.format(name=self.fullname)


class Subscribe(models.Model):
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{email}'.format(email=self.email)


class Video(models.Model):
    video = models.FileField(upload_to='videos', null=True, blank=True, verbose_name='Video')
    title = models.CharField(max_length=255, verbose_name=_('Название'), blank=True, null=True)

    def __str__(self):
        return '{title}'.format(title=self.title)


class Testimonial(models.Model):
    fullname = models.CharField(max_length=100)
    en_fullname = models.CharField(default='', max_length=100, help_text=_('Type fullname in english'),
                                   verbose_name='English fullname')
    client = models.CharField(max_length=50, help_text=_('For example: megacom, oobamarket, oshka'))
    en_client = models.CharField(default='', max_length=50, help_text=_('Type name in english'),
                                 verbose_name='English client')
    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to='testimonials',
                              null=True,
                              blank=True,
                              verbose_name='Client image'
                              )

    small_image = models.ImageField(upload_to='testimonials',
                                    null=True,
                                    blank=True,
                                    verbose_name='Logo image'
                                    )

    content = models.TextField()
    en_content = models.TextField(default='', help_text=_('Type the english translation'),
                                  verbose_name='English content')
    live = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self):
        super(Testimonial, self).save()
        name = self.fullname
        self.slug = '{instance}'.format(
            instance=base_slugify(name)
        )
        super(Testimonial, self).save()

    def __unicode__(self):
        return self.fullname

    def __str__(self):
        return "{fullname}".format(fullname=self.fullname)

    class Meta:
        ordering = ["-timestamp"]


def send_email(sender, instance, *args, **kwargs):
    get_subscribers = Subscribe.objects.order_by('-subscribed')
    if get_subscribers.count() != 0:
        for user in get_subscribers:
            mail.send_messages(subject=_('We added a new project, check it out'),
                               template='emails/customer_new_product.html',
                               # request.build_absolute_uri('/')
                               # +reverse('project', kwargs={'project_url':instance.slug}, current_app=request.resolver_match.namespace)
                               context={
                                   'project_url': 'http://sonunmebel.com/project/{slug}'.format(slug=instance.slug),
                                   'subscriber': user.email, 'contacts': Contact.objects.first()},
                               to_emails=[user.email])


pre_save.connect(send_email, sender=Product)
# pre_save.connect(pre_save_receiver, sender=Product)
# pre_save.connect(pre_save_receiver, sender=Testimonial)
# pre_save.connect(pre_save_receiver, sender=Service)
