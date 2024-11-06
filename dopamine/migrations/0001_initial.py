# Generated by Django 5.1.1 on 2024-11-05 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Monan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_monan', models.CharField(max_length=255)),
                ('nguyenlieu_monan', models.CharField(max_length=255)),
                ('hinhanh', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('diachi', models.CharField(max_length=255)),
                ('sdt', models.IntegerField()),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Phanloai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monman', models.CharField(max_length=255)),
                ('monchay', models.CharField(max_length=255)),
                ('thucuong', models.CharField(max_length=255)),
                ('trangmieng', models.CharField(max_length=255)),
                ('nuoccham', models.CharField(max_length=255)),
                ('monan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dopamine.monan')),
            ],
        ),
        migrations.CreateModel(
            name='Congthuc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenmon', models.CharField(max_length=255)),
                ('hinhanh', models.ImageField(upload_to='images/')),
                ('ngaythem', models.DateTimeField()),
                ('nguyenlieu', models.CharField(max_length=255)),
                ('huongdan', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dopamine.user')),
            ],
        ),
    ]
