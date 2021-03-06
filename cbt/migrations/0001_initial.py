# Generated by Django 3.1 on 2020-12-06 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('start_date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('candidates_no', models.IntegerField(default=10, null=True)),
                ('no_of_questions', models.IntegerField(default=10, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('is_sample', models.BooleanField(default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name of your Institution')),
                ('address', models.CharField(max_length=150, verbose_name='Address of your Institution')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('start_date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('candidates_no', models.IntegerField(default=10, null=True)),
                ('no_of_questions', models.IntegerField(default=10, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('is_sample', models.BooleanField(default=False, null=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.institution')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndividualAssessmentTaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('f', 'FAILED'), ('p', 'PASSED')], default=('f', 'FAILED'), max_length=20)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.individualassessment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionAssessmentTaker',
            fields=[
                ('individualassessment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.individualassessment')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.institutionassessment')),
            ],
            options={
                'abstract': False,
            },
            bases=('cbt.individualassessment',),
        ),
    ]
