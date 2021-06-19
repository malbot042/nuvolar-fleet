from django.http.response import HttpResponse



def check(request):
    """
    Dummy Test URL
    """
    return HttpResponse("ok")
