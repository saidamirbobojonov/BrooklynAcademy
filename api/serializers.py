from rest_framework import serializers

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


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # don't expose password on read
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "firstname",
            "lastname",
            "image_path",
            "email",
            "login",
            "password",
            "role",
            "group",
            "status",
        ]

    def create(self, validated_data):
        """
        If you later switch to Django auth-style hashing, hook it here.
        For now it just stores the given value into the CharField.
        """
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        # TODO: if you make this an AbstractBaseUser, use set_password here.
        if password is not None:
            user.password = password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            # TODO: instance.set_password(password) if you switch to Django auth.
            instance.password = password
        instance.save()
        return instance


class TestSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Test
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())

    class Meta:
        model = Question
        fields = "__all__"


class StudentSolveSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())

    class Meta:
        model = StudentSolve
        fields = "__all__"


class IntegrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Integration
        fields = "__all__"


class JournalSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Journal
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    material = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all(), allow_null=True, required=False
    )
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("date", "throttled", "throttle_until")


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("date",)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class CourseIncludedSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = CourseIncluded
        fields = "__all__"


class CourseProcessSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = CourseProcess
        fields = "__all__"


class ContactStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactStats
        fields = "__all__"


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = "__all__"


class SuccessStorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = SuccessStory
        fields = "__all__"