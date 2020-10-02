from django.shortcuts import render
import image
import boto3
import os
import base64
import json
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


# Create your views here.
def home(request):
    return render(request, 'analysis/home.html')

def analyse(request):
    if request.method == 'POST':
        fileobj = request.FILES['filepath']
        fs = FileSystemStorage()
        filePathName = fs.save(fileobj.name, fileobj)
        filePathName = fs.url(filePathName)
        testimage = '.' + filePathName
        # print(testimage)
        # img = image.load_img(testimage)
        rekognition_client = boto3.client('rekognition')
        file = open(testimage, 'rb').read()

        response = rekognition_client.detect_faces(
            Image={
                'Bytes': file
            },
            Attributes=['ALL']
        )

        # print(response['FaceDetails'])
        res = response['FaceDetails']
        # json_pretty = json.dumps(data, sort_keys=True, indent=4)
        for face in res:
            Agerangelow = face['AgeRange']['Low']
            Agerangehigh = face['AgeRange']['High']
            Gender =  face['Gender']["Value"]
            Emotion =  face['Emotions'][0]["Type"]
            Eyeglasses = face['Eyeglasses']['Value']
            print(Emotion)
            if Eyeglasses:
                Eyeglasses = "wearing glasses"
            else:
                Eyeglasses = "not wearing glasses"
            beard = face['Beard']['Value']
            if beard :
                beard = "has beard."
            else:
                beard = "does not have beard"
        for face in res:
            print(json.dumps(face, indent=4, sort_keys=True))
        context = {
            "Agerangelow": Agerangelow,
            "Agerangehigh": Agerangehigh,
            "Gender":Gender,
            "Emotion":Emotion,
            "Eyeglasses":Eyeglasses,
            "filePathName":filePathName,
            "beard":beard,
        }

        return render(request, 'analysis/analysis.html', context)
    else:
        return render(request, 'analysis/home.html')