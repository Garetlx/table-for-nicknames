# Generated by Django 4.1.1 on 2022-09-10 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50)),
                ('gangs', models.IntegerField()),
                ('forts', models.IntegerField()),
                ('fights', models.IntegerField()),
                ('zvz', models.IntegerField()),
                ('accepted_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
