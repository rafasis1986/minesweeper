import uuid

import api.constants as c
import api.snippets as snip

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields.array import ArrayField
from django.db import models


class CustomUserManager(UserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, email, password, **extra_fields)


class Player(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = CustomUserManager()

    class Meta:
        db_table = 'player'


class Game(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(Player, related_name='games', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    elapsed_time = models.PositiveIntegerField(default=0)
    board = ArrayField(ArrayField(models.SmallIntegerField()))
    moves = ArrayField(ArrayField(models.CharField(max_length=1)))
    state = models.CharField(max_length=25, choices=c.STATES, default=c.NEW)
    name = models.CharField(max_length=100)
    mines = models.PositiveIntegerField(default=0)
    flags = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'game'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name in [None, '']:
            self.name = 'game #%s' % self.uid
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using,
                                 update_fields=update_fields)

    def game_over(self):
        self.state = c.LOST
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] == c.MINE_CELL:
                    self.moves[y][x] = c.MINE_CELL

    def is_mine(self, x, y):
        return self.board[y][x] == c.MINE_CELL

    def is_end_game(self):
        hidden_count = snip.count_hidden_cells(self.moves)
        return hidden_count == self.mines

    def new_board(self, rows, cols, mines):
        self.mines = mines
        self.board = snip.init_array(rows, cols, c.SAFE_CELL)
        self.moves = snip.init_array(rows, cols, c.HIDDEN_CELL)
        snip.insert_mines(self.board, mines)

    def set_flag(self, x, y):
        assert self.flags < self.mines
        assert self.moves[y][x] == c.HIDDEN_CELL
        self.flags += 1
        self.moves[x][y] = c.FLAG_CELL

    def set_question(self, x, y):
        assert self.moves[y][x] == c.HIDDEN_CELL
        self.flags += 1
        self.moves[x][y] = c.QUESTION_CELL

    def show_cell(self, x, y):
        if self.moves[y][x] != c.HIDDEN_CELL:
            return
        snip.show_adjacent_cells(self.board, self.moves, x, y)

    def remove_flag(self, x, y):
        assert self.moves[y][x] == c.FLAG_CELL
        self.moves[x][y] = c.HIDDEN_CELL
        self.flags -= 1

    def remove_question(self, x, y):
        assert self.moves[y][x] == c.QUESTION_CELL
        self.moves[x][y] = c.HIDDEN_CELL
