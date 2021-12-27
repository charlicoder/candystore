# Generated by Django 4.0 on 2021-12-16 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferalCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(editable=False, max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('new', 'New')], default='new', max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.candyuser')),
            ],
        ),
        migrations.CreateModel(
            name='CandyUserReferral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('new', 'New')], default='new', max_length=20)),
                ('child', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='users.candyuser')),
                ('parent', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='users.candyuser')),
                ('referral_code', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='mlm.referalcode')),
            ],
        ),
    ]