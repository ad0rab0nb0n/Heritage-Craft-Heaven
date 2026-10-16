from django.shortcuts import render, redirect
from .models import Product,CartOrder, CartOrderItems
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import json
from django.utils import timezone
import random
import string

def product_list(request):
    products = Product.objects.all()
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
    return render(request, 'shop.html',  context)
def search_view(request):
    query=request.GET.get('q')
    products=Product.objects.filter(product_name__icontains=query).order_by("-date")
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
    context={'products': products,
             'query':query,
             }
    return render(request, 'search.html',context)
# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         # Handle checkout form submission
#         shipping_address = request.POST.get('shipping_address')
#         phone_number = request.POST.get('phone_number')
#         cart_items = request.session.get('cart', {})

#         # Create the Order
#         order = CartOrder.objects.create(
#             user=request.user,
#             total_price=sum([item['price'] * item['quantity'] for item in cart_items.values()]),
#             shipping_address=shipping_address,
#             phone_number=phone_number,
#         )

#         # Add products to the order
#         for item in cart_items.values():
#             product = Product.objects.get(id=item['product_id'])
#             order.product.add(product)

#         # Clear the cart
#         request.session['cart'] = {}

#         messages.success(request, 'Your order has been placed successfully!')
#         return redirect('shop')  # Redirect to the shop page or a thank you page after order placement

#     # Display checkout page
#     cart_items = request.session.get('cart', {})
#     total_price = sum([item['price'] * item['quantity'] for item in cart_items.values()])

#     return render(request, 'store/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     })
@login_required
def checkout(request):
    if request.method == 'POST':
        # Retrieve form data
        delivery_type = request.POST.get('delivery_option', 'deliver')
        payment_option = request.POST.get('payment_option', 'COD')
        delivery_address = request.POST.get('address', '')
        township = request.POST.get('township', '')
        city = request.POST.get('city', '')
        phone_number = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        # Retrieve cart data from the hidden form field
        cart_data = request.POST.get('cart_data', '{}')
        cart_items = json.loads(cart_data)



        # Validate that required fields are filled
        if not delivery_address or not township or not city or not phone_number or not email:
            messages.error(request, 'Please fill out all required fields.')
            return redirect('checkout')

        # Get the current user (assuming the user is logged in)
        user = request.user if request.user.is_authenticated else None

        # Debugging user data
        if user:
            print(f'Logged in User: {user}')
        else:
            print('User is not authenticated.')

        # Calculate total price from the cart items
        total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart_items.values())
        print(f'Total Price: {total_price}')

        # Create a new CartOrder
        order = CartOrder.objects.create(
            user=user,
            total_price=total_price,
            delivery_type=delivery_type,
            payment_option=payment_option,
            delivery_address=delivery_address,
            township=township,
            city=city,
            phone_number=phone_number,
            email=email
        )
        print(f'Order Created: {order.id}')

        # Create CartOrderItems for each item in the cart
        for item_id, item_details in cart_items.items():
            CartOrderItems.objects.create(
                order=order,
                item=item_details['name'],
                quantity=item_details['quantity'],
                price=Decimal(item_details['price']),
                total=Decimal(item_details['price']) * item_details['quantity']
            )
            print(f'Added item {item_details["name"]} to order {order.id}')

        # Clear the cart after successful checkout
        request.session['cart'] = {}
        print('Cart cleared after checkout.')

        # Display a success message and redirect to a confirmation page
        messages.success(request, 'Your order has been placed successfully!')

    return render(request, 'checkout.html')

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import json

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils import timezone
import json
import random
import string

def generate_pdf(request):
    if request.method == 'POST':
        # Get form data
        delivery_option = request.POST.get('delivery_option')
        payment_option = request.POST.get('payment_option')
        address = request.POST.get('address')
        township = request.POST.get('township')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        cart_data = request.POST.get('cart_data')

        # Parse cart data
        cart_items = json.loads(cart_data)
        total_price = sum(
            (
                Decimal(str(item['price'])) * int(item['quantity'])
                for item in cart_items.values()
            ),
            Decimal('0.00')
        )
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

        # Generate the timestamp + random alphanumeric string
        unique_id = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Create a PDF with ReportLab
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Function to draw header
        def draw_header():
            p.setFont("Helvetica-Bold", 16)
            p.drawString(40, height - 40, "Heritagecraftheaven- Order Invoice")
            p.setFont("Helvetica", 10)
            p.drawString(width - 150, height - 40, f"Date: {timezone.now().strftime('%d-%m-%Y')}")
            p.line(40, height - 50, width - 40, height - 50)  # Line below header

        # Function to draw footer
        def draw_footer():
            p.line(40, 50, width - 40, 50)  # Line above footer
            p.setFont("Helvetica-Bold", 10)
            p.drawString(40, 35, "Thank you for your purchase!")
            p.drawString(width - 200, 35, "www.heritagecraftheaven.com")

        # Draw header and footer
        draw_header()
        draw_footer()

        # Add content to the PDF
        p.setFont("Helvetica", 12)
        y = height - 100
        p.drawString(100, y, "Order Invoice")
        y -= 20
        p.drawString(100, y, f"Delivery Option: {delivery_option}")
        y -= 20
        p.drawString(100, y, f"Payment Option: {payment_option}")
        y -= 20
        p.drawString(100, y, f"Address: {address}, {township}, {city}")
        y -= 20
        p.drawString(100, y, f"Phone: {phone}")
        y -= 20
        p.drawString(100, y, f"Email: {email}")

        # Add cart items to the PDF
        y -= 40
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Cart Items:")
        y -= 20

        p.setFont("Helvetica", 12)
        for item_id, item in cart_items.items():
            price = Decimal(str(item['price']))
            quantity = int(item['quantity'])
            subtotal = price * quantity

            p.drawString(
                100, y,
                f"{item['name']} - {price:.2f} Ks x {quantity} = {subtotal:.2f} Ks"
            )
            y -= 20

        # Add total price at the bottom
        y -= 20
        p.line(100, y, width - 100, y)  # Line above total price
        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, f"Total Price: {total_price:.2f} Ks")

        # Add Order ID
        y -= 40
        p.drawString(100, y, f"Order ID: {unique_id}")

        # Finish the PDF
        p.showPage()
        p.save()

        return response
