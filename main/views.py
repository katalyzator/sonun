#! -*- coding: utf-8 -*-

import django, base64
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse

from django.urls import reverse
from django.utils import translation
from .tasks import send_verification_email
from .forms import SendLetter, Subscription
from .tokens_gen import account_activation_token
from django.utils.translation import ugettext_lazy as _
from .models import (
    Letters, 
    Subscribe,
    Product,
    Category,
    Testimonial,
    Service,
    Head,
    HeadSlider,
    AboutUs,
    Principle,
    Contact,
    Client,
    Social,
    Team,
    ProductGallery,
    YoutubeLink
)

import json
from .utils import validNumber
from .mailer import Mailer
from validate_email import validate_email
from htmlmin.decorators import minified_response, not_minified_response

mail = Mailer()

# Create your views here.

@minified_response
def main(request):

    data = []

    for i in Category.objects.all():
        data.append({
            'category': i,
            'products': Product.objects.filter(category=i, live=True).order_by('-publish')[:4]
        })

    testis = []

    for i in Testimonial.objects.all():
        testis.append({
            'client_image': i,
            'contents': Testimonial.objects.order_by('-timestamp')
        })

    head = Head.objects.first()
    trans_h = _(u'{}'.format(head))

    context = {
        'title':_('Home'),
        'form':SendLetter,
        'form_subscribe': Subscription,
        'pc_object': data,
        'testimonial':testis,
        'services': Service.objects.order_by('-publish'),
        'head':Head.objects.first(),
        'slider':HeadSlider.objects.all(),
        'about':AboutUs.objects.order_by('?')[:1],
        'principles':Principle.objects.order_by('-publish')[:5],
        'contacts':Contact.objects.first(),
        'socials':Social.objects.order_by('?')[:5],
        'youtube':YoutubeLink.objects.first()
        # 'svgList':['sofa.svg','shkaw.svg','office--chair.svg','stoyka.svg','Shkaf.svg','tumo4ka.svg','Table.svg','Tumbochka.svg', 'computer--table.svg']
    }

    return render(request, 'index.html', context)

@minified_response
def about(request):
    testis = []

    for i in Testimonial.objects.all():
        testis.append({
            'client_image': i,
            'contents': Testimonial.objects.order_by('-timestamp')
        })
    context = {
        'title':_('About us'),
        'form':SendLetter,
        'testimonial':testis,
        'contacts':Contact.objects.first(),
        'about':AboutUs.objects.first(),
        'socials':Social.objects.order_by('?')[:5],
        'team':Team.objects.order_by('-employee_since'),
    }
    return render(request, 'about-us.html', context)

@minified_response
def contact(request):
    context = {
        'title':_('Contact'),
        'form':SendLetter,
        'contacts':Contact.objects.first(),
        'socials':Social.objects.order_by('?')[:5],
    }
    return render(request, 'contact.html', context)

@minified_response
def catalog(request):
    data = []

    for i in Category.objects.all():
        data.append({
            'category': i,
            'products': Product.objects.filter(category=i, live=True).order_by('-publish')
        })

    testis = []

    for i in Testimonial.objects.all():
        testis.append({
            'client_image': i,
            'contents': Testimonial.objects.order_by('-timestamp')
        })

    context = {
        'title':_('Catalog'),
        'form':SendLetter,
        'pc_object': data,
        'testimonial':testis,
        'all_projects':Product.objects.order_by('-publish'),
        'contacts':Contact.objects.first(),
        'socials':Social.objects.order_by('?')[:5],
    }
    return render(request, 'catalog.html', context)

@minified_response
def project(request, slug):

    project = get_object_or_404(Product, slug=slug)
    more_products = Product.objects.filter(category__in=Category.objects.filter(name=project.category.name)).exclude(slug=slug)
    testis = []

    for i in Testimonial.objects.all():
        testis.append({
            'client_image': i,
            'contents': Testimonial.objects.order_by('-timestamp')
        })
    context = {
        'project': project,
        'title': project.title if django.utils.translation.get_language() == 'ru' else project.en_title,
        "more_products":more_products,
        'form':SendLetter,
        'testimonial':testis,
        'contacts':Contact.objects.first(),
        'socials':Social.objects.order_by('?')[:5],
        "gallery":ProductGallery.objects.filter(product__in=Product.objects.filter(id=project.id))[:4],
        "gallery_count": ProductGallery.objects.filter(product__in=Product.objects.filter(id=project.id))
    }
    return render(request, 'project.html', context)

@not_minified_response
def more_gallery(request, project_slug):
    project = get_object_or_404(Product, slug=str(project_slug))
    offset = request.GET.get('offset')
    all_galleries = ProductGallery.objects.filter(product__in=Product.objects.filter(id=project.id))

    more_products = ProductGallery.objects.filter(product__in=Product.objects.filter(id=project.id))[int(offset):]

    limit = all_galleries.count() - int(offset)
    exist_count = limit
    
    gallery = []
    for image in more_products:
        exist_count = exist_count-1
        images = {
            'gallery_image': '/media/'+json.dumps(str(image.image)),
            'limiter':True if exist_count == 0 else False
        }
        gallery.append(images)
    return JsonResponse({'count':more_products.count(), 'success':gallery})

@minified_response
def service(request, slug):

    service = get_object_or_404(Service, slug=slug)

    more_services = Service.objects.filter(category__in=Category.objects.filter(id=service.category.id)).order_by('-publish').exclude(slug=slug)
    
    testis = []

    for i in Testimonial.objects.all():
        testis.append({
            'client_image': i,
            'contents': Testimonial.objects.order_by('-timestamp')
        })
    context = {
        'service': service,
        'title':service.title if django.utils.translation.get_language() == 'ru' else service.en_title,
        "more_services":more_services,
        'form':SendLetter,
        'testimonial':testis,
        'contacts':Contact.objects.first(),
        'socials':Social.objects.order_by('?')[:5],
        'contacts':Contact.objects.first(),
    }
    return render(request, 'service.html', context)

@minified_response
def clients(request):
    context = {
        'title':_('Our clients'),
        'form':SendLetter,
        'clients': Client.objects.order_by('-client_since'),
        'socials':Social.objects.order_by('?')[:5],
        'contacts':Contact.objects.first(),
    }
    return render(request, 'clients.html', context)

@not_minified_response
def subscription(request):
    if request.method != 'POST':
        return JsonResponse({'error':_('Bad request')},400)
    if request.is_ajax():
        get_email = json.loads(request.body.decode('utf8').replace("'", '"'))
        if get_email == '':
            return JsonResponse({'error':_('* Enter your e-mail')})
        else:
            if not validate_email(get_email):
                return JsonResponse({'error':_('* Invalid e-mail address')})
            check_existance = Subscribe.objects.filter(email=get_email).first()
            if check_existance:
                return JsonResponse({'error':_('* E-mail is already token')})
            new_subscriber = Subscribe(email=get_email)
            new_subscriber.confirmed = True
            new_subscriber.save()

            mail.send_messages(subject=_('Thank you for choosing SONUN'),
                template='emails/simple.html',
                context={'subscriber': get_email,'contacts':Contact.objects.first(), 'unsubscribe':get_email},
                to_emails=[get_email])
            return JsonResponse({'message':_('Thanks for the subscription.')})

@not_minified_response
def unsubscribe(request, email):
    if not email:
        return redirect('{url}#subscribe'.format(url=request.build_absolute_uri()))
    else:
        get_email = Subscribe.objects.filter(email=email).first()
        if not get_email:
            return redirect('/#subscribe')
        get_email.delete()
        messages.success(request,_('You succesfully unsubscribed'), extra_tags='success')
        return redirect('{url}#subscribe'.format(url='/'))

@not_minified_response
def letters(request):
    if request.method == 'POST':
        form = SendLetter(request.POST or None)
        if form.is_valid():
            new_letter = Letters(
                fullname=request.POST.get('fullname'),
                telephone=request.POST.get('telephone'),
                email=request.POST.get('email')
            )
            new_letter.save()
            mail.send_messages(subject=_('New request from: {client}'),
                template='emails/new_request.html',
                context={'fullname': str(new_letter.fullname), 'telephone': new_letter.telephone.strip(), 'email': new_letter.email, 'contacts':Contact.objects.first()},
                to_emails=[settings.APP_EMAIL])
            #send_verification_email(_('New request from: {client}').format(client=request.POST.get('fullname')),request.POST.get('email'))
            messages.success(request,_('Your request sent successfully'), extra_tags='success')
            return redirect('/#contact-form')
        messages.error(request,_('All fields are required'), extra_tags='fail')
        return redirect('{url}#contact-form'.format(url=request.build_absolute_uri()))
    return redirect('index')
