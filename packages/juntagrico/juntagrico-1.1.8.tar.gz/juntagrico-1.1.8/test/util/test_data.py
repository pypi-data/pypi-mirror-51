from django.contrib.auth.models import Permission
from django.utils import timezone

from juntagrico.entity.depot import Depot
from juntagrico.entity.member import Member
from juntagrico.entity.jobs import ActivityArea, JobType, RecuringJob, Assignment, OneTimeJob


def create_test_data(cls):
    """
    member
    """
    member_data = {'first_name': 'first_name',
                   'last_name': 'last_name',
                   'email': 'test@email.org',
                   'addr_street': 'addr_street',
                   'addr_zipcode': 'addr_zipcode',
                   'addr_location': 'addr_location',
                   'phone': 'phone',
                   'confirmed': True,
                   }
    cls.member = Member.objects.create(**member_data)
    cls.member.user.set_password("12345")
    cls.member.user.user_permissions.add(
        Permission.objects.get(codename='is_depot_admin'))
    cls.member.user.user_permissions.add(
        Permission.objects.get(codename='can_filter_subscriptions'))
    cls.member.user.save()

    """
    admin member
    """
    admin_data = {'first_name': 'admin',
                  'last_name': 'last_name',
                  'email': 'admin@email.org',
                  'addr_street': 'addr_street',
                  'addr_zipcode': 'addr_zipcode',
                  'addr_location': 'addr_location',
                  'phone': 'phone',
                  'confirmed': True,
                  }
    cls.admin = Member.objects.create(**admin_data)
    cls.admin.user.set_password("123456")
    cls.admin.user.is_staff = True
    cls.admin.user.is_superuser = True
    cls.admin.user.save()

    """
    area
    """
    area_data = {'name': 'name',
                 'coordinator': cls.member}
    cls.area = ActivityArea.objects.create(**area_data)
    """
    job_type
    """
    job_type_data = {'name': 'name',
                     'activityarea': cls.area,
                     'duration': 2}
    cls.job_type = JobType.objects.create(**job_type_data)
    """
    jobs
    """
    time = timezone.now()+timezone.timedelta(hours=2)
    job_data = {'slots': 1,
                'time': time,
                'type': cls.job_type}
    cls.job1 = RecuringJob.objects.create(**job_data)
    cls.job2 = RecuringJob.objects.create(**job_data)
    """
    one time jobs
    """
    time = timezone.now()+timezone.timedelta(hours=2)
    one_time_job_data = {'name': 'name',
                         'activityarea': cls.area,
                         'duration': 2,
                         'slots': 1,
                         'time': time}
    cls.one_time_job1 = OneTimeJob.objects.create(**one_time_job_data)
    one_time_job_data['name'] = 'name2'
    cls.one_time_job2 = OneTimeJob.objects.create(**one_time_job_data)
    """
    assignment
    """
    assignment_data = {'job': cls.job2,
                       'member': cls.member,
                       'amount': 1}
    Assignment.objects.create(**assignment_data)
    """
    depot
    """
    depot_data = {
        'code': 'c1',
        'name': 'depot',
        'contact': cls.member,
        'weekday': 1}
    cls.depot = Depot.objects.create(**depot_data)
    return cls.member.user
