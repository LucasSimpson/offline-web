# Generated by Django 2.2.3 on 2019-07-14 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0003_auto_20190714_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='domain_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='proxy.Domain'),
            preserve_default=False,
        ),
    ]
