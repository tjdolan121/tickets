from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import new_ticket
from ..models import Board, Ticket, Post
from ..forms import NewTicketForm


class NewTicketTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123') ###

    def test_new_ticket_view_success_status_code(self):
        url = reverse('new_ticket', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_ticket_view_not_found_status_code(self):
        url = reverse('new_ticket', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_ticket_url_resolves_new_ticket_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_ticket)

    def test_new_ticket_view_contains_link_back_to_board_tickets_view(self):
        new_ticket_url = reverse('new_ticket', kwargs={'pk': 1})
        board_tickets_url = reverse('board_tickets', kwargs={'pk': 1})
        response = self.client.get(new_ticket_url)
        self.assertContains(response, 'href="{0}"'.format(board_tickets_url))

    def test_csrf(self):
        url = reverse('new_ticket', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_ticket_valid_post_data(self):
        url = reverse('new_ticket', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(url, data)
        self.assertTrue(Ticket.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_ticket_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_ticket', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_ticket_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_ticket', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Ticket.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_ticket', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTicketForm)


class LoginRequiredNewTicketTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_ticket', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))




