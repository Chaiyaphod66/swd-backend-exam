from rest_framework.viewsets import ModelViewSet

from apis.filters import StudentFilter
from apis.models import Student
from apis.serializers import StudentDetailSerializer, StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter

    def get_queryset(self):
        return self.queryset.select_related("classroom__school")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentDetailSerializer

        return self.serializer_class