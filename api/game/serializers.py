from api.game import models

from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Game
        fields = ('uid', 'name', 'state', 'moves', 'elapsed_time')


class GameNewSerializer(serializers.Serializer):
    rows = serializers.IntegerField(min_value=2)
    columns = serializers.IntegerField(min_value=2)
    mines = serializers.IntegerField(min_value=1)
    name = serializers.CharField(required=False)


class GameSelectPosSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)


class GameSelectFlagSerializer(GameSelectPosSerializer):
    flag = serializers.CharField(allow_null=True)


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Player
        fields = ('id', 'username')
        read_only_fields = ('username', )


class CreatePlayerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return models.Player.objects.create_user(**validated_data)

    class Meta:
        model = models.Player
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
