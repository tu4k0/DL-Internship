from django.db import models


class ETHBlockchainInfo(models.Model):
    id_info = models.AutoField(primary_key=True, serialize=False)
    node = models.CharField(max_length=255)
    blockNumber = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    protocol = models.IntegerField(null=False)
    id_chain = models.IntegerField(null=False)
    hashrate = models.IntegerField(null=True)
    mining = models.BooleanField(default=False)
    maxFee = models.IntegerField(null=False)
    time = models.DateTimeField(auto_now_add=True)
