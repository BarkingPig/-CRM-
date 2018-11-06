from django.shortcuts import render


# Create your views here.


def index(request):

    return render(request, 'index.html')


def salesman_index(request):

    return render(request, 'salesman/salesman.html')


def customer_index(request):

    return render(request, 'salesman/customer.html')

def student_index(request):
    print('333333333333333333333333333333333333333', dir(request))
    print('777777777777777777777777777777777777777', dir(request.user))
    return render(request, 'student/student.html')
