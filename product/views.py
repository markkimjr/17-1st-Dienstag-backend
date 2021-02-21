import json

from django.views import View
from django.http  import JsonResponse

from .models import BagType, BagModel, Product, Color, Size, Image, Recommendation

class BackpackListView(View):
    def get(self, request):
        pury_items = Product.objects.filter(bag_model=1)
        jonanza_items = Product.objects.filter(bag_model=2)

        pury_list = [
            {
                'id' : product.id,
                'image_url' : Image.objects.get(product=product.id).image_url
            } for product in pury_items
        ]

        jonanza_list = [
            {
                'id' : product.id,
                'image_url' : Image.objects.get(product=product.id).image_url
            } for product in jonanza_items
        ]
        
        return JsonResponse({'message': [pury_list, jonanza_list]}, status=200)

class ModelListView(View):
    def get(self, request):
        products        = Product.objects.all()
        recommendations = Recommendation.objects.all()

        model_list = [
            {
                'id'           : product.id,
                'image_url'    : Image.objects.get(product=product.id).image_url,
                'model_number' : product.model_number,
                'price'        : product.price,
                'color_name'   : product.color.name,
                'size_name'    : product.size.name,
                'description'  : product.description.split('/')
            } for product in products
        ]

        recommendation_list = [
            {
                'id'         : item.product.id,
                'model_name' : item.product.bag_model.name,
                'image_url'  : Image.objects.get(product=item.id).image_url,
            } for item in recommendations
        ]

        return JsonResponse({'message': [model_list, recommendation_list]}, status=200)

