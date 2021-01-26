# Generated by Django 3.1.5 on 2021-01-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, default=None, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=300)),
                ('variable', models.CharField(blank=True, choices=[('p', 'p'), ('h1', 'h1'), ('h2', 'h2'), ('h3', 'h3'), ('a', 'a')], default=None, max_length=10)),
                ('field_type', models.CharField(blank=True, choices=[('Text Area', 'Text Area'), ('Text Input', 'Text Input')], default=None, max_length=30)),
                ('answer', models.ManyToManyField(blank=True, default=None, related_name='field', to='question.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=300)),
                ('field', models.ManyToManyField(blank=True, default=None, related_name='form', to='question.Field')),
            ],
        ),
    ]
