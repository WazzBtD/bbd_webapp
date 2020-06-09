from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/login')
def homepage_request(request):
    return render(request=request,
                  template_name="store/index.html")