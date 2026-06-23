import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ophix_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientPackageVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pip_package', models.CharField(max_length=200, unique=True)),
                ('latest_version', models.CharField(max_length=100)),
                ('checked_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Client Package Version',
                'verbose_name_plural': 'Client Package Versions',
                'app_label': 'ophix_client_management',
            },
        ),
        migrations.CreateModel(
            name='ClientVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100)),
                ('pip_package', models.CharField(blank=True, default='', max_length=200)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='version_record', to='ophix_core.client')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
                'app_label': 'ophix_client_management',
            },
        ),
    ]
