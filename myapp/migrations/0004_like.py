# Generated by Django 2.1.7 on 2019-11-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_ads_customers_words'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('cust_id', models.IntegerField()),
                ('ads_id', models.IntegerField()),
                ('weight', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'like',
                'managed': False,
            },
        ),
    ]
