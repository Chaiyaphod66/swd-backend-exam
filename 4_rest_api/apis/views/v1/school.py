from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

from apis.filters import SchoolFilter
from apis.models import School
from apis.serializers import SchoolDetailSerializer, SchoolSerializer



class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter

    def get_queryset(self):
        return self.queryset.annotate(
            classroom_count=Count("classrooms", distinct=True),
            teacher_count=Count("classrooms__teachers", distinct=True),
            student_count=Count("classrooms__students", distinct=True),
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SchoolDetailSerializer
        return self.serializer_class