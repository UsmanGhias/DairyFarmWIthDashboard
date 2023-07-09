from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, TemplateView  # Add TemplateView import
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json
from django.http import JsonResponse
from users.models import User
from .models import Editors, Supplier, Buyer, Season, Drop, Product, Order, Delivery, Health
from .forms import SupplierForm, BuyerForm, SeasonForm, DropForm, ProductForm, OrderForm, DeliveryForm, HealthForm
from .forms import HealthForm
# Rest of the code...

# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_supplier=True)
                Supplier.objects.create(user=user, name=name, address=address)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_buyer=True)
                Buyer.objects.create(user=user, name=name, address=address)
                return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addbuyer.html', context)


class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


# Season views
@login_required(login_url='login')
def create_season(request):
    forms = SeasonForm()
    if request.method == 'POST':
        forms = SeasonForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('season-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSeason.html', context)


class SeasonListView(ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'


# Drop views
@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('drop-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addCategory.html', context)


class DropListView(ListView):
    model = Drop
    template_name = 'store/category_list.html'
    context_object_name = 'drop'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('order-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addOrder.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addelivery.html', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'


class HealthListView(ListView):
    model = Health
    template_name = 'store/health_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['health'] = Health.objects.all().order_by('-id')
        return context


# Chart view
class EditorChartView(TemplateView):
    template_name = "store/chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Editors.objects.all()
        return context


# Corrected OrderView
@login_required(login_url='login')
def order_view(request):
    cs_no = Order.objects.filter(supplier__name='Supplier').count()
    ce_no = Order.objects.filter(product__name='product').count()
    se_no = Order.objects.filter(design='design').count()
    sec_no = Order.objects.filter(color='color').count()
    male_no = Order.objects.filter(buyer__name='Male').count()
    female_no = Order.objects.filter(season__name='Season').count()

    context = {
        'cs_no': cs_no,
        'ce_no': ce_no,
        'se_no': se_no,
        'sec_no': sec_no,
        'male_no': male_no,
        'female_no': female_no,
    }

    return render(request, 'dashboard.html', context)


def chart(request):
    developer_work_week_data = [
        {"name": "Writing Code", "y": 30.7},
        {"name": "Debugging", "y": 36.4},
        {"name": "Problem Solving", "y": 3.7},
        {"name": "Firefighting", "y": 20.1},
        {"name": "Overhead", "y": 9.1}
    ]

    return render(request, 'chart.html', {"developer_work_week_data": developer_work_week_data})


# Other view functions...

def create_health(request):
    forms = HealthForm()
    if request.method == 'POST':
        forms = HealthForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('health-list')
    context = {
        'form': forms
    }
    return render(request, 'store/health.html', context)



def chart(request):
    orders = Order.objects.values('product__name').annotate(quantity=Count('product__name')).order_by('-quantity')
    order_data = [{'product': order['product__name'], 'quantity': order['quantity']} for order in orders]
    order_data_json = json.dumps(order_data)
    return JsonResponse(order_data_json, safe=False)
