from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *
from forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# @login_required()
def v_cargar_img(request):
    mi_template = loader.get_template("cargar_img.html")
    return HttpResponse(mi_template.render())

def logoutView(request):
    logout(request)
    return redirect("/")

def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(request.POST.get('next', '/cargar_imagen/'))
            else:
                messages.error(request, "Nombre de Usuario o contrasenia Incorrecto")
                return redirect("/login/")
    form = LoginForm()
    return render(request, "login.html", {"form": form})
