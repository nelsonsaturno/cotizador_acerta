from weasyprint import HTML, CSS

@login required
def get_report(request):
    html_template = get_template('templates/report.html')
    user = request.user

    rendered_html = html_template.render(RequestContext(request, {'you': user})).encode(encoding="UTF-8")

    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  'css/report.css')])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return response
