from api.game.models import Game
from api.game.serializers import GameNewSerializer, GameSerializer

from rest_framework import permissions, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class GameViewSet(viewsets.ViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        return Response()

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except: # noqa
            raise APIException(404)

    def create(self, request):
        serializer = GameNewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rows = serializer.validated_data['rows']
        columns = serializer.validated_data['columns']
        mines = serializer.validated_data['mines']
        name = serializer.validated_data.get('name')
        game = Game()
        game.new_board(rows, columns, mines)
        if name:
            game.name = name
        game.save()
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)
