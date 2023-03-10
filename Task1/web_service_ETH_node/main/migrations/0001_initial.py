# Generated by Django 4.1.6 on 2023-02-04 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ETHBlockchainInfo',
            fields=[
                ('id_info', models.AutoField(primary_key=True, serialize=False)),
                ('node', models.CharField(max_length=255)),
                ('blockNumber', models.IntegerField()),
                ('price', models.IntegerField()),
                ('protocol', models.IntegerField()),
                ('id_chain', models.IntegerField()),
                ('hashrate', models.IntegerField(null=True)),
                ('mining', models.BooleanField(default=False)),
                ('maxFee', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
