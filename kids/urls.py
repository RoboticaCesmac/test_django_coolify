from rest_framework.routers import DefaultRouter
from .views import UserKidsView

router = DefaultRouter()
router.register(r"me/kids", UserKidsView)
user_urlpatterns = router.urls
