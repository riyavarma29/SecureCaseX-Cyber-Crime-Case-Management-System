from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Case
from accounts.models import User

@login_required
def create_case(request):
    if request.user.role != 'admin':
        messages.error(request, "Permission denied")
        return redirect('case_list')

    investigators = User.objects.filter(role='investigator')

    if request.method == "POST":
        Case.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            assigned_investigator_id=request.POST.get('investigator'),
            created_by=request.user
        )
        return redirect('case_list')

    return render(request, 'cases/create_case.html', {
        'investigators': investigators
    })

@login_required
def update_case_status(request, case_id):
    case = get_object_or_404(Case, id=case_id)

    if request.user.role not in ['admin', 'investigator']:
        messages.error(request, "Permission denied")
        return redirect('case_list')

    if request.method == "POST":
        case.status = request.POST['status']
        case.save()
        return redirect('case_list')

    return render(request, 'cases/update_status.html', {'case': case})
@login_required
def case_list(request):
    user = request.user

    if user.role == 'admin':
        cases = Case.objects.all()

    elif user.role == 'investigator':
        cases = Case.objects.filter(assigned_investigator=user)

    elif user.role == 'analyst':
        cases = Case.objects.filter(assigned_analyst=user)

    else:
        cases = Case.objects.none()

    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'user': user
    })
@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})
@login_required
def assign_investigator(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')

    case = get_object_or_404(Case, id=pk)
    investigators = User.objects.filter(role='investigator')

    if request.method == 'POST':
        investigator_id = request.POST.get('investigator')

        investigator = User.objects.get(id=investigator_id)
        case.assigned_investigator = investigator   # 🔥 THIS IS CRITICAL
        case.status = 'investigating'               # optional but recommended
        case.save()

        return redirect('case_list')

    return render(request, 'cases/assign_investigator.html', {
        'case': case,
        'investigators': investigators
    })
@login_required
def assign_analyst(request, case_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    case = get_object_or_404(Case, id=case_id)
    analysts = User.objects.filter(role='analyst')

    if request.method == 'POST':
        analyst_id = request.POST.get('analyst')
        case.assigned_analyst = User.objects.get(id=analyst_id)
        case.status = 'investigating'  
        case.save()

        messages.success(request, "Analyst assigned successfully")
        return redirect('case_list')

    return render(request, 'cases/assign_analyst.html', {
        'case': case,
        'analysts': analysts
    })

