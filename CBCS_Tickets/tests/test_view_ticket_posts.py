from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Ticket
from ..views import ticket_posts


class TicketPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        ticket = Ticket.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', ticket=ticket, created_by=user)
        url = reverse('ticket_posts', kwargs={'pk': board.pk, 'ticket_pk': ticket.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/tickets/1/')
        self.assertEquals(view.func, ticket_posts)