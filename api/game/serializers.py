from api.game.models import Game

from rest_framework import serializers


class GameNewSerializer(serializers.Serializer):
    rows = serializers.IntegerField(min_value=2)
    columns = serializers.IntegerField(min_value=2)
    mines = serializers.IntegerField(min_value=1)
    name = serializers.CharField(required=False)


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('uid', 'name', 'state', 'moves')
