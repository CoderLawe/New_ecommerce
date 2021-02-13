from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse


from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
import csv

from .models import *
from .utils import cookieCart, cartData, guestOrder
from . import forms
from .forms import *

from .forms import CustomerLoginForm


# Create your views here.

def carousel_detail(request):
    if request.method == 'POST':
        form = forms.CarouselForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.author = request.user
            instance.save()
            return redirect('store')

    else:
        form = forms.CarouselForm()

    carousel = CarouselData.objects.all()

    return render(request, 'store/carousel_edit.html', {'carousel': carousel, 'form': form})


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    # context = {'Products': products}

    carousel_content = CarouselData.objects.all()

    print(products, cartItems)
    print(carousel_content)
    return render(request, 'store/index.html',
                  {'products': products, 'cartItems': cartItems, 'carousel_content': carousel_content})


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def updateGuest_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    print(total)

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    print('total:', total)
    print('order.get_cart_total:', order.get_cart_total)
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )


    return JsonResponse('Payment Complete!', safe=False)


def Search(request):
    data = cartData(request)
    cartItems = data['cartItems']

    kw = request.GET.get("keyword")
    results = Product.objects.filter(
        Q(name__icontains=kw) | Q(price__icontains=kw))
    print(results)

    return render(request, 'store/search.html', {'cartItems': cartItems, 'results': results})


def product_detail(request, slug):
    # return HttpResponse(slug)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.get(slug=slug)
    return render(request, 'store/detail.html', {'products': products, 'cartItems': cartItems,'order':order,'items':items})


def product_create(request):
    form = CreateProduct()
    if request.method == 'POST':
        form = CreateProduct(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.author = request.user
            instance.save()
            return redirect('store')

    return render(request, 'adminpages/product_create.html', {'form': form})


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = UpdateProduct(instance=product)

    if request.method == 'POST':
        form = UpdateProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'adminpages/product_create.html', {'form': form})

def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_home')

    return render(request, 'adminpages/order_create.html', {'form': form})




def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('admin_home')

    context = {'item': product}
    return render(request, 'adminpages/delete.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('admin_home')

    context = {'item': order}
    return render(request, 'adminpages/delete_order.html', context)


def all_categories(request):
    categories = Category.objects.all()

    return render(request, 'store/categories.html', {'categories': categories})

class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("admin_home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


def admin_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('store')


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


def home_admin(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    # Add status model field
    delivered = orders.filter(complete='True').count()
    pending = orders.filter(complete='False').count()


    return render(request, 'adminpages/admin_home_page.html',
                  {'orders':orders, 'total_orders': total_orders, 'delivered': delivered,'pending':pending})


def out_for_delivery(request):
    all_orders = Order.objects.all()
    delivering = all_orders.filter(status="Out for delivery")

    total_orders = all_orders.count()
    delivered = all_orders.filter(complete='True').count()
    pending = all_orders.filter(status='Pending').count()
    context = {'delivering':delivering,'total_orders': total_orders, 'delivered': delivered, "pending": pending }

    return render(request,'adminpages/admin_outfordelivery.html',context)


def delivered(request):
    all_orders = Order.objects.all()
    done = all_orders.filter(status="Delivered")

    total_orders = all_orders.count()
    delivered = all_orders.filter(complete='True').count()
    pending = all_orders.filter(status='Pending').count()
    context = {'done':done,'total_orders': total_orders, 'delivered': delivered, "pending": pending }

    return render(request,'adminpages/admin_delivered.html',context)

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/admin_home_page.html"

    def get(self, request, *args, **kwargs):
        all_orders = Order.objects.all()
        pending_orders = Order.objects.filter(status= "Pending")
        pending = Order.objects.filter(status = "Pending")
        qs = OrderItem.objects.all()
        #order_items = Order.get_cart_items(self)
        



        total_orders = all_orders.count()
        delivered = all_orders.filter(complete='True').count()
        pending = all_orders.filter(status='Pending').count()

        context = {
            "all_orders": all_orders, 'total_orders': total_orders, 'delivered': delivered, "pending": pending,"pending_orders":pending_orders,'qs':qs
        }
        return render(request, "adminpages/admin_home_new.html", context)


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/admin_detail.html"
    model = Order
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class admin_ordering(AdminRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        orderitem = OrderItem.objects.all()
        context = {
            "order": order,
            'orderitem':orderitem
            
        }
        return render(request, "adminpages/admin_detail.html", context)




class view_customer(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        shipping = ShippingAddress.objects.all()
        context = {
            "customers": customers,
            "shipping":shipping
        }
        return render(request, "adminpages/customer_view.html", context)


def customer_view_details(request, pk):
    shipping = ShippingAddress.objects.get(id=pk)

   

    return render(request, 'adminpages/customer_view_details.html', {'shipping': shipping})
# def customer_view(request):

# customers = Customer.objects.all()

# return render(request,'adminpages/customer_view.html',{'customers':customers})

class admin_products(AdminRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            "products": products
        }
        return render(request, "adminpages/products.html", context)

class admin_orders(AdminRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        context = {
            "orders": orders
            
        }
        return render(request, "adminpages/admin_orders.html", context)

def Export(request):
    response = HttpResponse(content_type ='text/csv')

    writer = csv.writer(response)
    writer.writerow(['product','quantity'])

    order = Order.objects.all
    products = Product.objects.get('name')

    for orders in Product.objects.all(), OrderItem.objects.all(), Product.objects.all().values_list('name','quantity'):

        writer.writerow(orders)
        print (orders)
    response['content-Disposition'] = 'attachment; filename="orders.csv"'

    return response

class ClubChartView(TemplateView):
    template_name = 'adminpages/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = OrderItem.objects.all() 
        return context



