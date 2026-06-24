from rest_framework.routers import DefaultRouter
from .views import CulturaViewSet

router = DefaultRouter()
router.register('culturas', CulturaViewSet, basename='cultura')

urlpatterns = router.urls