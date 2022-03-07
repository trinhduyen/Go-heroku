# Generated by Django 4.0.2 on 2022-03-03 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DX', '0003_alter_vattudung_trangthaikho_alter_vattudung_dongia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vattudung',
            name='DatetimeXuat',
            field=models.DateField(blank=True, null=True, verbose_name='Thời Gian Xuất'),
        ),
        migrations.AlterField(
            model_name='vattudung',
            name='TrangThaiKho',
            field=models.CharField(choices=[('Không', 'Không'), ('Có', 'Có')], max_length=50, verbose_name='Trạng Thái Kho'),
        ),
        migrations.AlterField(
            model_name='xevao',
            name='datetimeXera',
            field=models.DateField(blank=True, null=True, verbose_name='Thời Gian Xe Ra'),
        ),
        migrations.AlterField(
            model_name='xevao',
            name='datetimeXevao',
            field=models.DateField(verbose_name='Thời Gian Xe Vào'),
        ),
    ]