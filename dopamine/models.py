
# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    diachi = models.CharField(max_length=255)
    sdt = models.IntegerField()
    email = models.CharField(max_length=255)

class Monan(models.Model):
    ten_monan = models.CharField(max_length=255)
    nguyenlieu_monan = models.CharField(max_length=255)
    hinhanh = models.ImageField(upload_to='images/')

class Congthuc(models.Model):
    tenmon = models.CharField(max_length=255)
    hinhanh = models.ImageField(upload_to='images/')
    ngaythem = models.DateTimeField()
    nguyenlieu = models.CharField(max_length=255)
    huongdan = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Phanloai(models.Model):
    monman = models.CharField(max_length=255)
    monchay = models.CharField(max_length=255)
    thucuong = models.CharField(max_length=255)
    trangmieng = models.CharField(max_length=255)
    nuoccham = models.CharField(max_length=255)
    monan = models.ForeignKey(Monan, on_delete=models.CASCADE)

from.models import Monan

monans = Monan.objects.all()
for monan in monans:
    print(monan.ten_monan)