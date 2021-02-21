import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dienstag.settings")
django.setup()

from product.models import BagType, BagModel, Product, Color, Size, Image, Recommendation

CSV_PATH_BagType        = './BagType.csv'
CSV_PATH_BagModel       = './BagModel.csv'
CSV_PATH_Product        = './Product.csv'
CSV_PATH_Color          = './Color.csv'
CSV_PATH_Size           = './Size.csv'
CSV_PATH_Image          = './Image.csv'
CSV_PATH_Recommendation = './Recommendation.csv'

# Bag Type DB 업로드
with open(CSV_PATH_BagType) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        BagType.objects.create(name=row[0])

# Bag Model DB 업로드
with open(CSV_PATH_BagModel) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        BagModel.objects.create(name=row[0], bag_type_id=row[1])

# Color DB 업로드
with open(CSV_PATH_Color) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Color.objects.create(name=row[0])

# # # Size DB 업로드
with open(CSV_PATH_Size) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Size.objects.create(name=row[0])

# Product DB 업로드
with open(CSV_PATH_Product) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(
            model_number=row[0],
            price=row[1],
            description=row[2],
            bag_model_id=row[3],
            color_id=row[4],
            size_id=row[5]
            )

# Image DB 업로드
with open(CSV_PATH_Image) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Image.objects.create(product_id=row[0], image_url=row[1])

# # Recommendation DB 업로드
# with open(CSV_PATH_Recommendation) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         Recommendation.objects.create(product_id=row[0], bag_model_id=row[1])
