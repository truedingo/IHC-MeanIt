# Generated by Django 3.0.2 on 2020-01-19 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meanit_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meanituserquestions',
            name='question',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='meanit_app.Questions'),
        ),
    ]