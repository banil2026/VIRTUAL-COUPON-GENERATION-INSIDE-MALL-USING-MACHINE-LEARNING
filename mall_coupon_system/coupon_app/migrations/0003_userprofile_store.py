# Generated by Django 4.2.21 on 2025-05-24 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon_app', '0002_store_users_alter_store_name_alter_store_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coupon_app.store'),
        ),
    ]
