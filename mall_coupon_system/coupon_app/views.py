from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from .models import Coupon
from .models import Store, UserProfile, Coupon, Purchase, UploadedDataset
from .forms import UserRegisterForm, LoginForm, StoreRegistrationForm, DatasetUploadForm, AddCustomerForm
from .ml.train_model import train_model
from .ml.predict import predict_coupon
import random
import string
from .forms import IssueCouponForm
from django.shortcuts import render, get_object_or_404
from .models import Store, Coupon, UserProfile
from django.shortcuts import render, get_object_or_404
from .models import Coupon, UserProfile
from .models import Coupon, Store
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Coupon

@require_POST
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    # Ensure the logged-in user is the store owner
    if request.user != coupon.store.store_user:
        messages.error(request, "Unauthorized action.")
        return redirect('dashboard_store')

    coupon.delete()
    messages.success(request, "Coupon deleted successfully.")
    return redirect('dashboard_store')

def issue_coupon(request, user_id):
    if 'store_id' not in request.session:
        return redirect('login_store')

    try:
        store = Store.objects.get(id=request.session['store_id'])
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)

        if request.method == 'POST':
            form = IssueCouponForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                code = generate_coupon_code()
                issued_at = timezone.now().date()

                # ✅ Validity logic based on amount
                if amount <= 199:
                    validity_date = issued_at + timedelta(days=20)
                elif amount <= 999:
                    validity_date = issued_at + relativedelta(months=2)
                else:
                    validity_date = issued_at + timedelta(days=100)
                print(validity_date)
                # ✅ Create coupon with validity_date
                Coupon.objects.create(
                    user=user_profile,
                    store=store,
                    amount=amount,
                    code=code,
                    issued_at=issued_at,
                    validity_date=validity_date
                )

                messages.success(request, f"Coupon '{code}' of ₹{amount} issued to {user.username}.")
                return redirect('dashboard_store')
        else:
            form = IssueCouponForm()

        return render(request, 'coupon_app/issue_coupon.html', {
            'form': form,
            'user': user
        })

    except (Store.DoesNotExist, User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, "Invalid store or user.")
        return redirect('dashboard_store')

def monitor_store_coupons(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    coupons = Coupon.objects.filter(store=store).select_related('user').order_by('-issued_at')
    return render(request, 'coupon_app/monitor_coupons.html', {
        'store': store,
        'coupons': coupons
    })
def view_store_coupons(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    coupons = Coupon.objects.filter(store=store).select_related('user').order_by('-issued_at')
    return render(request, 'coupon_app/view_store_coupons.html', {
        'store': store,
        'coupons': coupons
    })

def view_user_coupons(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    coupons = Coupon.objects.filter(user=user)
    return render(request, 'coupon_app/user_store_coupons.html', {'coupons': coupons})

def view_user_coupons(request, store_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    store = get_object_or_404(Store, id=store_id)
    coupons = Coupon.objects.filter(store=store, user=user_profile)

    return render(request, 'coupon_app/user_store_coupons.html', {
        'store': store,
        'coupons': coupons
    })
def generate_coupon_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ---------------------- Admin Features ----------------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_store_coupons(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    coupons = Coupon.objects.filter(store=store)
    return render(request, 'coupon_app/view_store_coupons.html', {'store': store, 'coupons': coupons})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    store.delete()
    messages.success(request, "Store deleted successfully.")
    return redirect('dashboard_admin')  # Redirect back to the admin dashboard

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_admin(request):
    stores = Store.objects.all()
    return render(request, 'coupon_app/dashboard_admin.html', {'stores': stores})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_store(request):
    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
        else:
            messages.error(request, "Form is invalid. Please check input.")
    else:
        form = StoreRegistrationForm()
    return render(request, 'coupon_app/add_store.html', {'form': form})

# ---------------------- User Registration ----------------------

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            messages.success(request, "User registered successfully. Please log in.")
            return redirect('login_user')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'coupon_app/register_user.html', {'form': form})

# ---------------------- Logins ----------------------

def login_admin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard_admin')
        else:
            return render(request, 'coupon_app/login_admin.html', {'error': 'Invalid credentials or not an admin'})
    return render(request, 'coupon_app/login_admin.html')

def login_store(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            store = Store.objects.get(username=username, password=password)
            request.session['store_id'] = store.id
            return redirect('dashboard_store')
        except Store.DoesNotExist:
            messages.error(request, "Invalid store credentials.")
    return render(request, 'coupon_app/login_store.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard_user')
            messages.error(request, "Invalid user credentials.")
    else:
        form = LoginForm()
    return render(request, 'coupon_app/login_user.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def logout_store(request):
    request.session.flush()
    return redirect('home')

# ---------------------- Dashboards ----------------------

def dashboard_store(request):
    store_id = request.session.get('store_id')
    if not store_id:
        return redirect('login_store')

    store = get_object_or_404(Store, id=store_id)
    customers = User.objects.filter(userprofile__store=store)

    # Only show coupons that still exist (exclude expired ones if needed)
    issued_coupons = Coupon.objects.filter(store=store).order_by('-issued_at')

    add_customer_form = AddCustomerForm()

    return render(request, 'coupon_app/dashboard_store.html', {
        'customers': customers,
        'issued_coupons': issued_coupons,
        'store': store,
        'add_customer_form': add_customer_form
    })



@login_required(login_url='login_user')
def dashboard_user(request):
    user_profile = UserProfile.objects.get(user=request.user)  # Fix is here
    
    search_query = request.GET.get('search', '')
    if search_query:
        stores = Store.objects.filter(name__icontains=search_query)
    else:
        stores = Store.objects.all()

    user_coupons = Coupon.objects.filter(user=user_profile)  # use user_profile instead of request.user

    return render(request, 'coupon_app/dashboard_user.html', {
        'stores': stores,
        'user_coupons': user_coupons
    })

# ---------------------- Add Customer to Store ----------------------


# ---------------------- Dataset Upload & Prediction ----------------------

def upload_and_train_dataset(request):
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['dataset_file']
            file_path = os.path.join(settings.MEDIA_ROOT, 'dataset.csv')

            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            try:
                result = train_model(file_path)
                messages.success(request, result)
                return redirect('dashboard_store')  # Redirect to store dashboard
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('upload_dataset')  # Redirect back only on failure
    else:
        form = DatasetUploadForm()
        
    return render(request, 'coupon_app/upload_dataset.html', {'form': form})


def predict_coupon_view(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            visits = int(request.POST.get('visits'))

            # Determine coupon value based on visit count
            if visits <= 3:
                final_amount = round(amount * 0.05, 2)
            elif 4 <= visits <= 7:
                final_amount = round(amount * 0.07, 2)
            else:
                final_amount = round(amount * 0.09, 2)

            return render(request, 'coupon_app/predict_coupon.html', {
                'amount': amount,
                'visits': visits,
                'final_amount': final_amount
            })

        except (ValueError, TypeError):
            messages.warning(request, "Please enter valid numeric values.")
            return redirect('predict_coupon')

    return render(request, 'coupon_app/predict_coupon.html')

# ---------------------- Home ----------------------

def home(request):
    stores = Store.objects.all()
    return render(request, 'coupon_app/home.html', {'stores': stores})

def add_customer_to_store(request):
    if 'store_id' not in request.session:
        return redirect('login_store')

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)

            if user_profile.user_type != 'customer':
                messages.error(request, 'The username provided is not a customer.')
            else:
                store = Store.objects.get(id=request.session['store_id'])
                user_profile.store = store
                user_profile.save()
                messages.success(request, f'{username} has been added to your customer list.')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile does not exist.')

    return redirect('dashboard_store')


def delete_user_from_store(request, user_id):
    if 'store_id' not in request.session:
        return redirect('login_store')

    try:
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)

        if user_profile.store and user_profile.store.id == request.session['store_id']:
            user_profile.store = None
            user_profile.save()
            messages.success(request, f"{user.username} removed from your store.")
        else:
            messages.error(request, "This user does not belong to your store.")

    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, "User not found.")

    return redirect('dashboard_store')
