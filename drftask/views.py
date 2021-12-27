from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
import PIL
from PIL import Image
from tkinter.filedialog import *

from django.core.files import File
from django.shortcuts import render, redirect


from rest_framework.generics import ListAPIView
# Create your views here.


@api_view(['GET'])
def apioverview(request):
    api_urls = {
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
    }
    return Response(api_urls)
    # return JsonResponse("API",safe=False)


@api_view(['GET'])
def taskList(request):
    tasks= Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response("Item deleted successfully")


@api_view(['GET'])
def assignDetail(request):
    assignment = Assignment.objects.get(id=1)
    # tasks = assignment.get_task
    # print(tasks)
    # serializer=TaskSerializer(tasks, many=True)
    serializer = AssignmentSerializer(assignment, many=False)
    # serializer.IsReference = False;
    # return Response(serializer.data)
    return Response(serializer.data)
    # return Response("hello")


@api_view(['GET'])
def nestedcategory(request):
    # category = Category.objects.all()
    category = Category.objects.filter(title='Blackduck')
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def favourite(request):
    user = request.user
    # print(user)
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True, context={'user': user})
    # return Response(serializer.da3ta, context={'user': user})
    return Response(serializer.data)
    # print(product)
    # product1 = Favourite.objects.filter(user=user)
    # fav = []
    # notfav = []
    # for x in product1:
    #     # y = x.id
    #     prod = Product.objects.get(id=x.id)
    #     fav.append(prod)
    # # print(fav)
    #
    # notfav = [i for i in product if i not in fav]
    # # print(notfav)


@api_view(['POST'])
def createorder(request):
    # print(request.data)
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def getorder(request):
    tasks = Order.objects.all()
    serializer = OrderSerializer(tasks, many=True)
    return Response(serializer.data)


def customerview(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get_or_create(name=user, email='misbah@gmail.com')
        print(customer)
    return HttpResponse("yes")


@api_view(['GET'])
def customerorder(request):
    print(request.data)
    # customer = Customer.objects.all()
    # print(customer)
    customer = Customer.objects.filter(name='misbah')
    for x in customer:
        print(x.customorder)
        # order = Order.objects.get(id=x.customorder)
        # print(order)
    serializer = CustomerSerializer(customer, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def rating(request):
    mostfav = Rproducts.objects.filter(most_fav=True)
    fav = Rproducts.objects.filter(fav=True)
    leastfav = Rproducts.objects.filter(least=True)
    serializer1 = RproductSerializer(mostfav, many=True)
    serializer2 = RproductSerializer(fav, many=True)
    serializer3 = RproductSerializer(leastfav, many=True)
    response = dict()
    response['most_fav'] = serializer1.data
    response['fav'] = serializer2.data
    response['least'] = serializer3.data
    return Response(response)


class StandardPage(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data,
        })


class RatingView(generics.ListAPIView):
    queryset = Rproducts.objects.all()
    serializer_class = RproductSerializer
    pagination_class = StandardPage


@api_view(['GET'])
def ratingviewfun(request):
    paginator = StandardPage()
    # pages.page_size = 1
    # pages.max_page_size = 10
    query_set = Rproducts.objects.all().order_by('id')
    final = paginator.paginate_queryset(query_set, request)
    # print(final)
    serializer = RproductSerializer(final, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def postview(request):
    print(request.data)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_post(request):
    # print(request.data)
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        post_data = serializer.save()
    serializer1 = GetPostSerializer(post_data)
    # print(serializer.data)
    return Response(serializer1.data)


def create_assignment(request):
    myassignment = Assignment.objects.create(title='BlackOrchids3', submdate='2021-12-17 00:00:00', marks=10)
    request.session['my_assignment'] = myassignment.id
    request.session.set_expiry(60)
    return HttpResponse("Assignment created successfully")


def create_task(request):
    contains = 'my_assignment' in request.session
    print(contains)
    latestassignment = request.session['my_assignment']
    # print(latestassignment)
    # latestassignment = Assignment.objects.latest('id')
    # latestassignment = Assignment.objects.last()
    latestassignment1 = Assignment.objects.get(id=latestassignment)
    ctask = Task.objects.create(name='BlackOrchidstask', completed=True, assignment=latestassignment1)
    del request.session['my_assignment']
    return HttpResponse('Task created')


def thumbnailview(request):
    image = Productthumbnail.objects.latest('id')
    imagepath = image.picture.name
    # print(image.picture.size)
    # height, width = 150, 150
    myimage = PIL.Image.open(imagepath)
    print(myimage)
    # print(myimage.size)
    height, width = myimage.size
    print(height, width)
    newdimension = (300, 300)#,150,150)
    # myimage.thumbnail(newdimension)
    left = 5
    top = height / 40
    print(top)
    right = 164
    bottom = 3 * height / 4
    # image2 = myimage.crop((left, top, right, bottom))
    # image2.show()
    # image3 = myimage.resize((150, 150))
    # print(image3.size)
    # image3.show()
    # myimage.show()
    # imagepath = image.picture.path
    # print(image)
    f = open(imagepath, 'rb') # errors="ignore")
    image.thumbnail.save(image.picture.name, File(f))
    # image.thumbnail.save(image.picture.name, image.picture)
    # print(image.thumbnail.path)
    return HttpResponse('hello')
