"""data_scout_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'datasource', views.DataSourceViewSet)
router.register(r'datasourcefolder', views.DataSourceFolderViewSet)
router.register(r'recipe', views.RecipeViewSet)
router.register(r'recipefolder', views.RecipeFolderViewSet)
router.register(r'transformation', views.TransformationViewSet)
router.register(r'flow', views.FlowViewSet)
router.register(r'join', views.JoinViewSet)
router.register(r'flowstep', views.FlowStepViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/check/', views.LoginCheckView.as_view(), name='token_check'),
    path('datasource_types/', views.DataSourceTypesView.as_view(), name='hello'),
    path('transformation_types_view/', views.TransformationTypesView.as_view(), name='hello'),
    path('data/<int:recipe>', views.data, name='data'),
    # path('data/<int:recipe>/<int:step>', views.data, name='data'),
    path('meta/transformations', views.meta_transformations, name='meta_transformations'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     path('recipe/<int:recipe>/recipe', recipe.get_recipe),
#     path('recipe/<int:recipe>/data', recipe.get_data),
# ]

