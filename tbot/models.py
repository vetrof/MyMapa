from django.db import models


class TypeNotes(models.Model):
    name = models.CharField(max_length=100)


class TgUser(models.Model):
    chat_id = models.IntegerField()
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)


class Places(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()

    country = models.CharField(max_length=100, blank=True, null=True)
    district_country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district_city = models.CharField(max_length=100, blank=True, null=True)

    type = models.ManyToManyField(TypeNotes, blank=True)

    title = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)


class Gallery(models.Model):
    image = models.ImageField(upload_to="mapa_image")
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
