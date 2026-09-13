from .models import Classroom, School, Student, Teacher
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test-user",
            password="test-password",
        )

    def test_authentication_is_required(self):
        url = reverse("v1:school-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_access_api(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("v1:school-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


class SchoolAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="school-test-user",
            password="test-password",
        )
        self.client.force_authenticate(user=self.user)
        self.client.credentials(
            HTTP_ACCEPT="application/json",
        )

        self.school = School.objects.create(
            name="Existing School",
            abbreviation="ES",
            address="Bangkok"
        )

        self.list_url = reverse("v1:school-list")
        self.detail_url = reverse(
            "v1:school-detail",
            args=[self.school.id]
        )

    def test_create_school(self):
        payload = {
            "name": "New School",
            "abbreviation": "NS",
            "address": "Chiang Mai",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            School.objects.filter(name="New School").exists()
        )

    def test_list_schools(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["name"],
            "Existing School",
        )

    def test_retrieve_school(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.school.id,
        )
        self.assertEqual(
            response.data["classroom_count"],
            0,
        )
        self.assertEqual(
            response.data["teacher_count"],
            0
        )
        self.assertEqual(
            response.data["student_count"],
            0
        )

    def test_update_school(self):
        payload = {
            "name": "Update School",
            "abbreviation": "US",
            "address": "Phuket",
        }

        response = self.client.put(
            self.detail_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.school.refresh_from_db()

        self.assertEqual(
            self.school.name,
            "Update School",
        )
        self.assertEqual(
            self.school.address,
            "Phuket",
        )

    def test_delete_school(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            School.objects.filter(id=self.school.id).exists()
        )


class SchoolFilterAndDetailAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="relation-test-user",
            password="test-password",
        )
        self.client.force_authenticate(user=self.user)
        self.client.credentials(
            HTTP_ACCEPT="application/json",
        )

        self.school = School.objects.create(
            name="Swift Academy",
            abbreviation="SWD",
            address="Bangkok",
        )
        self.other_school = School.objects.create(
            name="Other College",
            abbreviation="OC",
            address="Chiang Mai",
        )

        self.classroom_one = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=1,
        )
        self.classroom_two = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=2,
        )

        self.teacher = Teacher.objects.create(
            first_name="Jirat",
            last_name="Fongda",
            gender="male",
        )
        self.teacher.classrooms.set(
            [self.classroom_one, self.classroom_two]
        )

        Student.objects.create(
            first_name="Nareerat",
            last_name="Wangsri",
            gender="female",
            classroom=self.classroom_one,
        )
        Student.objects.create(
            first_name="Muthita",
            last_name="Palamee",
            gender="female",
            classroom=self.classroom_two,
        )

    def test_filter_school_by_partial_name(self):
        url = reverse("v1:school-list")

        response = self.client.get(
            url,
            {"name": "SWIFT"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[0]["id"],
            self.school.id,
        )

    def test_school_detail_counts_related_objects(self):
        url = reverse(
            "v1:school-detail",
            args=[self.school.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["classroom_count"],
            2,
        )
        self.assertEqual(
            response.data["teacher_count"],
            1,
        )
        self.assertEqual(
            response.data["student_count"],
            2,
        )


class ClassroomAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="classroom-test-user",
            password="test-password",
        )
        self.client.force_authenticate(user=self.user)
        self.client.credentials(
            HTTP_ACCEPT="application/json",
        )

        self.school = School.objects.create(
            name="Swift Academy",
            abbreviation="SWD",
            address="Bangkok",
        )
        self.other_school = School.objects.create(
            name="Other School",
            abbreviation="OS",
            address="Phuket",
        )

        self.classroom = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=1,
        )
        self.other_classroom = Classroom.objects.create(
            school=self.other_school,
            grade=2,
            room=1,
        )

        self.teacher = Teacher.objects.create(
            first_name="Jirat",
            last_name="Fongda",
            gender="male",
        )
        self.teacher.classrooms.add(self.classroom)

        self.student = Student.objects.create(
            first_name="Narin",
            last_name="Dee",
            gender="male",
            classroom=self.classroom,
        )

        self.list_url = reverse("v1:classroom-list")
        self.detail_url = reverse(
            "v1:classroom-detail",
            args=[self.classroom.id],
        )

    def test_filter_classrooms_by_school(self):
        response = self.client.get(
            self.list_url,
            {"school": self.school.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.classroom.id,
        )

    def test_classroom_detail_includes_relations(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["school"]["id"],
            self.school.id,
        )
        self.assertEqual(
            response.data["teachers"][0]["id"],
            self.teacher.id,
        )
        self.assertEqual(
            response.data["students"][0]["id"],
            self.student.id,
        )

    def test_cannot_create_duplicate_classroom(self):
        payload = {
            "school": self.school.id,
            "grade": 1,
            "room": 1,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            Classroom.objects.filter(
                school=self.school,
                grade=1,
                room=1,
            ).count(),
            1,
        )


class TeacherAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="teacher-test-user",
            password="test-password",
        )
        self.client.force_authenticate(user=self.user)
        self.client.credentials(
            HTTP_ACCEPT="application/json",
        )

        self.school = School.objects.create(
            name="Swift Academy",
            abbreviation="SWD",
            address="Bangkok",
        )
        self.other_school = School.objects.create(
            name="Other School",
            abbreviation="OS",
            address="Phuket",
        )

        self.classroom_one = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=1,
        )
        self.classroom_two = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=2,
        )
        self.other_classroom = Classroom.objects.create(
            school=self.other_school,
            grade=2,
            room=1,
        )

        self.teacher = Teacher.objects.create(
            first_name="Jirat",
            last_name="Fongda",
            gender="male",
        )
        self.teacher.classrooms.set(
            [self.classroom_one, self.classroom_two]
        )

        self.other_teacher = Teacher.objects.create(
            first_name="Mali",
            last_name="Sukjai",
            gender="female",
        )
        self.other_teacher.classrooms.add(
            self.other_classroom
        )

        self.list_url = reverse("v1:teacher-list")
        self.detail_url = reverse(
            "v1:teacher-detail",
            args=[self.teacher.id],
        )

    def test_filter_teachers_by_school_without_duplicates(self):
        response = self.client.get(
            self.list_url,
            {"school": self.school.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.teacher.id,
        )

    def test_filter_teachers_by_classroom(self):
        response = self.client.get(
            self.list_url,
            {"classroom": self.classroom_two.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.teacher.id,
        )

    def test_filter_teachers_by_name_and_gender(self):
        response = self.client.get(
            self.list_url,
            {
                "first_name": "JIR",
                "last_name": "fong",
                "gender": "MALE",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.teacher.id,
        )

    def test_teacher_detail_includes_classrooms(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        classroom_ids = {
            classroom["id"]
            for classroom in response.data["classrooms"]
        }

        self.assertEqual(
            classroom_ids,
            {
                self.classroom_one.id,
                self.classroom_two.id,
            },
        )

    def test_create_teacher_with_multiple_classrooms(self):
        payload = {
            "first_name": "New",
            "last_name": "Teacher",
            "gender": "other",
            "classrooms": [
                self.classroom_one.id,
                self.classroom_two.id,
            ],
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        created_teacher = Teacher.objects.get(
            id=response.data["id"]
        )
        classroom_ids = set(
            created_teacher.classrooms.values_list(
                "id",
                flat=True,
            )
        )

        self.assertEqual(
            classroom_ids,
            {
                self.classroom_one.id,
                self.classroom_two.id,
            },
        )


class StudentAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student-test-user",
            password="test-password",
        )
        self.client.force_authenticate(user=self.user)
        self.client.credentials(
            HTTP_ACCEPT="application/json"
        )

        self.school = School.objects.create(
            name="Swift Academy",
            abbreviation="SWD",
            address="Bangkok",
        )
        self.other_school = School.objects.create(
            name="Other School",
            abbreviation="OS",
            address="Phuket",
        )

        self.classroom_one = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=1,
        )
        self.classroom_two = Classroom.objects.create(
            school=self.school,
            grade=1,
            room=2,
        )
        self.other_classroom = Classroom.objects.create(
            school=self.other_school,
            grade=2,
            room=1,
        )

        self.student = Student.objects.create(
            first_name="Narin",
            last_name="Dee",
            gender="male",
            classroom=self.classroom_one,
        )
        self.second_student = Student.objects.create(
            first_name="Mali",
            last_name="Suksan",
            gender="female",
            classroom=self.classroom_two,
        )
        self.other_student = Student.objects.create(
            first_name="Arun",
            last_name="Jaidee",
            gender="other",
            classroom=self.other_classroom,
        )

        self.list_url = reverse("v1:student-list")
        self.detail_url = reverse(
            "v1:student-detail",
            args=[self.student.id],
        )

    def test_filter_students_by_school(self):
        response = self.client.get(
            self.list_url,
            {"school": self.school.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        student_ids = {
            student["id"]
            for student in response.data
        }

        self.assertEqual(
            student_ids,
            {
                self.student.id,
                self.second_student.id,
            },
        )

    def test_filter_students_by_classroom(self):
        response = self.client.get(
            self.list_url,
            {"classroom": self.classroom_one.id},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.student.id,
        )

    def test_filter_students_by_name_and_gender(self):
        response = self.client.get(
            self.list_url,
            {
                "first_name": "MAL",
                "last_name": "suk",
                "gender": "FEMALE",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.second_student.id,
        )

    def test_student_detail_includes_classroom_and_school(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["classroom"]["id"],
            self.classroom_one.id,
        )
        self.assertEqual(
            response.data["classroom"]["school"]["id"],
            self.school.id,
        )

    def test_create_student_with_classroom(self):
        payload = {
            "first_name": "New",
            "last_name": "Student",
            "gender": "other",
            "classroom": self.classroom_two.id,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        created_student = Student.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(
            created_student.classroom_id,
            self.classroom_two.id,
        )

    def test_reject_invalid_gender(self):
        payload = {
            "first_name": "Invalid",
            "last_name": "Gender",
            "gender": "unknown",
            "classroom": self.classroom_one.id,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("gender", response.data)