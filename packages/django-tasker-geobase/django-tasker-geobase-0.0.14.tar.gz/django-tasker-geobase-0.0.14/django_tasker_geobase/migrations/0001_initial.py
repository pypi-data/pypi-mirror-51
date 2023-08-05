# Generated by Django 2.2.2 on 2019-07-02 10:26

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geobase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en', models.CharField(db_index=True, max_length=200)),
                ('ru', models.CharField(db_index=True, max_length=200)),
                ('type', models.SmallIntegerField(choices=[(1, 'Country'), (2, 'Province'), (3, 'Area'), (4, 'Locality'), (5, 'District'), (6, 'Street'), (7, 'House'), (8, 'Hydro'), (9, 'Railway'), (10, 'Route'), (11, 'Vegetation'), (12, 'Airport'), (13, 'Metro'), (14, 'Other'), (15, 'Apartment')], null=True)),
                ('timezone', models.CharField(blank=True, max_length=255, null=True, verbose_name='timezone')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('zipcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='Zipcode')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_tasker_geobase.Geobase')),
            ],
            options={
                'verbose_name': 'Geobase',
                'verbose_name_plural': 'Geobase',
            },
        ),
        migrations.CreateModel(
            name='ZipcodePostOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='Zipcode')),
                ('geobase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_tasker_geobase.Geobase')),
            ],
        ),
    ]
