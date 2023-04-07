from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

def homePost(request):
    # Create variable to store choice that is recognized through entire function.
    education = -999
    credit = -999
    married = -999
    co_inc = -999
    prop = -999
    try:
        # Extract value from request object by control name.
        currentEducation = request.POST['education']
        # Crude debugging effort.
        print("*** Education: " + str(currentEducation))
        education = int(currentEducation)

        currentCredit = request.POST['credit']
        print("*** self employed: " + str(currentCredit))
        credit = int(currentCredit)

        currentMarried = request.POST['married']
        print("*** app income: " + str(currentMarried))
        married = int(currentMarried)

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
            'credit': ['Yes', 'No'],
            'Married': ['Yes', 'No'],
            'prop': ['Rural', 'Urban', 'Semiurban'],
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(education, credit, married, co_inc, prop,)))


import pickle
import sklearn
import pandas as pd
def results(request, education, credit, married, co_inc, prop):
    print("*** Inside reults()")
    with open('./model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)
    # Create a single prediction.
    singleSampleDf = pd.DataFrame(
        columns=['Education', 'Credit_History', 'Married', 'CoapplicantIncome', 'Property_Area'])
    # education = 1
    # self_emp = 0
    # app_inc = 4000
    # co_inc = 0
    # prop = 1
    img = ''
    text = ''
    data = {'Education': education, 'Credit_History': credit, 'Married': married, 'CoapplicantIncome': co_inc,
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
    return render(request, 'results.html', {'prediction':singlePrediction,
                                            'img': img, 'text': text})

def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'education': ['Graduate', 'Not Graduate', ],
        'credit': ['Yes', 'No'],
        'married': ['Yes', 'No'],
        'prop': ['Rural', 'Urban', 'Semiurban',]})