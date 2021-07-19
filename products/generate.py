from .models import Category, Product
# Create your views here.

import os
import pandas as pd
import numpy as np
csv_path = os.path.join(os.path.dirname(__file__), 'All.csv')
All = pd.read_csv(csv_path)
rows = All.shape[0]
# Create your views here.
category_dict = {
    'Accessories': ['Brooch', 'Hair Accessories', 'Watches'],
    'Campaign': ['9-5 Collection', 'Birthday Boy', 'Birthday Gifts', 'BoardRoom Look', 'Casual', 'College', 'Date Night', 'Kids Jewelry', 'Party'],
    'Collections': ['Adorn',
                    'Aham Brahmasmi',
                    'Aztec bar',
                    'Bagh E Fiza',
                    'Butterfly',
                    'Colors Generic',
                    'Cool Stacked',
                    'Devil Collection'],
    'Jewellery': ['Anklet',
                  'Bangle & Bracelet',
                  'Bridal Sets',
                  'Chain',
                  'Earrings',
                  'Maang Tika',
                  'Maang Tika Set',
                  'Mangalsutra',
                  'Necklace',
                  'Necklace Set',
                  'Nose Ring',
                  'Pendant',
                  'Pendant Set',
                  'Ring',
                  'Toe Ring'],
    'Mens Jewellery': ['Bracelet',
                       'Cufflinks',
                       'Kada',
                       'Mens Chain',
                       'Mens Pendant',
                       'Mens Ring',
                       'Neck Piece',
                       'Studs']
}

for k in category_dict:
    Parent = Category.objects.create(name=k)
    for i in category_dict[k]:
        child = Category.objects.create(name=i, parent=Parent)

for i in range(rows):
    sub_category = All['sub_category'][i]  # got category
    Cat = Category.objects.filter(name=sub_category).first()
    p = Product(
        sub_category=Cat,
        productname=All['productname'][i],
        selling_price=All['selling_price'][i],
        discount=All['discount'][i],
        stylist_notes=All['stylist_notes'][i],
        image=All['image'][i],
        additional_info={
            'manufacturer': All['Manufacturer'][i],
            'colour': All['Colour'][i],
            'design': All['Design'][i],
            'design_length': All['Design Length'][i],
            'design_width': All['Design Width'][i],
            'gross_weight': All['Gross Weight'][i],
            'material': All['Material'][i],
            'sales_package': All['Sales Package'][i],
            'surface_finish': All['Surface Finish'][i],
            'theme': All['Theme'][i],
            'width': All['Width'][i],
            'length': All['Length'][i],
            'age_group': All['Age Group'][i],
            'alarm_clock': All['Alarm Clock'][i],
            'case_color': All['Case Color'][i],
            'case_material': All['Case Material'][i],
            'case_shape': All['Case Shape'][i],
            'dial_color': All['Dial Color'][i],
            'gender': All['Gender'][i],
            'glass_material': All['Glass Material'][i],
            'strap_color': All['Strap Color'][i],
            'strap_material': All['Strap Material'][i],
            'earring_length': All['Earring Length'][i],
            'earring_width': All['Earring Width'][i],
            'gemstone_colour': All['Gemstone Colour'][i],
            'necklace_length': All['Necklace Length'][i],
            'chain_length': All['Chain Length'][i],
            'pendant_length': All['Pendant Length'][i],
            'pendant_width': All['Pendant Width'][i],
            'necklace_width': All['Necklace Width'][i],
            'size': All['Size'][i],
            'stone_weight': All['Stone Weight'][i],
            'gold_weight': All['Gold Weight'][i],
            'diamond_weight': All['Diamond Weight'][i],
            'hath_phool_bracelet_length': All['Hath Phool Bracelet Length'][i],
            'hath_phool_design_length': All['Hath Phool Design Length'][i],
            'hath_phool_design_width': All['Hath Phool Design Width'][i],
            'hath_phool_length': All['Hath Phool Length'][i],
            'hath_phool_ring_design_length': All['Hath Phool Ring Design Length'][i],
            'hath_phool_ring_design_width': All['Hath Phool Ring Design Width'][i],
            'long_necklace_design_length': All['Long Necklace Design Length'][i],
            'long_necklace_design_width': All['Long Necklace Design Width'][i],
            'long_necklace_length': All['Long Necklace Length'][i],
            'long_necklace_pendant_length': All['Long Necklace Pendant Length'][i],
            'long_necklace_pendant_width': All['Long Necklace Pendant Width'][i],
            'maang_tika_design_length': All['Maang Tika Design Length'][i],
            'small_necklace_design_length': All['Small Necklace Design Length'][i],
            'small_necklace_diameter': All['Small Necklace Diameter'][i],
            'small_necklace_length': All['Small Necklace Length'][i],
            'small_necklace_pendant_length': All['Small Necklace Pendant Length'][i],
            'small_necklace_pendant_width': All['Small Necklace Pendant Width'][i],
            'small_necklace_width': All['Small Necklace Width'][i],
            'maang_tika_chain_length': All['Maang Tika Chain Length'][i],
            'maang_tika_side_chain_length': All['Maang Tika Side Chain Length'][i],
            'small_necklace_design_width': All['Small Necklace Design Width'][i],
            'diameter': All['Diameter'][i],
        }

    )
    p.save()
    print(p)
