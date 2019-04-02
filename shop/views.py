from audioop import reverse

from django.shortcuts import render, redirect
from django.views import View
#from cms.models import Menu
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Menu, TopBanner,BottomBanner
from shop.forms import ReviewForm, CartForm
from .models import Category,Product

# Create your views here.

class BaseView(View):
    template_context = {
        'menus': Menu.objects.order_by('-weight'),
        'categories': Category.objects.all(),
    }
class Homepage(BaseView):
    def get(self, request):
            # 'menus': Menu.objects.order_by('-weight'),
            self.template_context['top_banners'] = TopBanner.objects.all()
            # 'categories': Category.objects.all(),
            self.template_context['big_bottom_banner'] = BottomBanner.objects.filter(is_big=True).first()
            self.template_context['small_bottom_banner']= BottomBanner.objects.filter(is_big=False)[:2] #for list slicing
            self.template_context['deal_products'] = Product.objects.filter(deal_of_the_day=True)
            self.template_context['latest_products'] = Product.objects.order_by('-pub_date')[:8]
            self.template_context['picked_products'] = Product.objects.order_by('?')[:4]

            return render(request, 'index.html',self.template_context)#specify file inside templates

class ProductView(BaseView):
    def get(self,request,product_id , review_form =None):
            #self.template_context['review_form'] = review_form or ReviewForm()
            self.template_context['review_form'] = review_form if  ReviewForm() else ReviewForm()
            self.template_context['product'] = Product.objects.get(pk = product_id)

        #print(product_id)
            return render(request,'product.html',self.template_context)

    def post(self,request,product_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review =  form.save(commit=False)
            review.user = request.user
            review.product = Product.objects.get(pk=product_id)
            review.save()
            #print( reverse('product_page', args =[product_id]))#this only generets url not redirect
            return redirect(reverse('product_page',args =[product_id]))

        return self.get(request,product_id, form)

class CartView(BaseView):
    def post(self, request, product_id):
        form = CartForm(request.POST)

        cart = form.save(commit=False)
        cart.user=request.user
        cart.product = Product.objects.get(pk=product_id)
        cart.save()
        return redirect(reverse('product_page', args =[product_id]))


class CategorySerializer(object):
    pass


class CategoryApi(APIView):
    """
    List all category.
    """
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    