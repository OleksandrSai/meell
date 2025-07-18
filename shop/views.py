from django.shortcuts import render


def main_page_view(request):
    return render(request, template_name='shop/main_view.html')
