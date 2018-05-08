from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.text import slugify
from django.utils.html import format_html

from .models import *


# Register your models here.

# Customizing Products inside admin
class ProductAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:180px;height:180px;"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('image_tag', 'title', 'mini_text')
    list_filter = ('publish', 'updated',)
    date_hierarchy = 'publish'
    ordering = ('-publish',)
    fields = (
        'title', 'en_title', 'client_name', 'en_client_name', 'address', 'en_address', 'image', 'content', 'en_content',
        'mini_text', 'en_mini_text', 'live', 'category', 'publish',)


admin.site.register(Product, ProductAdmin)


# Customizing Service inside admin
class ServiceAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:180px;height:180px;"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('image_tag', 'title', 'mini_text')
    list_filter = ('publish',)
    date_hierarchy = 'publish'
    ordering = ('-publish',)
    fields = (
        'title', 'en_title', 'image', 'content', 'en_content', 'mini_text', 'en_mini_text', 'live', 'category',
        'publish',)


# class ServiceForm(forms.ModelForm):
#     class Meta:
#         model = Service
#         fields = (
#             'title',
#         )

#     def save(self):
#         instance = super(ServiceForm, self).save(commit=False)
#         instance.slug = slugify(instance.title)
#         instance.save()
#         return instance

admin.site.register(Service, ServiceAdmin)


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = (
            'fullname',
        )

    def save(self):
        instance = super(TestimonialForm, self).save(commit=False)
        instance.fullname = slugify(instance.fullname)
        instance.save()
        return instance


# Customizing Testimonials inside admin
class TestimonialAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:80px;height:80px;"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('image_tag', 'fullname', 'content', 'client',)
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    fields = ('fullname', 'en_fullname', 'client', 'en_client', 'image', 'small_image', 'content', 'en_content', 'live',
              'timestamp',)


admin.site.register(Testimonial, TestimonialAdmin)


# Customizing Services inside admin

class ServiceAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:80px;height:80px;"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('image_tag', 'title')
    list_filter = ('publish',)
    date_hierarchy = 'publish'
    ordering = ('-publish',)
    fields = ('title', 'en_title', 'image', 'content', 'en_content', 'live', 'publish',)


# Customizing website Head inside admin

class HeadSliderAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:80px;height:80px;"/>'.format(obj.image.url))

    list_display = ('image_tag', 'image')


# Customizing Principles inside admin

class PrincipleAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:80px;height:80px;"/>'.format(obj.image.url))

    list_display = ('image_tag', 'title')
    list_filter = ('publish',)
    date_hierarchy = 'publish'
    ordering = ('-publish',)
    fields = ('title', 'en_title', 'image', 'content', 'en_content', 'publish',)


# Customizing Contact informations inside admin

class ContactAdmin(admin.ModelAdmin):
    list_display = ('address', 'en_address', 'telephone', 'email',)


# Customizing Our Clients inside admin

class ClientAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:80px;height:80px;"/>'.format(obj.image.url))

    list_display = ('image_tag', 'name')
    list_filter = ('client_since',)
    date_hierarchy = 'client_since'
    ordering = ('-client_since',)
    fields = ('name', 'en_name', 'image', 'client_since',)


# Customizing Our Clients inside admin

class TeamAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:80px;height:80px;"/>'.format(obj.image.url))

    list_display = ('image_tag', 'name', 'position')
    list_filter = ('employee_since',)
    date_hierarchy = 'employee_since'
    ordering = ('-employee_since',)
    fields = ('name', 'en_name', 'position', 'en_position', 'image', 'employee_since',)


class ProductGalleryAdmin(admin.ModelAdmin):
    # Get the image url
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:25%;"/>'.format(obj.image.url))

    list_display = ('image_tag', 'product')


class SocialAdmin(admin.ModelAdmin):
    list_display = ('link', 'symbol')


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'en_name',)


admin.site.register(Video)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Head)
admin.site.register(YoutubeLink)
admin.site.register(HeadSlider, HeadSliderAdmin)
admin.site.register(AboutUs)
admin.site.register(Principle, PrincipleAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
