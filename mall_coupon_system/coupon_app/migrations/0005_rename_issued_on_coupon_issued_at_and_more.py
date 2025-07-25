# Generated by Django 4.2.21 on 2025-05-24 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon_app', '0004_remove_store_users_userprofile_user_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='issued_on',
            new_name='issued_at',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='details',
        ),
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='code',
            field=models.CharField(default=0.0, max_length=20),
            preserve_default=False,
        ),
    ]
