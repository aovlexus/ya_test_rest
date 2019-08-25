from rest_framework.routers import DefaultRouter

from imports.views import ImportViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'imports', ImportViewSet, basename='imports')


urlpatterns = router.urls
