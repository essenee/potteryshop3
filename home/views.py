# home/views.py
from rest_framework import viewsets, generics
from .models import PotteryCategory, Product
from .serializers import PotteryCategorySerializer, ProductSerializer

class PotteryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PotteryCategory.objects.all()
    serializer_class = PotteryCategorySerializer

class ProductByCategoryList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category', None)
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset.order_by('category__name')  # Updated to use 'name'