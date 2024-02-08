import json
import pandas as pd

from django.core.management.base import BaseCommand
from django.db.models import QuerySet, Q, Count, Case, When, IntegerField, Sum, F
from datetime import datetime, time, date

from app.models import *
from Appointment.models import *
from generic.models import YQPointRecord
from yp_library.models import LendRecord

class Command(BaseCommand):
    help = '导出2023寒假科研竞赛数据'

    def task1(self):
        participant = CourseParticipant.objects.select_related("course", "person")
        course_table = participant.values(
            "course_id"
        ).annotate(all=Count("person"), success=Count(
            Case(When(status=2, then=1), output_field=IntegerField()))
        ).values_list(
            "course__id", "course__name", "course__year", "course__semester", "course__type", 
            "course__capacity", "all", "success"
        )
        # df = pd.DataFrame(course_table, columns=["course id", "course name", "year", "semester", "type", "capacity", "selection", "success"])
        # df.to_csv("course.csv")

        records = CourseRecord.objects.select_related("person", "course")
        record_table = records.values_list(
            "person_id", "course__id", "course__name", "course__type", "year", "semester", "total_hours"
        )
        df = pd.DataFrame(record_table, columns=["person id", "course id", "course name", "type", "year", "semester", "hours"])
        df.to_csv("record.csv")

        hour_table = records.values("person_id").annotate(
            de=Sum("total_hours", filter=Q(course__type=0)),
            zhi=Sum("total_hours", filter=Q(course__type=1)),
            ti=Sum("total_hours", filter=Q(course__type=2)),
            mei=Sum("total_hours", filter=Q(course__type=3)),
            lao=Sum("total_hours", filter=Q(course__type=4)),
            total=Sum("total_hours")
        ).values_list(
            "person_id", "person__stu_id_dbonly", "de", "zhi", "ti", "mei", "lao", "total"
        )
        # df = pd.DataFrame(hour_table, columns=["person id", "stu grade", "de", "zhi", "ti", "mei", "lao", "total"])
        # five = ["de", "zhi", "ti", "mei", "lao"]
        # df["other"] = df["total"] - df[five].sum(axis=1)
        # df["stu grade"] = df["stu grade"].map(lambda x: "20"+x[:2])
        # df.to_csv("hour.csv")


    def task2(self):
        start = datetime(year=2022, month=7, day=1)
        finish = datetime(year=2024, month=1, day=24)
        appointment = Appoint.objects.all().filter(Astart__gte=start).filter(Afinish__lte=finish).values_list(
            "Astart", "Afinish", "Room", "Ayp_num", "Anon_yp_num", "Atype", "Astatus", "Areason"
        )
        df = pd.DataFrame(appointment, columns=["start time", "finish time", "room id", "yuanpei students", "other students", "type", "status", "reason"])
        df.to_csv("Task2.csv")
    

    def task3(self):
        start = datetime(year=2023, month=11, day=1)
        end = datetime(year=2024, month=1, day=1)

        yqp_record = YQPointRecord.objects.filter(time__gte=start).filter(time__lte=end).filter(source_type=YQPointRecord.SourceType.CONSUMPTION).values_list(
            "user", "source"
        )
        df = pd.DataFrame(yqp_record, columns=["person_id", "type"])
        df.to_csv("yqp.csv")

        s = datetime(year=2023, month=1, day=1)
        lend_record = LendRecord.objects.filter(lend_time__lte=end).filter(due_time__gte=s).select_related("book_id").values_list(
            "reader_id", "book_id__identity_code", "lend_time", "due_time", "return_time"
        )
        df = pd.DataFrame(lend_record, columns=["person_id", "book_type", "lend_time", "due_time", "return_time"])
        df["book_type"] = df["book_type"].map(lambda x: x[0])
        times = ["lend_time", "due_time", "return_time"]
        for t in times:
            df[t] = df[t].dt.normalize()
            df[t] = df[t].dt.floor('D')
        df.to_csv("lib.csv")

        participant = CourseParticipant.objects.select_related("course", "person").filter(status=2)
        course_table = participant.values(
            "person__id"
        ).annotate(
            all=Count("course"), 
            de=Count("course", filter=Q(course__type=0)),
            zhi=Count("course", filter=Q(course__type=1)),
            ti=Count("course", filter=Q(course__type=2)),
            mei=Count("course", filter=Q(course__type=3)),
            lao=Count("course", filter=Q(course__type=4)),
        ).values_list(
            "person__id", "all", "de", "zhi", "ti", "mei", "lao"
        )
        df = pd.DataFrame(course_table, columns=["person_id", "all", "de", "zhi", "ti", "mei", "lao"])
        df = df.to_csv("select.csv")

        position = Position.objects.activated().select_related("person", "org").values(
            "person", orgnum=Count("org")
        ).values_list(
            "person", "orgnum"
        )
        activity_info = Participation.objects.activated().filter(activity__start__gte=start).filter(activity__end__lte=end).select_related("person", "activity", "activity__organization_id").values(
            "person"
        ).annotate(actnum=Count("activity")).values_list(
            "person", "actnum"
        )
        perorg = dict((x[0], x[1]) for x in position)
        peract = dict((x[0], x[1]) for x in activity_info)
        u = []
        for per in perorg.keys():
            if per not in peract: continue
            u.append((per, perorg[per], peract[per]))
        df = pd.DataFrame(u, columns=["person_id", "orgnization_num", "active"])
        df.to_csv("org.csv")


    def handle(self, *args, **option):
        self.task3()