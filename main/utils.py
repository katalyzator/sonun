import random, string, re
from django.utils.text import slugify

from slugify import slugify, Slugify, UniqueSlugify
base_slugify = Slugify(to_lower=True)

# Generate random strings for slugifier
def random_string_generator(size=15, chars=string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

# Each slug has its unique string generator
def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def validNumber(phone_number):
    pattern = re.compile("^[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{3}$", re.IGNORECASE)
    return True if phone_number.startswith('996') and pattern.match(phone_number) else False
