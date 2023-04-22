from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from apps.goods.models import Product, ProductsCategory
from django.http import JsonResponse
from apps.users.models import MyUser
from apps.goods.forms import ProductInfo, ProductInfoChange, ProductPhotoChange, ProductsCategoryInfo
import os
from apps.order.models import ReviewAndRating, Order
from apps.order.forms import ReviewRatingChangeForm
from django.utils import timezone
from shoppingSystem import settings


# Create your views here.
def user_product_view(request):
    if request.method == "GET":
        datas = Product.objects.all()
        page_size = 2
        try:
            if not request.GET.get("page"):
                curr_page = 1
            curr_page = int(request.GET.get("page"))
        except:
            curr_page = 1
        paginator = Paginator(datas, page_size)
        try:
            products = paginator.page(curr_page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(1)
        return render(request, "homePage2.html", {"products": products})


def vendor_product_view(request):
    datas = Product.objects.all().order_by("product_id")
    products = Paginator(datas, 5)
    datas2 = ProductsCategory.objects.all().order_by("category_id")
    categorys = Paginator(datas2, 5)
    return render(request, "product_show.html", {"products": products, "categorys": categorys})


def product_detail(request, product_id):
    product = Product.objects.filter(product_id=product_id)
    review_ratings = ReviewAndRating.objects.filter(product_id=product_id)
    img_url = product[0].main_image
    return render(request, "product_detail2.html", {"product": product, "img_url": img_url, "review_ratings": review_ratings})


def ajax_products(request):
    print(request.GET)
    product_id = request.GET.get("product_id", '')
    product_name = request.GET.get("name", '')
    page_size = 5
    page = int(request.GET["page"])
    print(page)
    if product_name == "" and product_id == "":
        total = Product.objects.all().count()
        products = Product.objects.all().order_by("product_id")[(page - 1) * page_size: page * page_size]
        rows = []
        for product in products:
            rows.append({
                "product_id": product.product_id,
                "name": product.name,
                "temporary_status": product.temporary_status,
                "category_id": product.category.name,
                "price": product.price,
                "property1": product.property1,
                "property2": product.property2,
                "property3": product.property3,
                "property4": product.property4,
                "property5": product.property5,
                "property6": product.property6,
                "sale_number": product.sale_number,
                "sale_amount": product.sale_amount,
                "customer_rating": product.customer_rating,
                "review": product.review,
                "createDate": product.createDate
            })
        datas = {"total": total, "rows": rows}
    else:
        if product_id != "":
            total = Product.objects.filter(product_id=product_id).count()
            products = Product.objects.filter(product_id=product_id).order_by("product_id")[
                       (page - 1) * page_size: page * page_size]
        else:
            total = Product.objects.filter(name__icontains=product_name).count()
            products = Product.objects.filter(name__icontains=product_name).order_by("product_id")[
                       (page - 1) * page_size: page * page_size]
        rows = []
        for product in products:
            rows.append({
                "product_id": product.product_id,
                "name": product.name,
                "temporary_status": product.temporary_status,
                "category_id": product.category.name,
                "price": product.price,
                "property1": product.property1,
                "property2": product.property2,
                "property3": product.property3,
                "property4": product.property4,
                "property5": product.property5,
                "property6": product.property6,
                "sale_number": product.sale_number,
                "sale_amount": product.sale_amount,
                "customer_rating": product.customer_rating,
                "review": product.review,
                "createDate": product.createDate
            })

        datas = {"total": total, "rows": rows}
    return JsonResponse(datas, safe=False, json_dumps_params={'ensure_ascii': False, "indent": 4})


def product_add(request):
    if request.method == "GET":
        form_obj = ProductInfo()
        return render(request, 'product_add.html', {'form_obj': form_obj})
    if request.method == "POST":
        form_obj = ProductInfo(request.POST, request.FILES)
        if form_obj.is_valid():
            name = request.POST.get("name", '')
            category = request.POST.get("category", '')
            price = request.POST.get("price", '')
            property1 = request.POST.get("property1", '')
            property2 = request.POST.get("property2", '')
            property3 = request.POST.get("property3", '')
            property4 = request.POST.get("property4", '')
            property5 = request.POST.get("property5", '')
            property6 = request.POST.get("property6", '')
            main_image = request.FILES.get("main_image", '')
            temporary_status = request.POST.get("temporary_status", '')
            photo1 = request.FILES.get("photo1", '')
            photo2 = request.FILES.get("photo2", '')
            photo3 = request.FILES.get("photo3", '')
            photo4 = request.FILES.get("photo4", '')
            products = Product.objects.filter(name=name, price=price)
            if products:
                info = "the product has been existed"
                return render(request, 'product_add.html', {"info": info})
            else:
                form_obj.cleaned_data["name"] = name
                form_obj.cleaned_data["category"] = ProductsCategory.objects.filter(category_id=category)[0]
                form_obj.cleaned_data["price"] = price
                form_obj.cleaned_data["property1"] = property1
                form_obj.cleaned_data["property2"] = property2
                form_obj.cleaned_data["property3"] = property3
                form_obj.cleaned_data["property4"] = property4
                form_obj.cleaned_data["property5"] = property5
                form_obj.cleaned_data["property6"] = property6
                form_obj.cleaned_data["sale_number"] = 0
                form_obj.cleaned_data["sale_amount"] = 0
                form_obj.cleaned_data["main_image"] = main_image
                form_obj.cleaned_data["temporary_status"] = temporary_status
                form_obj.cleaned_data["photo1"] = photo1
                form_obj.cleaned_data["photo2"] = photo2
                form_obj.cleaned_data["photo3"] = photo3
                form_obj.cleaned_data["photo4"] = photo4
                product = Product.objects.create(**form_obj.cleaned_data)
                info = "create product successful"
                product_redirect = Product.objects.filter(name=name)[0]
                return redirect('/products/customer/' + str(product_redirect.product_id))
        else:
            errors = form_obj.errors
            print(errors)
            return render(request, "product_add.html", {"form_obj": form_obj, "errors": errors})


def product_change(request, product_id):
    product = Product.objects.filter(product_id=product_id)[0]
    print(product.temporary_status)
    if request.method == "GET":
        form_obj = ProductInfoChange()
        return render(request, "product_change.html", {"form_obj": form_obj, "product": product})
    if request.method == "POST":
        print(request.POST)
        form_obj = ProductInfoChange(request.POST, request.FILES)
        name = request.POST.get("name", '')
        category = request.POST.get("category", '')
        price = request.POST.get("price", '')
        property1 = request.POST.get("property1", '')
        property2 = request.POST.get("property2", '')
        property3 = request.POST.get("property3", '')
        property4 = request.POST.get("property4", '')
        property5 = request.POST.get("property5", '')
        property6 = request.POST.get("property6", '')

        main_image = request.FILES.get("main_image", '')
        temporary_status = request.POST.get("temporary_status", '')
        photo1 = request.FILES.get("photo1", '')
        photo2 = request.FILES.get("photo2", '')
        photo3 = request.FILES.get("photo3", '')
        photo4 = request.FILES.get("photo4", '')
        old_main_image = product.main_image
        old_photo1 = product.photo1
        old_photo2 = product.photo2
        old_photo3 = product.photo3
        old_photo4 = product.photo4
        form_obj.cleaned_data = {}
        if name:
            form_obj.cleaned_data["name"] = name
        if category:
            form_obj.cleaned_data["category"] = ProductsCategory.objects.filter(category_id=category)[0]
        if price:
            form_obj.cleaned_data["price"] = price
        if property1:
            form_obj.cleaned_data["property1"] = property1
        if property2:
            form_obj.cleaned_data["property2"] = property2
        if property3:
            form_obj.cleaned_data["property3"] = property3
        if property4:
            form_obj.cleaned_data["property4"] = property4
        if property5:
            form_obj.cleaned_data["property5"] = property5
        if property6:
            form_obj.cleaned_data["property6"] = property6
        if main_image:
            if old_main_image:
                image_path = old_main_image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.main_image = main_image
            product.save()
        if temporary_status:
            form_obj.cleaned_data["temporary_status"] = temporary_status
        if photo1:
            if old_photo1:
                image_path = old_photo1.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo1 = photo1
            product.save()
        if photo2:
            if old_photo2:
                image_path = old_photo2.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo2 = photo2
            product.save()
        if photo3:
            if old_photo3:
                image_path = old_photo3.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo3 = photo3
            product.save()
        if photo4:
            if old_photo4:
                image_path = old_photo4.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo4 = photo4
            product.save()
        try:
            Product.objects.filter(product_id=product_id).update(**form_obj.cleaned_data)
            print("sucess")
            return redirect("products")
        except Exception as e:
            print(e)


def product_delete(request, product_id):
    product = Product.objects.filter(product_id=product_id)[0]
    if product.main_image:
        if os.path.exists(product.main_image.path):
            os.remove(product.main_image.path)
    if product.photo1:
        if os.path.exists(product.photo1.path):
            os.remove(product.photo1.path)
    if product.photo2:
        if os.path.exists(product.photo2.path):
            os.remove(product.photo2.path)
    if product.photo3:
        if os.path.exists(product.photo3.path):
            os.remove(product.photo3.path)
    if product.photo4:
        if os.path.exists(product.photo4.path):
            os.remove(product.photo4.path)
    product.delete()
    return redirect("products")


def product_change_photo(request, product_id):
    if request.method == "GET":
        form_obj = ProductPhotoChange()
        product = Product.objects.filter(product_id=product_id)[0]
        return render(request, "product_change_photo.html", {"product": product, "form_obj": form_obj})
    if request.method == "POST":
        ProductPhotoChange(request.POST, request.FILES)
        product = Product.objects.filter(product_id=product_id)[0]
        old_main_image = product.main_image
        old_photo1 = product.photo1
        old_photo2 = product.photo2
        old_photo3 = product.photo3
        old_photo4 = product.photo4
        main_image = request.FILES.get("main_image", '')
        photo1 = request.FILES.get("photo1", '')
        photo2 = request.FILES.get("photo2", '')
        photo3 = request.FILES.get("photo3", '')
        photo4 = request.FILES.get("photo4", '')
        if main_image:
            if old_main_image:
                image_path = old_main_image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.main_image = main_image
            product.save()
        if photo1:
            if old_photo1:
                image_path = old_photo1.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo1 = photo1
            product.save()
        if photo2:
            if old_photo2:
                image_path = old_photo2.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo2 = photo2
            product.save()
        if photo3:
            if old_photo3:
                image_path = old_photo3.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo3 = photo3
            product.save()
        if photo4:
            if old_photo4:
                image_path = old_photo4.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            product.photo4 = photo4
            product.save()
        return redirect("products")


def product_ajax_photo_change(request):
    main_image = request.POST.get('main_image', '')
    photo1 = request.POST.get('photo1', '')
    photo2 = request.POST.get('photo2', '')
    photo3 = request.POST.get('photo3', '')
    photo4 = request.POST.get('photo4', '')
    product_id = request.POST.get('product_id', '')
    if main_image == "-1":
        os.remove(Product.objects.filter(product_id=product_id)[0].main_image.path)
        Product.objects.filter(product_id=product_id).update(main_image='')
        return redirect("products")
    if photo1 == "-1":
        os.remove(Product.objects.filter(product_id=product_id)[0].photo1.path)
        Product.objects.filter(product_id=product_id).update(photo1='')
        return redirect("products")
    if photo2 == "-1":
        os.remove(Product.objects.filter(product_id=product_id)[0].photo2.path)
        Product.objects.filter(product_id=product_id).update(photo2='')
        return redirect("products")
    if photo3 == "-1":
        os.remove(Product.objects.filter(product_id=product_id)[0].photo3.path)
        Product.objects.filter(product_id=product_id).update(photo3='')
        return redirect("products")
    if photo4 == "-1":
        os.remove(Product.objects.filter(product_id=product_id)[0].photo4.path)
        Product.objects.filter(product_id=product_id).update(photo4='')
        return redirect("products")
    return redirect("products")


def get_category(request):
    categories = ProductsCategory.objects.all()
    return render(request, "show_product_categories.html", {"categories": categories})


def get_category_detail(request, category_id):
    category = ProductsCategory.objects.filter(category_id=category_id)[0]
    return render(request, "show_product_category_detailed.html", {"category": category})


def add_categories(request):
    if request.method == "GET":
        form_obj = ProductsCategoryInfo()
        return render(request, "add_category.html", {"form_obj": form_obj})
    if request.method == "POST":
        print(request.POST)
        category_name = request.POST.get("name", '')
        categories = ProductsCategory.objects.all()
        if len(categories) == 0:
            ProductsCategory.objects.create(name=category_name)
            return redirect('category')
        else:
            for category in categories:
                if category.name == category_name:
                    return render(request, "add_category.html", {"errors": "the category has been existed"})
                else:
                    ProductsCategory.objects.create(name=category_name)
                    return redirect('category')


def edit_review_rating(request, product_id, order_id):
    print(product_id)
    print(order_id)
    if request.method == "GET":
        user = MyUser.objects.filter(username=request.user.username)[0]
        check_review_ratings = ReviewAndRating.objects.filter(user=user, product_id=product_id, order=Order.objects.filter(order_id=order_id)[0])
        if len(check_review_ratings) != 0 and check_review_ratings[len(check_review_ratings) - 1].review_date is not None:
            return render(request, "change_review_rating.html",
                          {"info": "You have reviewed and chose the customer rating", "code": 1})
        else:
            form_obj = ReviewRatingChangeForm()
            return render(request, "change_review_rating.html", {"form_obj": form_obj, "code": 0})
    if request.method == "POST":
        user = MyUser.objects.filter(username=request.user.username)[0]
        new_review = ReviewAndRating.objects.create(user=user, product_id=product_id, order=Order.objects.filter(order_id=order_id)[0])
        review_rating = ReviewAndRating.objects.filter(user=user, product_id=product_id, order=Order.objects.filter(order_id=order_id)[0])[len(ReviewAndRating.objects.filter(user=user, product_id=product_id, order=Order.objects.filter(order_id=order_id)[0]))-1]
        form_obj = ReviewRatingChangeForm(request.POST, request.FILES)
        review = request.POST.get("review", '')
        customer_rating = request.POST.get("customer_rating")
        print(review)
        print(customer_rating)
        if review != "":
            review_rating.review = review
            review_rating.save()
        if customer_rating != "":
            review_rating.customer_rating = customer_rating
            review_rating.save()
        if review != "" or customer_rating != "":
            review_rating.review_date = timezone.now()
            review_rating.save()
        if review == "" and customer_rating == "":
            new_review.delete()
        return redirect("/purchase_order/order_detail/" + str(order_id))





