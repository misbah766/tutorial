# return any model object in a jason response
from rest_framework import serializers
from .models import *
from collections import OrderedDict
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


class TaskSerializer(serializers.ModelSerializer):
    # assignment = serializers.CharField(source='assignment.title')
    assignment = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ['name', 'completed', 'assignment']


class AssignmentSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=True)
    # task= serializers.StringRelatedField(many=True)

    class Meta:
        model = Assignment
        fields = ['title', 'submdate', 'marks', 'task']


class SubsubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsubcategory
        fields = ['title']


class SubcategorySerializer(serializers.ModelSerializer):
    subsubcategory = SubsubcategorySerializer(many=True)

    class Meta:
        model = Subcategory
        fields = ['title', 'subsubcategory']


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['title', 'code', 'subcategory']


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ['product', 'user']


class ProductSerializer(serializers.ModelSerializer):
    # product = FavouriteSerializer(many=True)
    is_fav = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['name', 'code', 'avg_rating']

    def get_is_fav(self, obj):
        user = self.context.get('user')
        print(user)
        # print(obj)
        # print(obj.id)
        # product = Product.objects.all()
        # fav1 = Favourite.objects.all()
        # print(obj.id)
        exist = Favourite.objects.filter(product_id=obj.id, user=user)
        print(exist)
        print(Favourite.objects.filter(id=obj.id, user=user))
        if exist:
            return True
        else:
            return False
        # for i in fav1:
        #     for x in product:
        #         if x == obj:
        #             return True
        #         else:
        #             return True
        # return True


class OrderitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderitem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderitemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['total_quantity', 'grand_total', 'orderitems']

    def create(self, validated_data):
        # print(validated_data)
        # print(validated_data.pop('total_quantity'))
        order_items = validated_data.pop('orderitems')
        # print(order_items)
        # print(validated_data)
        order = Order.objects.create(**validated_data)
        print(order)
        # print(x)
        for x in order_items:
            # print(x)
            # x.pop('order')
            # print(x)
            orderitem = Orderitem.objects.create(**x, order=order)
            # print(orderitem.order)
        return order


class CustomerSerializer(serializers.ModelSerializer):
    customorder = OrderSerializer(many=True)
    # orders = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ['name', 'email', 'customorder']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RproductSerializer(serializers.ModelSerializer):
    # product = ReviewSerializer(many=True)
    # avg_rating = serializers.SerializerMethodField('average_rating')

    class Meta:
        model = Rproducts
        fields = '__all__' #, 'avg_rating', 'product']

    def to_representation(self, instance):
        # print(instance)
        data = super(RproductSerializer, self).to_representation(instance)
        print(data)
        field = OrderedDict([(key, data[key]) for key in data
                             if (data[key] is not False and data[key] is not None)])
        print(field)
        return field

    def average_rating(self, obj):
        # print(obj)
        # print(obj.id)
        rate = Review.objects.filter(product_id=obj.id).values_list('rating', flat=True)
        # print(rate)
        # print(type(rate[0]))
        rate = list(rate)
        # print(rate)
        length = len(rate)
        # print(length)
        Sum = sum(rate)
        # print(Sum)
        if length > 0:
            average = Sum / length
        else:
            average = 0
        average = round(average, 3)
        print(average)
        # print(rate)
        ratelist = []
        # for x in rate:
        #     print(x)
        # print(rate)
        return average


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Postmedia
        fields = ['picture']


class PostSerializer(serializers.ModelSerializer):
    # post = MediaSerializer(many=True)
    imagelist = serializers.ListField(child=serializers.FileField(max_length=None, allow_empty_file=False, use_url=False))
    # mypicture = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False)

    class Meta:
        model = Post
        fields = '__all__'#['title', 'picture']#, 'post']

    def create(self, validated_data):
        print(validated_data)
        postmedia = validated_data.pop('imagelist')
        c = 0
        for x in postmedia:
            y = x.name
            z = y.split('.')[1]
            if z == 'jpg':# or z == 'png' or z == 'jpeg':
                c += 1
            else:
                raise serializers.ValidationError({'error': 'UnSupported Media Type'})
            if c == len(postmedia):
                create_post = Post.objects.create(**validated_data)
                for i in postmedia:
                    created_media = Postmedia.objects.create(post=create_post, picture=i)
        return create_post


class GetPostSerializer(serializers.ModelSerializer):
    post = MediaSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title', 'post']


