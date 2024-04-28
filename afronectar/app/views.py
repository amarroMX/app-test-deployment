from django.shortcuts import render

# Create your views here.


def index_view(request):
    context = {
        "forwared_from_ip": request.META.get("REMOTE_ADDR"),
        "forwared_for_ip": request.META.get("HTTP_X_FORWARDED_FOR"),
    }

    return render(request=request, template_name="index.html", context=context)
