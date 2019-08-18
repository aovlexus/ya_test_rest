from rest_framework.routers import DefaultRouter

from imports.views import ImportViewSet

router = DefaultRouter()
router.register(r'imports', ImportViewSet, basename='imports')


urlpatterns = router.urls
