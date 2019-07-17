from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    all_products = Product.objects.all()
    prices = {}
    index = 1
    pairs = {}
    for product in all_products:
        prices.update({index : product.price})
        index+=1
    count = 2

    for pricing in all_products:
        pairs.update({
            pricing.id: pricing.price
        })
    print(pairs)
    
    context = {
        "all_products": pairs,
        "all_prices": prices,
        "count": int(count),

    }
    var_fixed = []
    price_list = [0, 1]
    for row in context['all_prices'].items():
        var_fixed.append(list(map(str, list(row))))
    for price in var_fixed:
        price_list.append(price[1])

    context = {
        "all_products": all_products,
        "price_list": price_list,
    }

    return render(request, "store/index.html", context)


def display_checkout(request):
    print(request.session.get('order_info'))
    return render(request, "store/checkout.html")


def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    my_price = Product.objects.get(id = request.POST['price'])
    price_from_form = my_price.price
    total_charge = quantity_from_form * price_from_form

    print("Charging credit card...")
    order = Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)

    # adding all total_price in Order model
    total = Order.objects.aggregate(Sum('total_price'))
    order_total = total['total_price__sum']

    total_items = len(Order.objects.all())

    request.session['order_info'] = {
        "total_charge": str(total_charge),
        "total_items": str(total_items), 
         "order_total": str(order_total)
    }
    return redirect("/display_checkout")