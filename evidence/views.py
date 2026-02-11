from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cases.models import Case, CaseAnalysis
from .models import Evidence
import hashlib
from io import BytesIO
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404, redirect
import base64

@login_required
def view_case_evidence(request, case_id):
    case = get_object_or_404(
        Case,
        id=case_id,
        assigned_investigator=request.user
    )

    evidences = case.evidences.all()

    return render(request, 'accounts/view_evidence.html', {
        'case': case,
        'evidences': evidences
    })
@login_required
def upload_evidence(request, case_id):
    case = get_object_or_404(
        Case,
        id=case_id,
        assigned_investigator=request.user
    )

    hash_code = None

    if request.method == 'POST':
        evidence = Evidence.objects.create(
            case=case,
            uploaded_by=request.user,
            file=request.FILES['file'],
            description=request.POST.get('description')
        )
        hash_code = evidence.hash_code  # ✅ NOW EXISTS

    return render(request, 'evidence/upload.html', {
        'case': case,
        'hash_code': hash_code
    })
@login_required
def generate_case_report(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    analyses = CaseAnalysis.objects.filter(case=case)
    
    if not analyses.exists():
        messages.warning(request, "No analysis exists for this case yet.")
        return redirect('assigned_cases')

    generated_time = timezone.now()

    # Convert image files to base64
    for analysis in analyses:
        for ev in analysis.case.evidences.all():
            ev.is_image = ev.file.name.lower().endswith(('.jpg', '.jpeg', '.png'))
            if ev.is_image:
                with open(ev.file.path, 'rb') as f:
                    ev.base64_data = base64.b64encode(f.read()).decode()
                    ev.mime_type = f"image/{ev.file.name.split('.')[-1].lower()}"

    # Render HTML template
    html = render_to_string('evidence/case_report.html', {
        'case': case,
        'analyses': analyses,
        'generated_time': generated_time,
    })

    # Generate PDF
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse(f"Error generating PDF: {pisa_status.err}")

    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.getvalue()
    report_hash = hashlib.sha256(pdf_bytes).hexdigest()

    # Send PDF in response
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="case_{case.id}_report.pdf"'
    response['X-Report-Hash'] = report_hash

    return response
