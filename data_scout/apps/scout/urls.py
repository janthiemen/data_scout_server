from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'datasource', views.datasources.DataSourceViewSet)
router.register(r'datasourcefolder', views.datasources.DataSourceFolderViewSet)
router.register(r'recipe', views.wrangler.RecipeViewSet)
router.register(r'recipefolder', views.wrangler.RecipeFolderViewSet)
router.register(r'transformation', views.wrangler.TransformationViewSet)
router.register(r'join', views.datasources.JoinViewSet)
router.register(r'datasource_file', views.datasources.UserFileViewSet)
router.register(r'project', views.iam.ProjectViewSet)
router.register(r'user_project', views.iam.UserProjectViewSet)
router.register(r'user_profile', views.iam.UserProfileViewSet)
router.register(r'user', views.iam.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/check/', views.iam.LoginCheckView.as_view(), name='token_check'),
    path('api/datasource_file/<int:user_file_id>/upload', views.datasources.UserFileUploadView.as_view(), name='data_source_file'),
    path('datasource_types/', views.datasources.DataSourceTypesView.as_view(), name='hello'),
    path('transformation_types_view/', views.wrangler.TransformationTypesView.as_view(), name='hello'),
    path('data/<int:recipe>', views.wrangler.data, name='data'),
    path('pipeline/<int:recipe>/', views.wrangler.pipeline, name='pipeline_json'),
    path('change_password', csrf_exempt(views.iam.ChangePasswordView.as_view()), name='change_password'),
    path('user_detail', csrf_exempt(views.iam.UserDetailView.as_view()), name='user_detail'),
    path('meta/transformations', views.wrangler.meta_transformations, name='meta_transformations'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
