# Generated by Django 4.1.3 on 2022-11-25 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_comment',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='mainapp.comment', verbose_name='Ответ на комментарий'),
        ),
    ]