# Generated by Django 4.2.7 on 2023-12-12 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_friend_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friend_request',
            field=models.ManyToManyField(related_name='user_friend_requests', to='accounts.friend'),
        ),
    ]