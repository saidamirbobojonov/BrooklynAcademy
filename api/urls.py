from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    CourseViewSet,
    GroupViewSet,
    TestViewSet,
    QuestionViewSet,
    StudentSolveViewSet,
    IntegrationViewSet,
    JournalViewSet,
    MaterialViewSet,
    LessonViewSet,
    ApplicationViewSet,
    PaymentViewSet,
    TeamViewSet,
    PartnerViewSet,
    FAQViewSet,
    CourseIncludedViewSet,
    CourseProcessViewSet,
    ContactStatsViewSet,
    ContactInfoViewSet,
    SuccessStoryViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"tests", TestViewSet, basename="test")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"student-solves", StudentSolveViewSet, basename="student-solve")
router.register(r"integrations", IntegrationViewSet, basename="integration")
router.register(r"journal", JournalViewSet, basename="journal")
router.register(r"materials", MaterialViewSet, basename="material")
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"team", TeamViewSet, basename="team")
router.register(r"partners", PartnerViewSet, basename="partner")
router.register(r"faq", FAQViewSet, basename="faq")
router.register(r"course-included", CourseIncludedViewSet, basename="course-included")
router.register(r"course-process", CourseProcessViewSet, basename="course-process")
router.register(r"contact-stats", ContactStatsViewSet, basename="contact-stats")
router.register(r"contact-info", ContactInfoViewSet, basename="contact-info")
router.register(r"success-stories", SuccessStoryViewSet, basename="success-story")

urlpatterns = [
    path("", include(router.urls)),
]