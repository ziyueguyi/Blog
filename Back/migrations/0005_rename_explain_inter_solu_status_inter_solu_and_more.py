# Generated by Django 5.1a1 on 2024-06-04 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Back', '0004_alter_status_statu_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='explain_inter_solu',
            new_name='inter_solu',
        ),
        migrations.AddField(
            model_name='status',
            name='explain',
            field=models.CharField(default=1, max_length=255, verbose_name='解释信息'),
            preserve_default=False,
        ),
    ]