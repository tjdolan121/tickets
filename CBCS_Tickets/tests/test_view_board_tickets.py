from django.urls import reverse, resolve
from django.test import TestCase
from ..views import TicketListView
from ..models import Board


class BoardTicketsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board')

    def test_board_tickets_view_success_status_code(self):
        url = reverse('board_tickets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_tickets_view_not_found_status_code(self):
        url = reverse('board_tickets', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_tickets_url_resolves_board_tickets_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TicketListView)

    def test_board_tickets_view_contains_link_back_to_homepage(self):
        board_tickets_url = reverse('board_tickets', kwargs={'pk': 1})
        response = self.client.get(board_tickets_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_board_tickets_view_contains_navigation_links(self):
        board_tickets_url = reverse('board_tickets', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_ticket_url = reverse('new_ticket', kwargs={'pk': 1})

        response = self.client.get(board_tickets_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_ticket_url))
