# views.py

from django.shortcuts import render, redirect
from .models import Drug, Stock
from .forms import DrugForm
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import Drug, Stock
from .forms import DrugForm
from django.contrib import messages


from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import CustomAuthenticationForm

def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('dashboard') 
        

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('dashboard')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'sign-in.html', {'form': form})


def add_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            drug = form.save(commit=False)
            
            # Check if a drug with the same name, generic_name, brand_name, and batch exists
            existing_drug = Drug.objects.filter(
                name=drug.name,
                generic_name=drug.generic_name,
                brand_name=drug.brand_name,
                batch=drug.batch,
                packaging_type=drug.packaging_type
            ).first()
            
            if existing_drug:
                # Update the stock quantity for the existing drug
                try:
                    stock = Stock.objects.get(drug=existing_drug)
                    stock.quantity += drug.quantity
                    stock.save()
                    messages.success(request, f'Stock for {existing_drug.name} updated successfully!')
                except Stock.DoesNotExist:
                    # If stock doesn't exist, create it
                    Stock.objects.create(drug=existing_drug, quantity=drug.quantity)
                    messages.success(request, f'Stock for {existing_drug.name} created successfully!')
            else:
                # Save the new drug instance and create a new stock entry
                drug.save()
                Stock.objects.create(drug=drug, quantity=drug.quantity)
                messages.success(request, f'Drug {drug.name} added successfully!')
            
            return redirect('add_drug')
    else:
        form = DrugForm()
    return render(request, 'add_drug.html', {'form': form})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Drug, Stock
from .forms import DrugForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Drug, Stock
from .forms import DrugForm

def drug_update(request, pk):
    drug = get_object_or_404(Drug, pk=pk)
    initial_quantity = drug.quantity
    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            updated_drug = form.save(commit=False)
            
            # Check if the updated drug matches any existing drug entry
            existing_drug = Drug.objects.filter(
                name=updated_drug.name,
                generic_name=updated_drug.generic_name,
                brand_name=updated_drug.brand_name,
                batch=updated_drug.batch,
                packaging_type=updated_drug.packaging_type
            ).exclude(pk=drug.pk).first()
            
            if existing_drug:
                # Update the stock quantity for the existing drug
                try:
                    stock = Stock.objects.get(drug=existing_drug)
                    stock.quantity += updated_drug.quantity - initial_quantity
                    stock.save()
                    messages.success(request, f'Stock for {existing_drug.name} updated successfully!')
                except Stock.DoesNotExist:
                    # If stock doesn't exist, create it
                    Stock.objects.create(drug=existing_drug, quantity=updated_drug.quantity)
                    messages.success(request, f'Stock for {existing_drug.name} created successfully!')
            else:
                # Save the updated drug instance and update the stock quantity
                updated_drug.save()
                try:
                    stock = Stock.objects.get(drug=updated_drug)
                    stock.quantity = updated_drug.quantity
                    stock.save()
                    messages.success(request, f'Drug {updated_drug.name} updated successfully!')
                except Stock.DoesNotExist:
                    Stock.objects.create(drug=updated_drug, quantity=updated_drug.quantity)
                    messages.success(request, f'Stock for {updated_drug.name} created successfully!')
            
            return redirect('stock_list')  # Adjust this to your drug list view
    else:
        form = DrugForm(instance=drug)
    return render(request, 'drug_form.html', {'form': form})



from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Drug, Stock

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Drug, Stock

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Drug, Stock
from django.contrib import messages

# Other imports and views...

def expiring_drugs(request):
    today = timezone.now().date()
    next_sixty_days = today + timedelta(days=60)

    # Query the Stock model for drugs expiring within the next 60 days
    expiring_stocks = Stock.objects.filter(drug__expiry_date__lte=next_sixty_days, drug__expiry_date__gte=today)
    
    drugs_with_stock = []
    for stock in expiring_stocks:
        drugs_with_stock.append({
            'drug': stock.drug,
            'stock_quantity': stock.quantity
        })
    
    
    for item in drugs_with_stock:
        print(f"Drug: {item['drug'].name}, Stock Quantity: {item['stock_quantity']}, Expiry Date: {item['drug'].expiry_date}")
    
    return render(request, 'expiring_drugs.html', {'drugs_with_stock': drugs_with_stock})





# views.py

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Supplier, Category, PackagingType
from .forms import SupplierForm, CategoryForm, PackagingTypeForm

# Supplier Views
def supplier_list(request):
    suppliers = Supplier.objects.all()
    paginator = Paginator(suppliers, 10)  # Show 10 suppliers per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'supplier_list.html', {'page_obj': page_obj})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier_form.html', {'form': form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('supplier_list')
    return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})

# Category Views
def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)  # Show 10 categories per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'category_list.html', {'page_obj': page_obj})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

# PackagingType Views
def packaging_type_list(request):
    packaging_types = PackagingType.objects.all()
    paginator = Paginator(packaging_types, 10)  # Show 10 packaging types per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'packaging_type_list.html', {'page_obj': page_obj})

def packaging_type_create(request):
    if request.method == 'POST':
        form = PackagingTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Packaging Type added successfully!')
            return redirect('packaging_type_list')
    else:
        form = PackagingTypeForm()
    return render(request, 'packaging_type_form.html', {'form': form})

def packaging_type_update(request, pk):
    packaging_type = get_object_or_404(PackagingType, pk=pk)
    if request.method == 'POST':
        form = PackagingTypeForm(request.POST, instance=packaging_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Packaging Type updated successfully!')
            return redirect('packaging_type_list')
    else:
        form = PackagingTypeForm(instance=packaging_type)
    return render(request, 'packaging_type_form.html', {'form': form})

def packaging_type_delete(request, pk):
    packaging_type = get_object_or_404(PackagingType, pk=pk)
    if request.method == 'POST':
        packaging_type.delete()
        messages.success(request, 'Packaging Type deleted successfully!')
        return redirect('packaging_type_list')
    return render(request, 'packaging_type_confirm_delete.html', {'packaging_type': packaging_type})


from django.shortcuts import render, get_object_or_404
from .models import Stock, Drug
from django.core.paginator import Paginator

def stock_list(request):
    stocks = Stock.objects.all()
    paginator = Paginator(stocks, 10)  # Show 10 stocks per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'stock_list.html', {'page_obj': page_obj})

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    return render(request, 'stock_detail.html', {'stock': stock})



def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Stock deleted successfully!')
        return redirect('stock_list')
    return render(request, 'stock_confirm_delete.html', {'stock': stock})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('add_drug')  # Change 'home' to the appropriate view name
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})




def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')  # Change to the appropriate view name
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def password_change_done(request):
    return render(request, 'password_change_done.html')

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Drug, Stock, Cart, CartItem, Sale
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from django.shortcuts import render
from django.db.models import Q
from .models import Drug

from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.db.models import Q

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

def search_drug(request):
    name_query = request.GET.get('name', '')
    generic_query = request.GET.get('generic_name', '')
    brand_query = request.GET.get('brand_name', '')
    description_query = request.GET.get('description', '')
    
    filters = Q()
    if name_query:
        filters |= Q(name__icontains=name_query)
    if generic_query:
        filters |= Q(generic_name__icontains=generic_query)
    if brand_query:
        filters |= Q(brand_name__icontains=brand_query)
    if description_query:
        filters |= Q(description__icontains=description_query)
    
    drugs = Drug.objects.filter(filters) if filters else Drug.objects.all()
    
    # Pagination
    paginator = Paginator(drugs, 10)  # Show 10 drugs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'name_query': name_query,
        'generic_query': generic_query,
        'brand_query': brand_query,
        'description_query': description_query
    }
    return render(request, 'search_drug.html', context)



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from .models import Drug, Cart, CartItem, Stock

def add_to_cart(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    stock = get_object_or_404(Stock, drug=drug)  # Get the stock associated with the drug
    
    cart, created = Cart.objects.get_or_create(pharmacist=request.user, defaults={'created_at': timezone.now()})
    cart_item, created = CartItem.objects.get_or_create(cart=cart, drug=drug, defaults={'quantity': 0})
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > 0 and quantity <= stock.quantity:  # Compare against stock quantity
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'Added {quantity} units of {drug.name} to cart.')
        else:
            messages.error(request, 'Invalid quantity. Please check the stock availability.')
        return redirect('view_cart')

    return render(request, 'add_to_cart.html', {'drug': drug, 'stock_quantity': stock.quantity})
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Cart, CartItem, Stock

def view_cart(request):
    cart = get_object_or_404(Cart, pharmacist=request.user)
    cart_items = cart.items.all()
    total_amount = 0
    for item in cart_items:
        stock = get_object_or_404(Stock, drug=item.drug)
        if item.quantity > stock.quantity:
            messages.error(request, f"The quantity of {item.drug.name} in your cart exceeds the available stock. Please adjust the quantity.")
            item.quantity = stock.quantity
            item.save()
        total_amount += item.quantity * item.drug.unit_price
    
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, CartItem, Sale, SaleItem, Stock

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Sale, SaleItem, Stock

def finalize_sale(request):
    cart = get_object_or_404(Cart, pharmacist=request.user)
    cart_items = cart.items.all()
    total_amount = sum(item.quantity * item.drug.unit_price for item in cart_items)
    
    sale = Sale.objects.create(pharmacist=request.user, total_amount=total_amount)
    
    for item in cart_items:
        stock = Stock.objects.get(drug=item.drug)
        if item.quantity > stock.quantity:
            messages.error(request, f"Not enough stock for {item.drug.name}.")
            return redirect('view_cart')
        
        SaleItem.objects.create(
            sale=sale,
            drug=item.drug,
            quantity=item.quantity,
            unit_price=item.drug.unit_price
        )
        
        stock.quantity -= item.quantity
        stock.save()
        item.delete()
    
    cart.delete()
    messages.success(request, 'Sale finalized successfully!')
    return redirect('generate_receipt', sale_id=sale.id)

from django.shortcuts import render, get_object_or_404
from .models import Sale, SaleItem

from django.shortcuts import render, get_object_or_404
from .models import Sale, SaleItem, CustomUser

def generate_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale_items = SaleItem.objects.filter(sale=sale)
    
    # Fetch the currently logged-in user
    user = request.user
    
   
    pharmacy_contact = "+233 000 0000"  
    pharmacy_address = "AAMUSTED - KUMASI CAMPUS"  

    context = {
        'sale': sale,
        'sale_items': sale_items,
        'user': user,
        'pharmacy_contact': pharmacy_contact,
        'pharmacy_address': pharmacy_address
    }
    return render(request, 'receipt.html', context)




from django.shortcuts import redirect, get_object_or_404
from .models import CartItem

def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart') 

from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity'))
    stock = get_object_or_404(Stock, drug=cart_item.drug)
    
    if quantity > 0 and quantity <= stock.quantity:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Updated the quantity of {cart_item.drug.name} to {quantity}.")
    else:
        messages.error(request, f"Invalid quantity for {cart_item.drug.name}. Please check the stock availability.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Sale, SaleItem

def sales_list(request):
    sales = Sale.objects.all().order_by('-sale_date')
    sales_by_date = {}
    
    for sale in sales:
        sale_date = sale.sale_date.date()
        if sale_date not in sales_by_date:
            sales_by_date[sale_date] = []
        sales_by_date[sale_date].append(sale)
    
    context = {
        'sales_by_date': sales_by_date,
    }
    
    return render(request, 'sales_list.html', context)

def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale_items = SaleItem.objects.filter(sale=sale)
    
    context = {
        'sale': sale,
        'sale_items': sale_items,
    }
    
    return render(request, 'sale_detail.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Sale, Stock, Alert

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Sale, Stock, Alert
from django.db.models import Sum

from django.db.models import Sum

def dashboard(request):
    
    recent_sales = Sale.objects.order_by('-sale_date')[:10]  # Last 10 sales
    low_stock_alerts = Alert.objects.filter(alert_type='low_stock')  # Adjust filter as needed

    # Calculate total stock across all drugs
    total_stock = Stock.objects.aggregate(total_stock=Sum('quantity'))['total_stock'] or 0
    today = timezone.now().date()
    next_sixty_days = today + timedelta(days=60)
    expiring_drugs_count = Drug.objects.filter(expiry_date__lte=next_sixty_days, expiry_date__gte=today).count()
    total_sales_today = Sale.objects.filter(sale_date__year=today.year, sale_date__month=today.month, sale_date__day=today.day).aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'recent_sales': recent_sales,
        'low_stock_alerts': low_stock_alerts,
        'total_sales': Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
         'total_sales_today': total_sales_today,
        'total_stock': total_stock,
        'expiring_drugs_count': expiring_drugs_count,
    }

    return render(request, 'dashboard.html', context)


