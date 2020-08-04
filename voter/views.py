from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from voterList.models import VoterRegistration
from django.core import serializers
from django.db.models import Count
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from json import dumps
import io
import os

@login_required
def home(request,status=None):
    voterDistribution = VoterRegistration.objects.values('state').annotate(the_count=Count('state')).order_by().values_list('state','the_count')
    voterState,votercount = [], []
    for voter in voterDistribution:
        voterState.append(voter[0].strip('&#x27;'))
        votercount.append(voter[1])
    voterState = dumps(voterState)
    return render(request, 'index.html', {"TransactionStatus": status, 'voterState':voterState,'votercount':votercount})

def submit(request):
    if request.method == 'POST' and request.FILES['img']:
        citizen = request.POST['rdcitizen']
        age = request.POST['rdage']
        name = request.POST['txtfname'] + " " + request.POST['txtlname']
        DOB = request.POST['txtdob']
        contact = request.POST['txtmob']
        address = request.POST['txtadd1'] + "--" +  request.POST['txtadd2'] + "--" + request.POST['txtadd3']
        city = request.POST['txtcity']
        state = request.POST['txtstate']
        pin = request.POST['txtpin']
        myfile = request.FILES['img']
        VoterRegistration.objects.create(Name=name,Address=address,DOB=DOB,state=state,city=city,pin=pin,citizenship=citizen,age=age,Contact=contact,image=myfile)
        return redirect('/home/Succesfull')
    else:
        return redirect('/home/Failed')

@login_required
def search(request):
    voterDistribution = VoterRegistration.objects.values('state').annotate(the_count=Count('state')).order_by().values_list('state','the_count')
    voterState,votercount = [], []
    for voter in voterDistribution:
        voterState.append(voter[0].strip('&#x27;'))
        votercount.append(voter[1])
    voterState = dumps(voterState)
    if request.method == 'POST':
        contact = request.POST['txtsearch']
        user = VoterRegistration.objects.filter(Contact=contact)
        voter_details = serializers.serialize('python',user)
        detail = {}
        if len(voter_details) == 0:
            detail['stat'] = "notexist"
        else:
            detail['stat'] = "exist"
            detail['Name'] = voter_details[0]['fields']['Name']
            detail['contact'] = voter_details[0]['fields']['Contact']
            card_url = createIDcard(voter_details[0]['fields']['Contact'])
        return render (request,'index.html',{'user':detail,'voterState':voterState,'votercount':votercount})
    return render (request,'index.html',{'voterState':voterState,'votercount':votercount})

def createIDcard(contact):
    user = VoterRegistration.objects.filter(Contact=contact)
    voter_details = serializers.serialize('python',user)
    buffer = io.BytesIO()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    width,height = 540*mm,860*mm
    filename = str(contact) + ".pdf"
    filepath = BASE_DIR + "\\static\\voterCard\\" + filename
    if os.path.exists(filepath):
        os.remove(filepath)
    c = canvas.Canvas(filepath)
    pic = BASE_DIR + "\\media\\images\\" + (voter_details[0]['fields']['image'].split('/'))[1]
    c.setPageSize((width, height))
    c.setFont('Times-Bold', 26)
    c.drawCentredString(180*mm, height-(60*mm),"Voter ID Card")
    c.drawImage(pic, 60*mm, height-(180*mm), height=100*mm, width=100*mm)
    c.setFont('Times-Bold',22)
    c.drawString(180*mm, 760*mm, "Name :")
    c.drawString(210*mm, 760*mm,voter_details[0]['fields']['Name'])
    c.drawString(180*mm, 750*mm, "Date of Birth :")
    d = str(voter_details[0]['fields']['DOB']).split("-")
    Dob = d[2]+"/"+d[1]+"/"+d[0]
    c.drawString(230*mm, 750*mm,Dob)
    c.drawString(180*mm, 740*mm, "State:")
    c.drawString(210*mm, 740*mm, voter_details[0]['fields']['state'])
    c.drawString(180*mm, 730*mm, "Unique Voter ID :")
    c.drawString(250*mm, 730*mm, str(voter_details[0]['pk']))
    c.drawString(320*mm, 680*mm, "Authorized Signature")
    c.showPage()
    c.save()
    return filename


def generateID(request,contact):
    print(contact)
    user = VoterRegistration.objects.filter(Contact=contact)
    voter_details = serializers.serialize('python',user)
    buffer = io.BytesIO()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    width,height = 540*mm,860*mm
    c = canvas.Canvas(buffer)
    pic = BASE_DIR + "\\media\\images\\" + (voter_details[0]['fields']['image'].split('/'))[1]
    c.setPageSize((width, height))
    c.setFont('Times-Bold', 26)
    c.drawCentredString(180*mm, height-(60*mm),"Voter ID Card")
    c.drawImage(pic, 60*mm, height-(180*mm), height=100*mm, width=100*mm)
    c.setFont('Times-Bold',22)
    c.drawString(180*mm, 760*mm, "Name :")
    c.drawString(210*mm, 760*mm,voter_details[0]['fields']['Name'])
    c.drawString(180*mm, 750*mm, "Date of Birth :")
    d = str(voter_details[0]['fields']['DOB']).split("-")
    Dob = d[2]+"/"+d[1]+"/"+d[0]
    c.drawString(230*mm, 750*mm,Dob)
    c.drawString(180*mm, 740*mm, "State:")
    c.drawString(210*mm, 740*mm, voter_details[0]['fields']['state'])
    c.drawString(180*mm, 730*mm, "Unique Voter ID :")
    c.drawString(250*mm, 730*mm, str(voter_details[0]['pk']))
    c.drawString(320*mm, 680*mm, "Authorized Signature")
    c.showPage()
    c.save()
    buffer.seek(0)
    print("ID Card GEnerated")
    return FileResponse(buffer, as_attachment=True, filename='voterCard.pdf')
   
def register(request):
    if request.method == 'POST':
        fname = request.POST['txtfname']
        lname = request.POST['txtlname']
        userID = request.POST['txtuser']
        pwd = request.POST['txtpwd']
        email = request.POST['txtemail']
        try:
            user= User.objects.get(username=userID)
            return render (request,'registration/register.html',{'fname':fname,'lname':lname,'userID':userID,'email':email,'availability':{'status':'Unavailable'}})            
        except User.DoesNotExist:
            user = User.objects.create_user(userID, email, pwd)
            user.first_name = fname
            user.last_name = lname
            user.save()
            return redirect ('/accounts/login/?next=/')
        
    return render (request,'registration/register.html')
