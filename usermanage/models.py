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

    def __str__(self):
        return self.stuno+" "+self.stuname+" "+self.sex+" "+self.class_field

class Answer(models.Model):
    workname = models.CharField(db_column='workName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    workanswer = models.TextField(db_column='workAnswer', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'answer'

class Score(models.Model):
    stuno = models.OneToOneField('Stu', models.DO_NOTHING, db_column='stuNo', primary_key=True)  # Field name made lowercase.
    worksubmit = models.TextField(db_column='workSubmit', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    workcorrection = models.TextField(db_column='workCorrection', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    workname = models.CharField(db_column='workName', max_length=10)  # Field name made lowercase.
    stuname = models.CharField(db_column='stuName', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'score'
        unique_together = (('stuno', 'workname'),)

class Problem(models.Model):
    workname = models.CharField(max_length=10, blank=True, null=True)
    wrokcontent = models.TextField(db_column='wrokContent', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'problem'

