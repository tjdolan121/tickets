from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Board, Post, Ticket
from ..views import reply_ticket


class ReplyTicketTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.ticket = Ticket.objects.create(subject='Hello, world', board=self.board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', ticket=self.ticket, created_by=user)
        self.url = reverse('reply_ticket', kwargs={'pk': self.board.pk, 'ticket_pk': self.ticket.pk})


# class LoginRequiredReplyTicketTests(ReplyTicketTestCase):
#
#
# class ReplyTicketTests(ReplyTicketTestCase):
#
#
# class SuccessfulReplyTicketTests(ReplyTicketTestCase):
#
#
# class InvalidReplyTicketTests(ReplyTicketTestCase):
