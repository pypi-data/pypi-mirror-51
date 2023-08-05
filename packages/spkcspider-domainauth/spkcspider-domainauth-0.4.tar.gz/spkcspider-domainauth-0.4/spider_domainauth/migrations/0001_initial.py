# Generated by Django 2.2.1 on 2019-05-30 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spider_base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReverseToken',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=126, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('assignedcontent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='spider_base.AssignedContent')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
