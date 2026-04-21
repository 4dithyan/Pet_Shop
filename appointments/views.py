from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm

from pets.models import Pet

@login_required
def book_appointment(request):
    """
    Book a new appointment
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully! Awaiting approval.')
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def book_visit(request, pet_id):
    """
    Book a visit for a specific pet
    """
    pet = get_object_or_404(Pet, pk=pet_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, f'Visit booked for {pet.name} successfully! Awaiting approval.')
            return redirect('appointments:appointment_list')
    else:
        initial_data = {
            'service_type': 'Visit',
            'pet_name': pet.name,
            'notes': f"Visiting {pet.name} ({pet.breed})"
        }
        form = AppointmentForm(initial=initial_data)
    
    return render(request, 'appointments/book_visit.html', {'form': form, 'pet': pet})


@login_required
def book_adoption(request, pet_id):
    """
    Apply for pet adoption
    """
    pet = get_object_or_404(Pet, pk=pet_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, f'Adoption application for {pet.name} submitted successfully! Awaiting approval.')
            return redirect('appointments:appointment_list')
    else:
        initial_data = {
            'service_type': 'Adoption',
            'pet_name': pet.name,
            'notes': f"Applying to adopt {pet.name} ({pet.breed})"
        }
        form = AppointmentForm(initial=initial_data)
    
    return render(request, 'appointments/book_adoption.html', {'form': form, 'pet': pet})


@login_required
def appointment_list(request):
    """
    List all appointments for current user or all if staff
    """
    if request.user.is_staff:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(user=request.user)
    
    context = {
        'appointments': appointments,
    }
    return render(request, 'appointments/appointment_list.html', context)


@staff_member_required
def approve_appointment(request, pk):
    """
    Approve appointment (staff only)
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Appointment.STATUS_CHOICES):
            appointment.status = status
            appointment.save()
            messages.success(request, f'Appointment status updated to {status}!')
    return redirect(request.META.get('HTTP_REFERER', 'appointments:appointment_list'))


@login_required
def cancel_appointment(request, pk):
    """
    Cancel appointment
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permission
    if appointment.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to cancel this appointment.')
        return redirect('appointments:appointment_list')
    
    if request.method == 'POST':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.info(request, 'Appointment cancelled.')
        return redirect('appointments:appointment_list')
    
    return render(request, 'appointments/cancel_appointment.html', {'appointment': appointment})
