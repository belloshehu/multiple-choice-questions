# Generated by Django 3.1 on 2020-11-22 21:32

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
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_statement', models.TextField(unique=True)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalCBT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('duration', models.TimeField()),
                ('candidates_no', models.IntegerField(default=10)),
                ('no_of_questions', models.IntegerField(default=10)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_asked', models.TextField(unique=True)),
                ('grade', models.IntegerField(default=5)),
                ('no_of_choices', models.IntegerField(default=4)),
            ],
        ),
        migrations.CreateModel(
            name='OrganisationalCBT',
            fields=[
                ('personalcbt_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.personalcbt')),
            ],
            bases=('cbt.personalcbt',),
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
            name='CBTAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('f', 'FAILED'), ('p', 'PASSED')], default=('f', 'FAILED'), max_length=20)),
                ('cbt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.personalcbt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.question')),
                ('personal_cbt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.personalcbt')),
            ],
            bases=('cbt.question',),
        ),
        migrations.CreateModel(
            name='PersonalChoice',
            fields=[
                ('choice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.choice')),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.personalquestion')),
            ],
            bases=('cbt.choice',),
        ),
        migrations.CreateModel(
            name='OrganisationalQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.question')),
                ('organisational_cbt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.organisationalcbt')),
            ],
            bases=('cbt.question',),
        ),
        migrations.CreateModel(
            name='OrganisationalChoice',
            fields=[
                ('choice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.choice')),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.personalquestion')),
            ],
            bases=('cbt.choice',),
        ),
        migrations.AddField(
            model_name='organisationalcbt',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.institution'),
        ),
        migrations.CreateModel(
            name='InstitutionCBTAssessment',
            fields=[
                ('cbtassessment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cbt.cbtassessment')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt.institution')),
            ],
            bases=('cbt.cbtassessment',),
        ),
    ]
