from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, get_user_model, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from cases.models import Case, CaseAnalysis
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()

def signup_view(request):
    admin_exists = User.objects.filter(role="admin").exists()
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")
        #  password mismatch
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
        # username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")
        # BLOCK MULTIPLE ADMINS
        if role == "admin" and User.objects.filter(role="admin").exists():
            messages.error(
                request,
                "Admin already exists. You cannot register as Admin."
            )
            return redirect("signup")
        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role
        )
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")
    return render(request, "accounts/signup.html", {
        "admin_exists": admin_exists
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        users = User.objects.all().order_by('-last_login')
        context = {
            'users': users,
            'active_users': User.objects.filter(is_active=True).count(),
            'inactive_users': User.objects.filter(is_active=False).count(),
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    elif user.role == 'investigator':
        return redirect('investigator_dashboard')
    elif user.role == 'analyst':
        return render(request, 'accounts/analyst_dashboard.html')
    return redirect('login')

def manage_users(request):
    users = User.objects.all()
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        user = get_object_or_404(User, id=user_id)
        # Prevent deleting self (important)
        if action == "delete":
            if user != request.user:
                user.delete()
        elif action == "update":
            role = request.POST.get("role")
            user.role = role
            user.save()
        return redirect("manage_users")
    return render(request, "accounts/manage_users.html", {"users": users})

@login_required
def assign_investigators(request):
    return render(request, 'accounts/assign_investigators.html')

@login_required
def system_reports(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    context = {
    'total_users': User.objects.count(),
    'total_cases': Case.objects.count(),
    'open_cases': Case.objects.filter(status='open').count(),
    'investigating_cases': Case.objects.filter(status='investigating').count(),
    'closed_cases': Case.objects.filter(status='closed').count(),
}
    return render(request, 'accounts/system_reports.html', context)

@login_required
def investigator_dashboard(request):
    if request.user.role != 'investigator':
        return redirect('dashboard')
    cases = Case.objects.filter(
        assigned_investigator=request.user
    ).annotate(
    evidence_count=Count('evidences')
)
    return render(request, 'accounts/investigator_dashboard.html', {
        'cases': cases
    })

@login_required
def update_case_status(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.user.role not in ['admin', 'investigator']:
        messages.error(request, "Permission denied")
        return redirect('case_list')
    if request.method == "POST":
        status = request.POST['status']
        if status not in ['open', 'investigating', 'closed']:
            messages.error(request, "Invalid status")
            return redirect('update_case_status', case_id=case.id)
        case.status = status
        case.save()
        return redirect('case_list')
    return render(request, 'accounts/update_status.html', {'case': case})

@login_required
def analyst_dashboard(request):
    total_cases = Case.objects.count()
    analyzed_cases = CaseAnalysis.objects.filter(analyst=request.user).count()
    context = {
        'total_cases': total_cases,
        'analyzed_cases': analyzed_cases,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def analyze_case(request, case_id):
    case = get_object_or_404(Case, id=case_id, assigned_analyst=request.user)
    view_only = request.GET.get('view_only') == '1'
    # If submitting analysis and not read-only
    if request.method == 'POST' and not view_only:
        CaseAnalysis.objects.create(
            case=case,
            analyst=request.user,
            evidence_summary=request.POST['evidence'],
            insights=request.POST['insights'],
            patterns_identified=request.POST.get('patterns', ''),
            recommended_status=request.POST['recommended_status']
        )
        messages.success(request, "Analysis submitted successfully!")
        return redirect('analyst_reports')
    return render(request, 'accounts/case_analysis.html', {
        'case': case,
        'view_only': view_only
    })

@login_required
def view_case_info(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    # Fetch evidences if your template expects them
    evidences = case.evidences.all()  # adjust the related name
    return render(request, 'accounts/analyze_case.html', {
        'case': case,
        'evidences': evidences,
        'view_only': True  # flag to disable form
    })

@login_required
def analyst_case_stats(request):
    if request.user.role != 'analyst':
        return redirect('dashboard')
    # Only cases assigned to this analyst
    assigned_cases = Case.objects.filter(assigned_analyst=request.user)
    stats = {
        'total_cases': assigned_cases.count(),
        'open_cases': assigned_cases.filter(status='open').count(),
        'investigating_cases': assigned_cases.filter(status='investigating').count(),
        'closed_cases': assigned_cases.filter(status='closed').count(),
    }
    return render(request, 'accounts/case_stats.html', stats)

@login_required
def analyst_reports(request):
    analyses = CaseAnalysis.objects.filter(
        analyst=request.user
    ).select_related('case')
    return render(request, 'accounts/analyst_reports.html',{
        'analyses': analyses
    }) 

@login_required
def assigned_cases(request):
    if request.user.role != 'analyst':
        return redirect('dashboard')
    cases = Case.objects.filter(
        assigned_analyst=request.user
    )
    return render(request, 'accounts/assigned_cases.html', {
        'cases': cases
    })
