from django.http.response import HttpResponse
from django.template.defaulttags import register
from .models import Product, Category
from django.shortcuts import render
import random
import json
'''Paste code here'''

''''''


class NavBar:
    def __init__(self, Category):
        self.objects_of_category = Category.objects.all()
        self.ltfive = {}
        self.gtfive = {}
        for i in self.objects_of_category:
            if(i.is_root_node()):
                # menu_dict[i.name] = list(i.get_children())
                children_list = [j.name for j in i.get_children()]
                if(len(children_list) > 5):
                    self.gtfive[i.name] = [
                        children_list[:6], children_list[6:]]
                else:
                    self.ltfive[i.name] = children_list

    def details(self):
        context = {'gtfive': self.gtfive, 'ltfive': self.ltfive}
        return context


navbar = NavBar(Category)


class RandomProductSelector:
    def __init__(self, Category_name):
        self.category = Category.objects.filter(name=Category_name).first()

    def get_list(self, number):
        temp_list = list(self.category.get_children())  # sub_category_list
        winner_products_list = []  # list of randomly drawn products
        while(len(winner_products_list) < number):
            winner_sub_category = random.choice(temp_list)
            temp_list.remove(winner_sub_category)
            products_of_won_category = Product.objects.filter(
                sub_category=winner_sub_category).first()
            if(products_of_won_category == None):
                continue
            winner_products_list.append(products_of_won_category)
        return(winner_products_list)  # list of products won on random draw


class GetImportantInfoProduct:
    def __init__(self, Product):
        self.Product = Product

    def get_slug(self):
        return(self.Product.slug)

    def get_info(self):
        d = {}
        d['productname'] = self.Product.productname
        d['selling_price'] = self.Product.selling_price
        d['MRP'] = self.Product.discount+self.Product.selling_price
        image = self.Product.image[1:-
                                   1].replace("'", '').replace(" ", '').split(',')
        d['image'] = image[0]
        return(d)


class GetRandomProducts:
    def __init__(self, Category_name, number):
        selector = RandomProductSelector(Category_name)
        self.winner_products_list = selector.get_list(number)

    def get_winner_products_dictionary(self):
        winner_products_dictionary = {}
        for i in self.winner_products_list:
            product_info = GetImportantInfoProduct(i)
            winner_products_dictionary[product_info.get_slug(
            )] = product_info.get_info()
        return(winner_products_dictionary)


def home(request):
    jewellery = GetRandomProducts('Jewellery', 10)
    mens_jewellery = GetRandomProducts('Mens Jewellery', 6)
    context = {
        'mens_jewellery_dict': mens_jewellery.get_winner_products_dictionary(),
        'jewellery_dict': jewellery.get_winner_products_dictionary()
    }
    return render(request, 'Products/home.html', {'title': 'Kridha', 'context': context, 'navbar': navbar.details()})


def category(request, slug):
    slug_category = Category.objects.filter(slug=slug).first()

    category_dict = {}  # key=slug_of_product,value=dict of product details
    if(len(slug_category.get_family()) > 2):
        # all subcategories to dictionary
        for i in slug_category.get_family()[1:]:
            for pro in Product.objects.filter(sub_category=i):
                d = {}
                d['id'] = pro.id
                d['productname'] = pro.productname

                d['selling_price'] = pro.selling_price
                d['MRP'] = pro.discount+pro.selling_price
                image = pro.image[1:-
                                  1].replace("'", '').replace(" ", '').split(',')
                d['image'] = image[0]
                category_dict[pro.slug] = d
    else:
        products = Product.objects.filter(sub_category=slug_category)
        print(products)

        for pro in products:
            d = {}
            d['id'] = pro.id
            d['productname'] = pro.productname
            d['selling_price'] = pro.selling_price
            d['MRP'] = pro.discount+pro.selling_price
            image = pro.image[1:-
                              1].replace("'", '').replace(" ", '').split(',')
            d['image'] = image[0]
            category_dict[pro.slug] = d
    print(category_dict)
    return render(request, 'Products/category.html', {'title': slug_category, 'navbar': navbar.details(), 'category_dict': category_dict})


def product(request, slug):
    product = Product.objects.filter(slug=slug).first()
    field_list = ['sub_category', 'age_group', 'alarm_clock', 'case_color', 'case_material', 'case_shape', 'chain_length', 'colour', 'design', 'design_length', 'design_width', 'dial_color', 'diameter', 'diamond_weight', 'earring_length', 'earring_width', 'gemstone_colour', 'gender', 'glass_material', 'gold_weight', 'gross_weight', 'hath_phool_bracelet_length', 'hath_phool_design_length', 'hath_phool_design_width', 'hath_phool_length', 'hath_phool_ring_design_length', 'hath_phool_ring_design_width', 'length', 'long_necklace_design_length',
                  'long_necklace_design_width', 'long_necklace_length', 'long_necklace_pendant_length', 'long_necklace_pendant_width', 'maang_tika_chain_length', 'maang_tika_design_length', 'maang_tika_side_chain_length', 'manufacturer', 'material', 'necklace_length', 'necklace_width', 'pendant_length', 'pendant_width', 'sales_package', 'size', 'small_necklace_design_length', 'small_necklace_design_width', 'small_necklace_diameter', 'small_necklace_length', 'small_necklace_pendant_length', 'small_necklace_pendant_width', 'small_necklace_width', 'stone_weight', 'strap_color', 'strap_material', 'surface_finish', 'theme']
    image = product.image[1:-
                          1].replace("'", '').replace(" ", '').split(',')
    image_dict = {}
    for i in range(1, len(image)):
        image_dict[i] = image[i]
    main_details = {
        "id": product.id,
        "name": product.productname,
        "selling_price": product.selling_price,
        "MRP": product.selling_price+product.discount,
        "main_image": image[0],
        "image": image_dict,
        "stylist_notes": product.stylist_notes
    }
    #additional_details = {}
    # for i in field_list:
    #    if(product.additional_info()[i] != 'nan'):
    #        key = i.replace('_', ' ').title()
    #        additional_details[key] = product.additional_details()[i]
    print(product.additional_info)

    details = {'main_details': main_details
               }
    return render(request, 'Products/product-detail.html', {'title': product.productname, 'navbar': navbar.details(), 'details': details})


def search(request):
    q = request.GET.get('q')
    if(q):
        products = Product.objects.filter(
            productname__contains=q)
        search_dict = {}
        for pro in products:
            d = {}
            d['id'] = pro.id
            d['productname'] = pro.productname
            d['selling_price'] = pro.selling_price
            d['MRP'] = pro.discount+pro.selling_price
            image = pro.image[1:-
                              1].replace("'", '').replace(" ", '').split(',')
            d['image'] = image[0]
            search_dict[pro.slug] = d
    return render(request, 'Products/search.html', {'title': 'Kridha',  'search_dict': search_dict, 'navbar': navbar.details()})
