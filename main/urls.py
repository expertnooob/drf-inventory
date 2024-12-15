from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


#Swagger schema view
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Inventory Management API",
#         default_version='v1',
#         description="API documentation",
#     ),
#     public=True,
#     permission_classes=[AllowAny],
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('user/', include('user.urls')),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] 
