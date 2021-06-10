from django.db import models


class Technician(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    contactnum = models.BigIntegerField(db_column='contactNum', blank=True, null=True)  # Field name made lowercase.
    taddress = models.CharField(db_column='Taddress', max_length=30, blank=True, null=True)  # Field name made lowercase.
    employeedtime = models.DateTimeField(db_column='employeedTime', blank=True, null=True)  # Field name made lowercase.
    salary = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Technician'


class Vipcard(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    holder = models.ForeignKey('Customer', models.DO_NOTHING, db_column='holder', blank=True, null=True)
    registertime = models.DateField(db_column='registerTime', blank=True, null=True)  # Field name made lowercase.
    expiry = models.DateField(blank=True, null=True)
    times = models.IntegerField(blank=True, null=True)
    deposit = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VIPcard'






class Class(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    classtype = models.CharField(db_column='classType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    coach = models.CharField(max_length=10, blank=True, null=True)
    fee = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class'


class Classhistory(models.Model):
    coachid = models.ForeignKey('Coach', models.DO_NOTHING, db_column='coachID', primary_key=True)  # Field name made lowercase.
    studentid = models.BigIntegerField(db_column='studentID')  # Field name made lowercase.
    classid = models.BigIntegerField(db_column='classID')  # Field name made lowercase.
    classtime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classHistory'
        unique_together = (('coachid', 'studentid', 'classid'),)


class Coach(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    coachname = models.CharField(db_column='Coachname', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=6, blank=True, null=True)
    contactnum = models.BigIntegerField(db_column='contactNum', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=30, blank=True, null=True)
    employeedtime = models.DateTimeField(db_column='employeedTime', blank=True, null=True)  # Field name made lowercase.
    salary = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    speciality = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coach'


class Customer(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customername = models.CharField(db_column='Customername', unique=True, max_length=10)  # Field name made lowercase.
    gender = models.CharField(max_length=6, blank=True, null=True)
    contactnum = models.BigIntegerField(db_column='contactNum', blank=True, null=True)  # Field name made lowercase.
    registertime = models.DateTimeField(db_column='registerTime', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=20, blank=True, null=True)
    membership = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'
        unique_together = (('id', 'customername'),)





class Equipment(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    equipname = models.CharField(db_column='Equipname', max_length=10, blank=True, null=True)  # Field name made lowercase.
    equipdata = models.BinaryField(db_column='EquipData', blank=True, null=True)  # Field name made lowercase.
    equipextn = models.CharField(db_column='Equipextn', max_length=10, blank=True, null=True)  # Field name made lowercase.
    purchasedtime = models.DateField(db_column='purchasedTime', blank=True, null=True)  # Field name made lowercase.
    lastfix = models.CharField(db_column='lastFix', max_length=10, blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment'


class Maintenance(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fixday = models.DateField(db_column='fixDay', blank=True, null=True)  # Field name made lowercase.
    equipid = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='equipID', blank=True, null=True)  # Field name made lowercase.
    repairman = models.ForeignKey(Technician, models.DO_NOTHING, db_column='repairman', blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maintenance'


class Manager(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    managername = models.CharField(db_column='Managername', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=6, blank=True, null=True)
    contactnum = models.BigIntegerField(db_column='contactNum', blank=True, null=True)  # Field name made lowercase.
    maddress = models.CharField(db_column='Maddress', max_length=30, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=20, blank=True, null=True)
    employeedtime = models.DateTimeField(db_column='employeedTime', blank=True, null=True)  # Field name made lowercase.
    salary = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manager'


class Student(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contactnum = models.BigIntegerField(db_column='contactNum', blank=True, null=True)  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='classID')  # Field name made lowercase.
    classtime = models.CharField(db_column='classTime', max_length=10, blank=True, null=True)  # Field name made lowercase.
    classstart = models.DateTimeField(db_column='classStart', blank=True, null=True)  # Field name made lowercase.
    classleft = models.IntegerField(db_column='classLeft', blank=True, null=True)  # Field name made lowercase.
    coach = models.ForeignKey(Coach, models.DO_NOTHING, db_column='coach', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'
        unique_together = (('id', 'classid'),)
