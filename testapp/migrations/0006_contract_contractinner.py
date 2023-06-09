# Generated by Django 4.2.1 on 2023-05-30 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cNumber', models.CharField(default='', max_length=50)),
                ('cClient', models.CharField(max_length=20)),
                ('cLocation', models.CharField(max_length=20)),
                ('cContent', models.TextField()),
                ('cPayMode', models.CharField(max_length=20)),
                ('cBudget', models.CharField(max_length=20)),
                ('cOther', models.TextField()),
                ('cConfirm', models.CharField(default='_年_月_日決定以___元整交由__承攬本工程', max_length=5)),
                ('cGeneral_Sign', models.CharField(blank=True, max_length=20)),
                ('cViceGeneral_Sign', models.CharField(blank=True, max_length=20)),
                ('cManager_Sign', models.CharField(blank=True, max_length=20)),
                ('cDepartmentManager_Sign', models.CharField(blank=True, max_length=20)),
                ('home', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='testapp.home')),
            ],
        ),
        migrations.CreateModel(
            name='ContractInner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cContractor', models.CharField(max_length=20)),
                ('cQuotation', models.CharField(max_length=20)),
                ('cBargain1', models.CharField(max_length=20)),
                ('cBargain2', models.CharField(max_length=20)),
                ('cRemark', models.TextField()),
                ('innercontract', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='details', to='testapp.contract')),
            ],
        ),
    ]
