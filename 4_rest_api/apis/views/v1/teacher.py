from rest_framework.viewsets import ModelViewSet

from apis.filters import TeacherFilter
from apis.models import Teacher
from apis.serializers import TeacherDetailSerializer, TeacherSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_class = TeacherFilter

    def get_queryset(self):
        return self.queryset.prefetch_related("classrooms__school")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer

        return self.serializer_class