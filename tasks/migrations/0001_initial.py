# Generated by Django 4.0.4 on 2022-04-17 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter project title', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(help_text='Enter task name', max_length=100)),
                ('task_description', models.CharField(blank=True, help_text='Enter task description', max_length=200)),
                ('due_date', models.DateField()),
                ('files', models.FileField(blank=True, null=True, upload_to='attachments/%Y/%m/%d')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.project')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter name for team member', max_length=100)),
                ('email', models.EmailField(help_text='Enter email for team member', max_length=100)),
                ('phone', models.CharField(blank=True, help_text='Enter phone number for team member', max_length=100)),
                ('profile_pic', models.ImageField(blank=True, help_text='Upload profile picture', null=True, upload_to='profile_pics/%Y/%m/%d')),
                ('project', models.ManyToManyField(blank=True, help_text='Assign project for team member', null=True, to='tasks.project')),
                ('task', models.ManyToManyField(blank=True, help_text='Assign task for team member', null=True, to='tasks.task')),
            ],
        ),
    ]
