from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Course,
    Group,
    User,
    Test,
    Question,
    StudentSolve,
    Integration,
    Journal,
    Material,
    Lesson,
    Application,
    Payment,
    Team,
    Partner,
    FAQ,
    CourseIncluded,
    CourseProcess,
    ContactStats,
    ContactInfo,
    SuccessStory,
)

from .serializers import (
    CourseSerializer,
    GroupSerializer,
    UserSerializer,
    TestSerializer,
    QuestionSerializer,
    StudentSolveSerializer,
    IntegrationSerializer,
    JournalSerializer,
    MaterialSerializer,
    LessonSerializer,
    ApplicationSerializer,
    PaymentSerializer,
    TeamSerializer,
    PartnerSerializer,
    FAQSerializer,
    CourseIncludedSerializer,
    CourseProcessSerializer,
    ContactStatsSerializer,
    ContactInfoSerializer,
    SuccessStorySerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    - SAFE methods (GET, HEAD, OPTIONS) – allowed for everyone (or authenticated only if you want).
    - write operations – only for ADMIN role.
    """

    def has_permission(self, request, view):
        # all can read
        if request.method in permissions.SAFE_METHODS:
            return True

        # for write, must be authenticated and admin role
        if not request.user or not request.user.is_authenticated:
            return False

        # If you later integrate with Django auth User, adapt this check.
        try:
            # assuming you map request.user.email to your custom User
            from .models import User as CustomUser

            custom = CustomUser.objects.filter(email=request.user.email).first()
            if custom and custom.role == CustomUser.Role.ADMIN:
                return True
        except Exception:
            pass

        return False


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base CRUD viewset. Permission is open for now – you can switch to
    IsAuthenticated / custom permission later.
    """
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]


class UserViewSet(viewsets.ModelViewSet):
    """
    /api/users/
    /api/users/{id}/

    Filters:
      - ?role=student|admin
      - ?status=active|upcoming|finished|paused
      - ?group=<group_id>

    Search:
      - ?search=John
    Ordering:
      - ?ordering=firstname
      - ?ordering=-id
    """

    queryset = User.objects.all().select_related("group")
    serializer_class = UserSerializer

    # if you want only authenticated users to see something:
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["firstname", "lastname", "email", "login"]
    ordering_fields = ["id", "firstname", "lastname", "email"]
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()

        role = self.request.query_params.get("role")
        status = self.request.query_params.get("status")
        group_id = self.request.query_params.get("group")

        if role:
            qs = qs.filter(role=role)
        if status:
            qs = qs.filter(status=status)
        if group_id:
            qs = qs.filter(group_id=group_id)

        return qs


class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    search_fields = ["title", "description"]
    ordering_fields = ["id", "title", "price"]
    ordering = ["id"]


class GroupViewSet(BaseViewSet):
    queryset = Group.objects.all().select_related("course")
    serializer_class = GroupSerializer

    search_fields = ["title"]
    ordering_fields = ["id", "starting_date", "ending_date"]
    ordering = ["id"]


class TestViewSet(BaseViewSet):
    queryset = Test.objects.all().select_related("course")
    serializer_class = TestSerializer

    search_fields = ["title"]
    ordering_fields = ["id", "course"]
    ordering = ["id"]


class QuestionViewSet(BaseViewSet):
    queryset = Question.objects.all().select_related("test")
    serializer_class = QuestionSerializer

    search_fields = ["title"]
    ordering_fields = ["id", "type"]
    ordering = ["id"]


class StudentSolveViewSet(BaseViewSet):
    queryset = StudentSolve.objects.all().select_related("user", "test")
    serializer_class = StudentSolveSerializer

    ordering_fields = ["id", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user")
        test_id = self.request.query_params.get("test")

        if user_id:
            qs = qs.filter(user_id=user_id)
        if test_id:
            qs = qs.filter(test_id=test_id)

        return qs


class IntegrationViewSet(BaseViewSet):
    queryset = Integration.objects.all().select_related("user")
    serializer_class = IntegrationSerializer

    ordering_fields = ["id", "date", "rate_limit_per_minute", "rate_limit_per_day"]
    ordering = ["-date"]


class JournalViewSet(BaseViewSet):
    queryset = Journal.objects.all().select_related("group", "user")
    serializer_class = JournalSerializer

    ordering_fields = ["id", "date"]
    ordering = ["-date"]

    def get_queryset(self):
        qs = super().get_queryset()
        group_id = self.request.query_params.get("group")
        user_id = self.request.query_params.get("user")
        if group_id:
            qs = qs.filter(group_id=group_id)
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


class MaterialViewSet(BaseViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    search_fields = ["title", "source"]
    ordering_fields = ["id", "title"]
    ordering = ["id"]


class LessonViewSet(BaseViewSet):
    queryset = Lesson.objects.all().select_related("material", "course")
    serializer_class = LessonSerializer

    search_fields = ["title", "description"]
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get("course")
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs


class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.all().select_related("course")
    serializer_class = ApplicationSerializer

    ordering_fields = ["id", "date"]
    ordering = ["-date"]


class PaymentViewSet(BaseViewSet):
    queryset = Payment.objects.all().select_related("user")
    serializer_class = PaymentSerializer

    ordering_fields = ["id", "date", "payed"]
    ordering = ["-date"]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


class TeamViewSet(BaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    search_fields = ["fullname", "speciality"]
    ordering_fields = ["id", "fullname"]
    ordering = ["id"]


class PartnerViewSet(BaseViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    search_fields = ["name", "description"]
    ordering_fields = ["id", "name"]
    ordering = ["id"]


class FAQViewSet(BaseViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    search_fields = ["question", "answer"]
    ordering_fields = ["id"]
    ordering = ["id"]


class CourseIncludedViewSet(BaseViewSet):
    queryset = CourseIncluded.objects.all().select_related("course")
    serializer_class = CourseIncludedSerializer

    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get("course")
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs


class CourseProcessViewSet(BaseViewSet):
    queryset = CourseProcess.objects.all().select_related("course")
    serializer_class = CourseProcessSerializer

    ordering_fields = ["course", "rank", "id"]
    ordering = ["course", "rank"]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get("course")
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs


class ContactStatsViewSet(BaseViewSet):
    queryset = ContactStats.objects.all()
    serializer_class = ContactStatsSerializer

    ordering_fields = ["id", "students"]
    ordering = ["id"]


class ContactInfoViewSet(BaseViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

    ordering_fields = ["id"]
    ordering = ["id"]


class SuccessStoryViewSet(BaseViewSet):
    queryset = SuccessStory.objects.all().select_related("user")
    serializer_class = SuccessStorySerializer

    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs