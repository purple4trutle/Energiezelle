from django.shortcuts import render

from django.http import HttpResponse, response
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, BuildingDataForm, EnergyDataForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from epanel.models import User, BuildingData, EnergyByYear
from django.core.mail import EmailMessage
from django.contrib.auth import logout as logout_user
from datetime import datetime
import epanel.calculate as calc
import traceback
import collections

import io

def datenschutz(request):
    return render(request, 'datenschutz.html')

def impressum(request):
    return render(request, 'impressum.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'message.html', {'title': "Account bestätigt!" , 'message':"Ihr Account wurde erfolgreich bestätigt. Sie können sich nun <a href='/accounts/login/'>hier</a> anmelden."})
    else:
        return render(request, 'message.html', {'title': "Fehler!" , 'message':"Der von Ihnen verwendete Link ist ungültig."})

def signup(request):

    if request.user.is_authenticated:
        return redirect('/overview')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account für das Energiepanel bestätigen.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'message.html', {'title': "E-Mail verschickt" , 'message':"Ihnen wurde eine E-Mail mit einem Link zum Bestätigen Ihrer Anmeldung geschickt."})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def buildingdata(request):

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        #Has the user already sumbitted a buildingdata Form? The data needs to be overwritten
        try:
            oldBuildingData = BuildingData.objects.get(user = request.user)
        except:
            oldBuildingData = None

        if oldBuildingData is None:
            form = BuildingDataForm(request.POST)
        else:
            form = BuildingDataForm(request.POST, instance=oldBuildingData)

        form.instance.user = request.user

        if form.is_valid():
            buildingdata = form.save()
            return redirect('/overview/')
        pass
    else:
        #Has the user already sumbitted a buildingdata Form? The data will populate the form
        try:
            oldBuildingData = BuildingData.objects.get(user = request.user)
        except:
            oldBuildingData = None

        if oldBuildingData is None:
            form = BuildingDataForm()
        else:
            form = BuildingDataForm(instance=oldBuildingData)

    return render(request, 'buildingdata.html', {'form': form})

def add_year(request):

    try:
        buildingData = BuildingData.objects.get(user = request.user)
    except:
        return redirect('/overview/')

    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = EnergyDataForm(request.POST)

        if form.is_valid():
            try:
                yearData = EnergyByYear.objects.filter(user = request.user, jahr=form.cleaned_data["jahr"])
            except:
                yearData = []

            if len(yearData) == 0:
                #Es existiert noch kein Eintrag mit diesem Jahr. -> Speichern und zurück zur Overview wenn valid.
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                return redirect('/overview/')

            if form.is_valid() and form.cleaned_data["acceptoverwrite"]:
                #Überschreiben
                EnergyByYear.objects.filter(user = request.user, jahr=form.cleaned_data["jahr"]).delete()
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                return redirect('/overview/')
            else:
                return render(request, 'add_year.html', {'form': form, 'error_overwrite': True})
    else:
        
        has_eigenstrom = False
        if buildingData.art_eigenstromanlage != "KEINE":
            has_eigenstrom = True

        j = request.GET.get('j', None)
        if not j is None:
            yearData = EnergyByYear.objects.filter(user = request.user, jahr=j)
            if (len(yearData) > 0):
                form = EnergyDataForm(instance=yearData[0])
            else:
                form = EnergyDataForm()
        else:
            form = EnergyDataForm()
    return render(request, 'add_year.html', {'form': form , "eigenstrom" : has_eigenstrom})

def home(request):
    user = None
    if request.user.is_authenticated:
        return redirect('/overview')

    #Render the homepage
    return render(request, 'home.html')

def logout(request):
    if request.user.is_authenticated:
        logout_user(request) 
    return render(request, 'logout.html')

def calculation(request, user = None):
    if not request.user.is_authenticated:
        return redirect('/')

    own = True
    foruser = None
    if user is None:
        user = request.user
    else:
        own = False
        foruser = user.username
    try:
        context = calc.calculate(user)
    except:
        print(traceback.format_exc())
        return render(request, 'message.html', {'title': "Fehler." , 'message':"Die Auswertung kann auf Grund von fehlenden Daten noch nicht durchgeführt werden."})
    context["own"] = own
    context["foruser"] = foruser

    #Render the homepage
    return render(request, 'calculate.html', context)

def download_pdf_old(request):
    user = None
    if not request.user.is_authenticated:
        return redirect('/')

    user = request.user
    pdf = calc.createPDF(user)
    f = io.BytesIO(pdf)
    f.seek(0)
    response = HttpResponse(f, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

def download_pdf(request , user=None):

    own = True
    foruser = None
    if user is None:
        user = request.user
    else:
        own = False
        foruser = user.username

    if not request.user.is_authenticated:
        return redirect('/')

    pdf = calc.createPDF(user)
    f = io.BytesIO(pdf)
    f.seek(0)
    response = HttpResponse(f, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

def overview(request):
    if not request.user.is_authenticated:
        return redirect('/')
    user = request.user

    context = {}

    try:
        buildingData = BuildingData.objects.get(user = user)
        context["buildingdata"] = True
    except:
        context["buildingdata"] = False

    try:
        years = EnergyByYear.objects.filter(user = user)
        context["energybyyear"] = True
        jahre = {}

        yneeded = [datetime.today().year-1,datetime.today().year-2,datetime.today().year-3]

        for y in years:
            jahre[y.jahr] = (y.jahr <= datetime.today().year-1)
            if y.jahr in yneeded: yneeded.remove(y.jahr)

        if (len(jahre) > 0):
            od = collections.OrderedDict(sorted(jahre.items()))
            context["years"] = od
        context["yearscomplete"] = len(yneeded) == 0
        context["yearsmissing"] = yneeded
    except:
        context["energybyyear"] = False


    #Render the homepage
    return render(request, 'overview.html' , context)

def calculation_admin(request, user=None):
    if not request.user.is_authenticated:
        return redirect('/')
    user = request.user
    if user.is_superuser:
        showusername = request.GET.get('username', None)
        showuser = User.objects.get(username=showusername)
        if showuser is None:
            return render(request, 'message.html', {'title': "Unbekannter Benutzer" , 'message':"Der Benutzer konnte nicht gefunden werden."})
        #show results
        try:
            return calculation(request, user=showuser)
        except:
            return render(request, 'message.html', {'title': "Fehler." , 'message':"Die Daten des Nutzers konnten nicht angezeigt werden. Gründe hierfür sind z.B. dass der Nutzer seine Daten noch nicht vollständig ausgefüllt hat."})
    else:
        return render(request, 'message.html', {'title': "Keine Berechtigung." , 'message':"Zu dieser Seite haben Sie keinen Zugriff."})

def pdf_admin(request, user=None):
    if not request.user.is_authenticated:
        return redirect('/')
    user = request.user
    if user.is_superuser:
        showusername = request.GET.get('username', None)
        showuser = User.objects.get(username=showusername)
        if showuser is None:
            return render(request, 'message.html', {'title': "Unbekannter Benutzer" , 'message':"Der Benutzer konnte nicht gefunden werden."})
        #show results
        try:
            return download_pdf(request, user=showuser)
        except:
            return render(request, 'message.html', {'title': "Fehler." , 'message':"Die Daten des Nutzers konnten nicht angezeigt werden. Gründe hierfür sind z.B. dass der Nutzer seine Daten noch nicht vollständig ausgefüllt hat."})
    else:
        return render(request, 'message.html', {'title': "Keine Berechtigung." , 'message':"Zu dieser Seite haben Sie keinen Zugriff."})