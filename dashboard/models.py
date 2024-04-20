from django.db import models

# # Create your models here.
# class ScripMaster(models.Model):
#     token = models.TextField()
#     symbol = models.TextField()
#     name = models.TextField()
#     expiry = models.TextField()
#     strike = models.TextField()
#     lotsize = models.TextField()
#     instrumenttype = models.TextField()
#     exch_seg = models.TextField()
#     tick_size = models.TextField()

#     def __str__(self):
#         return self.name

class Watchlist(models.Model):
    clientId = models.TextField()
    token = models.TextField()
    symbol = models.TextField()