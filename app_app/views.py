from django.shortcuts import render , redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

 
# pdf  تصدير ------------
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# pdf  تصدير ------------

# Create your views here.---------------------------------------




def export_products_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products_full_report.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4)
    )

    products = Product.objects.all()

    elements = []

    # ✅ styles
    styles = getSampleStyleSheet()

    # ⭐ TITLE
    title = Paragraph("📦 Inventory Management - Products Report", styles["Title"])
    elements.append(title)

    # مسافة بين العنوان والجدول
    elements.append(Spacer(1, 20))

    # الجدول
    data = []

    data.append([
        "#", "Name", "SKU", "Quantity", "Min Stock", "Category",
        "Cost", "Price", "Discount", "Supplier", "Import Date", "Size", "Notes"
    ])

    for i, p in enumerate(products, start=1):
        data.append([
            i,
            p.name,
            p.sku,
            p.quantity,
            p.min_stock,
            p.get_category_display(),
            p.cost,
            p.price,
            p.discount if p.discount else "-",
            p.get_supplier_display() if p.supplier else "-",
            p.import_date if p.import_date else "-",
            p.size if p.size else "-",
            p.notes if p.notes else "-"
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
    ]))

    elements.append(table)

    doc.build(elements)

    return response

 
def export_distributors_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="distributors_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))

    distributors = Distributor.objects.all()

    elements = []
    styles = getSampleStyleSheet()

    # ⭐ العنوان
    title = Paragraph("🚚 Distributors Report", styles["Title"])
    elements.append(title)

    elements.append(Spacer(1, 10))

    # 📊 بيانات الجدول
    data = []

    data.append([
        "#",
        "Name",
        "Vehicle",
        "Load",
        "Qty",
        "Type",
        "Date",
        "Phone",
        "Notes"
    ])

    for i, d in enumerate(distributors, start=1):
        data.append([
            i,
            d.distributor_name,
            d.vehicle if d.vehicle else "-",
            d.load if d.load else "-",
            d.quantity_taken,
            d.get_quantity_type_display() if d.quantity_type else "-",
            str(d.quantity_date) if d.quantity_date else "-",
            d.phone if d.phone else "-",
            (d.notes[:15] + "...") if d.notes else "-"   # 🔥 تقصير النص
        ])

    # 🎯 تحديد عرض الأعمدة (أهم خطوة للتصغير)
    table = Table(data, colWidths=[
        30,   # #
        90,   # Name
        70,   # Vehicle
        60,   # Load
        50,   # Qty
        60,   # Type
        70,   # Date
        80,   # Phone
        100   # Notes
    ])

    # 🎨 تنسيق احترافي
    table.setStyle(TableStyle([
        # header
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),   # 🔥 تصغير الخط

        # body
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),

        # padding
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(table)

    doc.build(elements)

    return response

 


def export_sales_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))

    sales = Sale.objects.select_related('product').all()

    elements = []
    styles = getSampleStyleSheet()

    # ⭐ عنوان
    title = Paragraph("💰 Sales Report", styles["Title"])
    elements.append(title)

    elements.append(Spacer(1, 10))

    # 📊 البيانات
    data = []

    data.append([
        "#",
        "Buyer",
        "Phone",
        "Product",
        "Category",
        "Size",
        "Qty",
        "Total",
        "Date",
        "Notes"
    ])

    for i, s in enumerate(sales, start=1):
        data.append([
            i,
            s.buyer_name,
            s.phone if s.phone else "-",
            s.product.name,
            s.product.get_category_display() if s.product else "-",
            s.product.size if s.product.size else "-",
            s.quantity,
            f"${s.total_price}",
            str(s.sale_date) if s.sale_date else "-",
            (s.notes[:15] + "...") if s.notes else "-"   # 🔥 تقصير
        ])

    # 🎯 عرض الأعمدة (مهم جداً)
    table = Table(data, colWidths=[
        30,   # #
        90,   # Buyer
        80,   # Phone
        100,  # Product
        80,   # Category
        60,   # Size
        50,   # Qty
        70,   # Total
        80,   # Date
        120   # Notes
    ])

    # 🎨 تنسيق
    table.setStyle(TableStyle([
        # header
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        # تصغير الخط
        ('FONTSIZE', (0,0), (-1,-1), 8),

        # محاذاة
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        # خطوط
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),

        # خلفية
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),

        # padding
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(table)

    doc.build(elements)

    return response






















def About_System(request):
    return render(request,'pages/About_System.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # غيّرها حسب صفحتك
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


 
#index-----------------------------------------------------------
@login_required
def index(request):
    total_products = Product.objects.count()
    total_sales = Sale.objects.count()
    total_distributors = Distributor.objects.count()
                # المنتجات منخفضة المخزون
    low_stock = Product.objects.filter(quantity__lte=5).count()
     
    # 🔹 Chart 1: Sales per month (مثال بسيط)
    sales = Sale.objects.all()

    months = []
    sales_data = []

    for m in range(1, 13):
        total = sales.filter(sale_date__month=m).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        months.append(m)
        sales_data.append(total)

    # 🔹 Chart 2: Distributors load
    distributors = Distributor.objects.all()

    dist_names = []
    dist_loads = []

    for d in distributors:
        dist_names.append(d.distributor_name)
        dist_loads.append(d.load or 0)
    context={
        'total_products': total_products,
        'total_sales': total_sales,
        'total_distributors': total_distributors,
        'low_stock': low_stock,
        
        'months': months,
        'sales_data': sales_data,
        'dist_names': dist_names,
        'dist_loads': dist_loads,

    }
    return render(request,'pages/index.html',context)
 

# prodect  prodect prodect-------------------------------------------------------
def add_product(request):
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')
 
    else:
        form = ProductForm()
    
    return render(request,'pages/add/add_product.html',{'form':form})

def product_list(request):
    query = request.GET.get('q', '')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(price__icontains=query) |
            Q(quantity__icontains=query)
        )
    
    context={
        'products': products,    
        'query': query,
    }
    return render(request,'pages/list/product_list.html',context)

def update_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'pages/update/update_product.html', {
        'form': form,
        'product': product
    })

def delete_product(request, id):
    obj = get_object_or_404(Product, id=id)

    if request.method == "POST":
        obj.delete()
        return redirect('product_list')

    return render(request, 'pages/delete/delete_product.html', {
        'obj': obj,
        'type': 'product'
    })
# prodect -------------------------------------------------------


 

# distributors -------------------------------------------------------
def add_distributors(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = DistributorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('distributors_list')

    else:
        form = DistributorsForm()

    return render(request, 'pages/add/add_distributors.html', {'form': form,'products': products})

def distributors_list(request):
    query = request.GET.get('q', '')

    distributors = Distributor.objects.all()

    if query:
        distributors = distributors.filter(
            Q(distributor_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(vehicle__icontains=query) |
            Q(load__icontains=query)
        )
    context={
        'distributors': distributors,
        'query': query
    } 
    return render(request,'pages/list/distributors_list.html',context)

def update_distributors(request, id):
    distributor = get_object_or_404(Distributor, id=id)
    products = Product.objects.all()

    if request.method == "POST":
        form = DistributorsForm(request.POST, instance=distributor)

        print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('distributors_list')
    else:
        form = DistributorsForm(instance=distributor)

    return render(request, 'pages/update/update_distributors.html', {
        'form': form,
        'distributor': distributor,
        'products': products
    })

def delete_distributor(request, id):
    obj = get_object_or_404(Distributor, id=id)

    if request.method == "POST":
        obj.delete()
        return redirect('distributors_list')

    return render(request, 'pages/delete/delete_distributor.html', {
        'obj': obj,
        'type': 'distributor'
    })
# distributors -------------------------------------------------------
 

# sales --------------------------------------------------------------
def sales_prodect(request):
    if request.method == "POST":
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_list')
    else:
        form = SalesForm()

    return render(request, 'pages/add/sales_prodect.html', {'form': form})

def sales_list(request):
    query = request.GET.get('q', '')

    sales = Sale.objects.all()

    if query:
        sales = sales.filter(
            Q(buyer_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(product__name__icontains=query) |
            Q(total_price__icontains=query)
        )

    
    context={
        "sales": sales,  
        'query': query,
    }
    return render(request,'pages/list/sales_list.html',context)

def update_sales(request, id):
    sales = get_object_or_404(Sale, id=id)
    products = Product.objects.all()

    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sales)
        if form.is_valid():
            form.save()
            return redirect('sales_list')
        else:
            print(form.errors)
    else:
        form = SalesForm(instance=sales)

    return render(request, 'pages/update/update_sales.html', {
        'form': form,
        'sales': sales,
        'products': products
    })

def delete_sale(request, id):
    obj = get_object_or_404(Sale, id=id)

    if request.method == "POST":
        obj.delete()
        return redirect('sales_list')

    return render(request,'pages/delete/delete_sale.html', {
        'obj': obj,
        'type': 'sale'
    })
# sales --------------------------------------------------------------
 
 
 