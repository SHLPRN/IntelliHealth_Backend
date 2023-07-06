from django.db import models


class Administrator(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Administrator'


class Record(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')
    time = models.DateTimeField()
    date = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Record'


class RecordImage(models.Model):
    record = models.ForeignKey(Record, models.DO_NOTHING, db_column='record')
    image = models.TextField()

    class Meta:
        managed = False
        db_table = 'RecordImage'


class User(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'User'
