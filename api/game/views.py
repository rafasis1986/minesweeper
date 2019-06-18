import api.constants as c
import api.game.serializers as s
from api.game import models
from api.game.serializers import CreatePlayerSerializer

from django.db.utils import IntegrityError

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = s.GameSerializer

    def get_queryset(self):
        return models.Game.objects.filter(player__id=self.request.user.id).order_by('created')

    def get_object(self, pk):
        try:
            game = models.Game.objects.get(pk=pk, player__id=self.request.user.id)
            return game
        except: # noqa
            raise APIException(detail='No game found')

    def create(self, request):
        serializer = s.GameNewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rows = serializer.validated_data['rows']
        columns = serializer.validated_data['columns']
        mines = serializer.validated_data['mines']
        name = serializer.validated_data.get('name')
        game = models.Game()
        game.player = request.user
        game.new_board(rows, columns, mines)
        if name:
            game.name = name
        game.save()
        serializer = s.GameSerializer(game, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None):
        serializer = s.GameSelectPosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            px = serializer.validated_data['x']
            py = serializer.validated_data['y']
            game = self.get_object(pk)
            if game.is_mine(px, py):
                game.game_over()
            else:
                game.show_cell(px, py)
                if game.is_end_game():
                    game.state = c.WON
            game.save()
            serializer = s.GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except: # noqa
            raise APIException(detail="You can't show this cell")

    @detail_route(methods=['put'])
    def set_flag(self, request, pk=None):
        serializer = s.GameSelectFlagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            px = serializer.validated_data['x']
            py = serializer.validated_data['y']
            flag_str = serializer.validated_data['flag']
            game = self.get_object(pk)
            if flag_str == c.FLAG_CELL:
                game.set_flag(px, py)
            elif flag_str == c.QUESTION_CELL:
                game.set_question(px, py)
            game.save()
            serializer = s.GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except APIException as e:
            raise e
        except: # noqa
            raise APIException(detail="You can't assign a flag in this cell")


class PlayerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = models.Player.objects.all()
    serializer_class = CreatePlayerSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            msg_str = e.args[0].split('DETAIL:')[-1]
            raise APIException(detail=msg_str)
        except Exception as e:
            raise APIException(detail=e.args[0])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
