# Generated by Django 2.2.7 on 2020-10-18 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('provider', models.CharField(max_length=30)),
                ('accuracy', models.FloatField(null=True)),
                ('altitude', models.FloatField(null=True)),
                ('bearing', models.FloatField(null=True)),
                ('speed', models.FloatField(null=True)),
                ('time', models.CharField(max_length=30)),
                ('timestamp', models.BigIntegerField()),
                ('owner', models.CharField(max_length=30)),
            ],
        ),
    ]
