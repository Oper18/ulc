# coding: utf-8

from rest_framework import serializers

from championat.models import Championat


class ChampionatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championat
        fields = ['id', 'championat', 'season', 'active', 'ended']
