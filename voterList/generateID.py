from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.http import FileResponse
import os
import io

def IDCARD():
    buffer = io.BytesIO()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    width,height = 540*mm,860*mm
    c = canvas.Canvas(buffer)
    pic = BASE_DIR + "\\media\\images\\logo.png"
    c.setPageSize((width, height))
    c.setFont('Times-Bold', 26)
    c.drawCentredString(180*mm, height-(60*mm),"Voter ID Card")
    c.drawImage(pic, 60*mm, height-(180*mm), height=100*mm, width=100*mm)
    c.setFont('Times-Bold',22)
    c.drawString(180*mm, 760*mm, "Name :")
    c.drawString(210*mm, 760*mm,"Abhishek Agarwal")
    c.drawString(180*mm, 750*mm, "Course :")
    c.drawString(210*mm, 750*mm,"Freelancer")
    c.drawString(180*mm, 740*mm, "Branch :")
    c.drawString(210*mm, 740*mm, "CS")
    c.drawString(180*mm, 730*mm, "ADMN No :")
    c.drawString(230*mm, 730*mm, "12345")
    c.drawString(180*mm, 720*mm, "Valid Till :")
    c.drawString(230*mm, 720*mm,"8/8/2020")
    c.drawString(180*mm, 710*mm, "Date Of Birth:")
    c.drawString(230*mm, 710*mm,"20/12/1993")
    c.drawString(320*mm, 680*mm, "Authorized Signature")
    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='voterCard.pdf')