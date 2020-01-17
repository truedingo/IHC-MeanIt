# Generated by Django 3.0.2 on 2020-01-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meanit_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='question_answer',
        ),
        migrations.AddField(
            model_name='meanituserquestions',
            name='question_answer',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='meanituserquestions',
            name='question_name',
            field=models.CharField(default='Question', max_length=512, unique=True),
        ),
    ]
