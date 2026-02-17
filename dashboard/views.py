from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from accounts.models import User
from pets.models import Pet
from products.models import Product
from orders.models import Order
from appointments.models import Appointment
import json

@staff_member_required
def dashboard_view(request):
    """
    Admin dashboard with analytics
    """
    # Count statistics
    total_users = User.objects.filter(role='customer').count()
    total_pets = Pet.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    # Revenue calculation
    total_revenue = Order.objects.exclude(status='Cancelled').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Low stock products
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=F('low_stock_threshold')
    )[:10]
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    # Monthly sales data (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_sales = Order.objects.filter(
        created_at__gte=six_months_ago,
        status__in=['Processing', 'Shipped', 'Delivered']
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    ).order_by('month')
    
    # Prepare chart data
    months = []
    revenues = []
    for sale in monthly_sales:
        months.append(sale['month'].strftime('%B %Y'))
        revenues.append(float(sale['total']))
    
    # Order status distribution
    status_distribution = Order.objects.values('status').annotate(
        count=Count('id')
    )
    
    status_labels = [item['status'] for item in status_distribution]
    status_counts = [item['count'] for item in status_distribution]
    
    context = {
        'total_users': total_users,
        'total_pets': total_pets,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'chart_months': json.dumps(months),
        'chart_revenues': json.dumps(revenues),
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
    }
    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
def product_list_admin(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/product_list.html', {'products': products})

@staff_member_required
def pet_list_admin(request):
    pets = Pet.objects.all().order_by('-created_at')
    return render(request, 'dashboard/pet_list.html', {'pets': pets})

@staff_member_required
def order_list_admin(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_member_required
def appointment_list_admin(request):
    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    return render(request, 'dashboard/appointment_list.html', {'appointments': appointments})
