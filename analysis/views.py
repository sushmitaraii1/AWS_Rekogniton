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
            Agerange = str(face['AgeRange']['Low'])
            Gender =  str(face['Gender']["Value"])
            Emotion =  str(face['Emotions'][1]["Type"])
            Sunglass = str(face['Sunglasses']['Value'])
            if Sunglass == 'True':
                sunglass = "wearing sunglass"
            else:
                sunglass = "not wearing sunglass"

        # for face in res:



        context = {
            "Agerange": Agerange,
            "Gender":Gender,
            "Emotion":Emotion,
            "Sunglass":sunglass,
            "filePathName":filePathName,
        }
        return render(request, 'analysis/analysis.html', context)
    else:
        return render(request, 'analysis/home.html')