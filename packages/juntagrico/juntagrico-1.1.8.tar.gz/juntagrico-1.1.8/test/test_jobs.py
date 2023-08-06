from django.test import TestCase
from django.urls import reverse

from test.util.test import test_simple_get
from test.util.test_data import create_test_data


class JobTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data(cls)

    def testAssignments(self):
        self.client.force_login(self.member.user)
        response = self.client.get(reverse('jobs'))
        self.assertEqual(response.status_code, 200)

    def testAssignmentsAll(self):
        self.client.force_login(self.member.user)
        response = self.client.get(reverse('jobs-all'))
        self.assertEqual(response.status_code, 200)

    def testJob(self):
        test_simple_get(self, reverse('job', args=[self.job1.pk]))

    def testPastJob(self):
        self.client.force_login(self.member.user)
        response = self.client.get(reverse('memberjobs'))
        self.assertEqual(response.status_code, 200)

    def testParticipation(self):
        self.client.force_login(self.member.user)
        response = self.client.get(reverse('areas'))
        self.assertEqual(response.status_code, 200)

    def testTeam(self):
        test_simple_get(self, reverse('area', args=[self.area.pk]))

    def testAreaJoinAndLeave(self):
        test_simple_get(self, reverse('area-join', args=[self.area.pk]))
        self.assertEqual(self.area.members.count(), 1)
        test_simple_get(self, reverse('area-leave', args=[self.area.pk]))
        self.assertEqual(self.area.members.count(), 0)

    def testJobPost(self):
        self.client.force_login(self.member.user)
        response = self.client.post(reverse('job', args=[self.job1.pk]), {'jobs': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.job1.free_slots(), 0)
