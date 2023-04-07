from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

def homePost(request):
    # Create variable to store choice that is recognized through entire function.
    education = -999
    self_emp = -999
    app_inc = -999
    co_inc = -999
    prop = -999
    try:
        # Extract value from request object by control name.
        currentEducation = request.POST['education']
        # Crude debugging effort.
        print("*** Education: " + str(currentEducation))
        education = int(currentEducation)

        currentEmp = request.POST['self_emp']
        print("*** self employed: " + str(currentEmp))
        self_emp = int(currentEmp)

        currentInc = request.POST['app_inc']
        print("*** app income: " + str(currentInc))
        app_inc = int(currentInc)

        currentCoInc = request.POST['co_inc']
        print("*** co inc: " + str(currentCoInc))
        co_inc = int(currentCoInc)

        currentProp = request.POST['prop']
        print("*** property: " + str(currentProp))
        prop = int(currentProp)
    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage':'*** The choice was missing please try again',
            'education': ['Graduate', 'Not Graduate', ],
            'self_emp': ['Yes', 'No'],
            'prop': ['Rural', 'Urban', 'Semiurban'],
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(education, self_emp, app_inc, co_inc, prop,)))


import pickle
import sklearn
import pandas as pd
def results(request, education, self_emp, app_inc, co_inc, prop):
    print("*** Inside reults()")
    with open('./model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)
    # Create a single prediction.
    singleSampleDf = pd.DataFrame(
        columns=['Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'Property_Area'])
    # education = 1
    # self_emp = 0
    # app_inc = 4000
    # co_inc = 0
    # prop = 1
    img = ''
    text = ''
    data = {'Education': education, 'Self_Employed': self_emp, 'ApplicantIncome': app_inc, 'CoapplicantIncome': co_inc,
            'Property_Area': prop}
    singleSampleDf = pd.concat([singleSampleDf, pd.DataFrame.from_records([data])])
    print(singleSampleDf)
    singlePrediction = loadedModel.predict(singleSampleDf)
    if singlePrediction == 1:
        img = 'https://static.vecteezy.com/system/resources/previews/002/743/514/original/green-check-mark-icon-in-a-circle-free-vector.jpg'
        text = "Congratulations! This model predicts you will be approved for a loan."
    else:
        img = 'https://p.kindpng.com/picc/s/503-5036239_red-x-mark-icon-good-mark-hd-png.png'
        text = "Sorry. This model predicts you will not be approved for a loan."
    print("Single prediction: " + str(singlePrediction))
    return render(request, 'results.html', {'education': education, 'self_emp': self_emp, 'app_inc':app_inc,
                                            'co_inc': co_inc, 'prop':prop, 'prediction':singlePrediction,
                                            'img': img, 'text': text})

def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'education': ['Graduate', 'Not Graduate', ],
        'self_emp': ['Yes', 'No'],
        'prop': ['Rural', 'Urban', 'Semiurban',]})