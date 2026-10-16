from django.shortcuts import render
from store.models import Product
def home(request):
    products = Product.objects.filter(feature=True)
    for product in products:
        product.is_on_sale = product.price != product.old_price
    for product in products:
        # Prepare URLs for the various views of the product images
        default_view = product.images.filter(view_type='default_view').first()
        top_view = product.images.filter(view_type='top_view').first()
        side_view = product.images.filter(view_type='side_view').first()
        extra_view = product.images.filter(view_type='extra_view').first()
        product.top_view = top_view.image.url if top_view else None
        product.side_view = side_view.image.url if side_view else None
        product.extra_view = extra_view.image.url if extra_view else None
        product.default_view = default_view.image.url if default_view else None

    context = {'products': products}
    return render(request, 'home/home.html',context)

def vlog_view(request):
    return render(request, 'home/vlog.html')


def aboutus(request):
    return render(request, 'home/aboutus.html')
