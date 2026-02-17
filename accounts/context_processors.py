from appointments.models import Appointment
from orders.models import Order

def recent_user_data(request):
    """
    Context processor to add recent appointments and orders to context
    """
    if request.user.is_authenticated:
        recent_appointments = Appointment.objects.filter(
            user=request.user
        ).order_by('-appointment_date', '-appointment_time')[:3]
        
        recent_orders = Order.objects.filter(
            user=request.user
        ).order_by('-created_at')[:3]
        
        return {
            'recent_appointments': recent_appointments,
            'recent_orders': recent_orders,
        }
    return {}
