from django.db import models
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import DraftStateMixin, Page, RevisionMixin, Orderable
from wagtail.search import index
from wagtail.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from wagtail.admin.panels import FieldPanel
from wagtail.images.widgets import AdminImageChooser
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from django.db import models
from django.shortcuts import render

class PaymentPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['payment_url'] = '/payments/'
        return context



from wagtail.models import (
    Collection)

from .blocks import BaseStreamBlock


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        context['products'] = Product.objects.child_of(self).live()
        context['categories'] = PotteryCategory.objects.all()
        images_list = []

        for i in self.carousel_images.get_object_list():
            images_list.append(i)
        context['carousel_images'] = images_list

        return context

    def get_products_by_category(self, request, category_id=None):
        if category_id and category_id != 'all':
            products = Product.objects.filter(categories__id=category_id).select_related('category')
        else:
            products = Product.objects.all().select_related('category')

    content_panels = Page.content_panels + [

        InlinePanel('carousel_images', label='Carousel images'),

    ]

class Product(Page):
    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split('|')
                fields.append(f)
            else:
                fields.append(f)
        context['custom_fields'] = fields
        context['products'] = Product.objects.all()
        images_list = []
        for i in self.carousel_images.get_object_list():
            images_list.append(i)
        context['carousel_images'] = images_list
        return context
    sku = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    categories = ParentalManyToManyField("PotteryCategory", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('sku'),
        FieldPanel('price'),
        InlinePanel('carousel_images', label='Carousel images'),
        FieldPanel('image'),
        FieldPanel('short_description'),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        InlinePanel('custom_fields', label='Custom fields'),
    ]

class ProductCustomField(Orderable):
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        # FieldPanel("carousel_image"),
        FieldPanel('name'),
        FieldPanel('options')
    ]
    # name = models.CharField(max_length=255)
    # options = models.CharField(max_length=500, null=True, blank=True)
    #
    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]

class ProductCarousel(Orderable):
    product = ParentalKey('Product', on_delete=models.CASCADE, related_name='carousel_images')
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("carousel_image", widget=AdminImageChooser),
    ]

class HomeCarousel(Orderable):
    product = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='carousel_images')
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_text = models.CharField(
        max_length=255,
    )
    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text='Text to display on Call to Action'
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
        help_text='Choose a page to link to for the Call to Action'
    )

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel('hero_text'),
        FieldPanel('hero_cta'),
        FieldPanel('hero_cta_link')
    ]


class GalleryPage(Page):
    """
    This is a page to list locations from the selected Collection. We use a Q
    object to list any Collection created (/admin/collections/) even if they
    contain no items. In this demo we use it for a GalleryPage,
    and is intended to show the extensibility of this aspect of Wagtail
    """
    # collections-based version

    # introduction = models.TextField(help_text="Text to describe the page", blank=True)
    # image = models.ForeignKey(
    #     "wagtailimages.Image",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    # )
    # body = StreamField(
    #     BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    # )
    # collection = models.ForeignKey(
    #     Collection,
    #     limit_choices_to=~models.Q(name__in=["Root"]),
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     help_text="Select the image collection for this gallery.",
    # )
    #
    # content_panels = Page.content_panels + [
    #     FieldPanel("introduction"),
    #     FieldPanel("body"),
    #     FieldPanel("image"),
    #     FieldPanel("collection"),
    # ]


    # BaseStreamBlock - based version

    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )

    subtitle = models.CharField(blank=True, max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]



@register_setting
class SnipcartSettings(BaseSiteSetting):
    api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )

class PotteryCategory(DraftStateMixin, RevisionMixin, models.Model):

    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel("name"),
        FieldPanel('image'),

    ]

    def __str__(self):
        return self.name

    def get_products(self):
        return Product.objects.filter(category=self)

    class Meta:
        verbose_name_plural = "Pottery Categories"

