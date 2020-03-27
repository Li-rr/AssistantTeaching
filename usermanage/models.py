from django.db import models

# Create your models here.
class Stu(models.Model):
    stuno = models.CharField(db_column='stuNo', primary_key=True, max_length=8)  # Field name made lowercase.
    stuname = models.CharField(db_column='stuName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(max_length=2, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=6, blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'stu'

