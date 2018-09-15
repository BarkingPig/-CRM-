from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def salesman_index(request):
    return render(request, 'salesman/salesman.html')


def customer_index(request):
    return render(request, 'salesman/customer.html')

def student_index(request):
    return render(request, 'student/student.html')
