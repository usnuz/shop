from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from .models import *
from .serializer import *


# All categories, category via id, for admin create and delete category
@api_view(['GET'])
def categories(request):
    category_id = request.GET.get('id')
    create = request.GET.get('create')
    delete = request.GET.get('delete')
    if create is not None or delete is not None:
        if request.user.is_authenticated():
            if request.user.status == 1:
                if create is not None:
                    category = Category.objects.create(name=create)
                    ser = CategorySerializer(category)
                    return Response(ser.data)
                if delete is not None:
                    category = Category.objects.get(id=delete)
                    name = category.name
                    category.delete()
                    return Response(f'{name} deleted')
    if category_id is not None:
        ser = CategorySerializer(Category.objects.get(id=category_id))
        return Response(ser.data)
    all_category = Category.objects.all()
    ser = CategorySerializer(all_category, many=True)
    return Response(ser.data)


# Get all subcategories and filter subcategories via category id, for admin create and delete subcategory
@api_view(['GET', 'POST'])
def subcategories(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            if request.user.status == 1:
                category_id = request.POST.get('category')
                name = request.POST.get('name')
                category = Category.objects.get(id=category_id)
                new_subcategory = SubCategory.objects.create(
                    category=category,
                    name=name
                )
                ser = SubcategorySerializer(new_subcategory)
                return Response(['created', ser.data])
    category_id = request.GET.get('category-id')
    subcategory_id = request.GET.get('id')
    if subcategory_id is not None:
        if request.user.is_authenticated():
            if request.user.status == 1:
                subcategory = SubCategory.objects.get(id=subcategory_id)
                name = subcategory.name
                subcategory.delete()
                return Response(f'{name} deleted')
    if category_id is not None:
        category = Category.objects.get(id=category_id)
        filter_subcategories = SubCategory.objects.filter(category=category)
        ser = SubcategorySerializer(filter_subcategories, many=True)
        return Response(ser.data)
    all_subcategory = SubCategory.objects.all()
    ser = SubcategorySerializer(all_subcategory, many=True)
    return Response(ser.data)


# Get all products and one product via product id and filter name and price
@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            characteristics = request.POST.get('characteristics')
            # images = request.POST.get('images')
            category = request.POST.get('category')
            tags = request.POST.get('tags')
            info = request.POST.get('info')
            cat = SubCategory.objects.get(id=category)
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=cat,
            )
            for characteristic in characteristics:
                a = Characteristic.objects.get(id=characteristic)
                product.characteristics.add(a)
                product.save()
            for tag in tags:
                a = Tag.objects.get(id=tag)
                product.tags.add(a)
                product.save()
            for inf in info:
                a = Info.objects.get(id=inf)
                product.info.add(a)
                product.save()
            ser = ProductSerialier(product)
            return Response(ser.data)
    product_id = request.GET.get('id')
    search_product = request.GET.get('name')
    price_from = request.GET.get('min')
    price_to = request.GET.get('max')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    tag = request.GET.get('tag')
    a = []
    if product_id is not None:
        product = Product.objects.get(id=product_id)
        ser = ProductSerialier(product)
        a.append(ser.data)
    if search_product is not None:
        filter_products = Product.objects.filter(name__icontains=search_product)
        ser = ProductSerialier(filter_products, many=True)
        a.append(ser.data)
    if price_from is not None or price_to is not None:
        if price_from is not None and price_to is not None:
            filter_price_product = Product.objects.filter(price__range=(price_from, price_to))
            ser = ProductSerialier(filter_price_product, many=True)
            a.append(ser.data)
    if subcategory is not None:
        one_subcategory = SubCategory.objects.get(id=subcategory)
        subcategory_product = Product.objects.filter(category=one_subcategory)
        ser = ProductSerialier(subcategory_product, many=True)
        a.append(ser.data)
    if category is not None:
        one_category = Category.objectsa.get(id=category)
        category_subcategories = SubCategory.objectsa.filter(category=one_category)
        for category_subcategory in category_subcategories:
            category_product = Product.objects.filter(category=category_subcategory)
            ser = ProductSerialier(category_product, many=True)
            a.append([
                category_subcategory.name,
                ser.data,
            ])
    if tag is not None:
        one_tag = Tag.objects.get(id=tag)
        all_products = Product.objects.all()
        for one_product in all_products:
            if one_tag in one_product.tags:
                ser = ProductSerialier(one_product)
                a.append([
                    one_tag.name,
                    ser.data,
                ])
    if product_id is None and search_product is None and price_from is None and price_to is None and subcategory is None and category is None and tag is None:
        all_products = Product.objects.all()
        ser = ProductSerialier(all_products, many=True)
        return Response(ser.data)
    return Response(a)


# Create product
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    characteristics = request.POST.get('characteristics')
    # images = request.POST.get('images')
    category = request.POST.get('category')
    tags = request.POST.get('tags')
    info = request.POST.get('info')
    cat = SubCategory.objects.get(id=category)
    product = Product.objects.create(
        name=name,
        description=description,
        category=cat,
    )
    for characteristic in characteristics:
        a = Characteristic.objects.get(id=characteristic)
        product.characteristics.add(a)
        product.save()
    for tag in tags:
        a = Tag.objects.get(id=tag)
        product.tags.add(a)
        product.save()
    for inf in info:
        a = Info.objects.get(id=inf)
        product.info.add(a)
        product.save()
    ser = ProductSerialier(product)
    return Response(ser.data)


# Products slider
@api_view(['GET'])
def is_slider(request):
    is_slider_products = Product.objects.filter(is_slider=True)
    ser = ProductSerialier(is_slider_products, many=True)
    return Response(ser.data)


# Products filter via promo
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def promo(request):
    promo_code = request.GET.get('code')
    user_promo = request.GET.get('username')
    if promo_code is not None:
        a = []
        prom = Promo.objects.get(code=promo_code)
        products_promo = Product.objects.filter(promos=prom)
        ser_promo = PromoSerializer(prom).data
        ser = ProductSerialier(products_promo, many=True).data
        a.append(ser_promo)
        a.append(ser)
        return Response(a)
    if user_promo is not None:
        user = User.objects.get(username=user_promo)
        pr = []
        promos = Promo.objects.all()
        for i in promos:
            if user in i.usr.all():
                ser = PromoSerializer(i)
                pr.append(ser.data)
        return Response(pr)
    promos = Promo.objects.all()
    ser = PromoSerializer(promos, many=True)
    return Response(ser.data)


# Add wishlist and delete wishlist user's all wishlist
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def wishlist(request):
    product_id = request.GET.get('create')
    delete = request.GET.get('delete')
    if product_id is not None:
        product = Product.objects.get(id=product_id)
        user = request.user
        new_wishlist = WishList.objects.create(
            product=product,
            usr=user,
        )
        ser = WishlistSerializer(new_wishlist)
        return Response(ser.data)
    elif delete is not None:
        card = WishList.objects.get(id=delete)
        card.delete()
        return Response('Success')
    user = request.user
    card = WishList.objects.filter(usr=user)
    ser = WishlistSerializer(card, many=True)
    return Response(ser.data)


# Create card edit card delete card one card and user's cards
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cards(request):
    if request.method == 'POST':
        card_id = request.POST.get('id')
        product_id = request.POST.get('product-id')
        quantity = request.POST.get('quantity')
        user = request.user
        product = Product.objects.get(id=product_id)
        if card_id is not None:
            card = Card.objects.get(id=card_id)
            card.product = product
            card.quantity = quantity
            card.user = user
            card.save()
            ser = CardSerializer(card)
            return Response(ser.data)
        new_card = Card.objects.create(
            product=product,
            quantity=quantity,
            user=user,
        )
        ser = CardSerializer(new_card)
        return Response(ser.data)
    else:
        card_id = request.GET.get('id')
        delete = request.GET.get('delete')
        if card_id is not None:
            card = Card.objects.get(id=card_id)
            ser = CardSerializer(card)
            return Response(ser.data)
        if delete is not None:
            card = Card.objects.get(id=delete)
            card.delete()
            return Response('Success')
        user = request.user
        card = Card.objects.filter(user=user)
        ser = CardSerializer(card, many=True)
        return Response(ser.data)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity
        user_billing = request.user.address
        user_orders = Order.objects.filter(billing_detail=user_billing)
        if user_orders is not None:
            for user_order in user_orders:
                if product == user_order.product:
                    user_order.quantity += quantity
                    user_order.total += total_price
                    user_order.save()
                    ser = OrderSerializer(user_order)
                    return Response(ser.data)
        new_order = Order.order.create(
            billing_detail=user_billing,
            product=product,
            quantity=quantity,
            total=total_price,
        )
        ser = OrderSerializer(new_order)
        return Response(ser.data)
    user_billing = request.user.address
    user_orders = Order.objects.filter(billing_detail=user_billing)
    ser = OrderSerializer(user_orders, many=True)
    return Response(ser.data)
