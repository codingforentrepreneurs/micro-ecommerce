from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponseBadRequest,HttpResponse,HttpResponseRedirect
from .models import Purchase
from products.models import Product
from products.models import Product
import stripe
from cfehome.env import config
from django.urls import reverse
from django.conf import settings,urls

# stripe_pricef_id=Product.get_stripe_id(Product)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY",default=None)
stripe.api_key=STRIPE_SECRET_KEY
base_endpoint="http://127.0.0.1:8000/"



def purchase_start_view(request):
    if request.method != 'POST' or not request.user.is_authenticated:
        return HttpResponseBadRequest("Invalid request")

    handle = request.POST.get('handle')
    obj = get_object_or_404(Product, handle=handle)

    purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session['purchase_id'] = purchase.id

    success_path = reverse("purchase:success")
    cancel_path = reverse("purchase:stopped")
    success_url = f"{base_endpoint}{success_path}"  # Assuming base_endpoint is defined somewhere
    cancel_url = f"{base_endpoint}{cancel_path}"

    stripe_p_id = obj.stripe_price_id
    print(stripe_p_id)
    # try:
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price':stripe_p_id,
                    'quantity':1,
                }
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url
        )

    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()

    print(checkout_session)
        # print(stripe_price_id)

    return HttpResponseRedirect(checkout_session.url)

    # except stripe.error.StripeError as e:
    #     print(f"Stripe Error: {e.error.message}")
    #     return HttpResponseBadRequest("Error creating Checkout Session")

# def purchase_start_view(request):
    if not request.method=='POST':
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    handle=request.POST.get('handle')
    obj=Product.objects.get(handle=handle)
    
    # if stripe_price_id is None:
    #     return HttpResponseBadRequest("Something went wrong")
    purchase=Purchase.objects.create(user=request.user,product=obj)
    request.session['purchase_id']=purchase.id
    success_path=reverse("purchase:success")
    if not success_path.startswith("/"):
        success_path=f"/{success_path}"
    cancel_path=reverse("purchase:stopped")
    success_url=f"{base_endpoint}{success_path}"
    cancel_url=f"{base_endpoint}{cancel_path}"
    stripe_price_id=obj.stripe_price_id
    checkout_session=stripe.checkout.Session.create(
        line_items=[
                {
            'price_data': {
                'currency': 'usd',
                'product': stripe_price_id,
                'unit_amount': 1000,  # Replace with your actual amount in cents
            },
            'quantity':1,
            }  
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    purchase.stripe_checkout_session_id=checkout_session.id
    purchase.save()
    print(checkout_session)
    # print(success_path)
    # print(cancel_url)
    print(stripe_price_id)
    # return HttpResponse("Start")
    return HttpResponseRedirect(checkout_session.url)

def purchase_success_view(request):
    
    purchase_id=request.session.get('purchase_id')
    if purchase_id:
        purchase=Purchase.objects.get(id=purchase_id)
        purchase.completed=True
        purchase.save()
        # p=request.product
        # product_handle=request.POST.get('product')
    return redirect(reverse('/products/'))


def purchase_stopped_view(request):
    return HttpResponse('stopped')