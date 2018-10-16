from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.utils import timezone
from django.db.models import Count
from .forms import NewTicketForm, PostForm
from .models import Board, Ticket, Post


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_tickets(request, pk):
    board = get_object_or_404(Board, pk=pk)
    tickets = board.tickets.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'tickets.html', {'board': board, 'tickets': tickets})


@login_required
def new_ticket(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #user = User.objects.first()
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.board = board
            ticket.starter = request.user
            ticket.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                ticket=ticket,
                created_by=request.user
            )

            return redirect('ticket_posts', pk=pk, ticket_pk=ticket.pk)

    else:
        form = NewTicketForm()
    return render(request, 'new_ticket.html', {'board': board, 'form': form})


def ticket_posts(request, pk, ticket_pk):
    ticket = get_object_or_404(Ticket, board__pk=pk, pk=ticket_pk)
    ticket.views += 1
    ticket.save()
    return render(request, 'ticket_posts.html', {'ticket': ticket})


@login_required
def reply_ticket(request, pk, ticket_pk):
    ticket = get_object_or_404(Ticket, board__pk=pk, pk=ticket_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.ticket = ticket
            post.created_by = request.user
            post.save()
            return redirect('ticket_posts', pk=pk, ticket_pk=ticket_pk)
    else:
        form = PostForm()
    return render(request, 'reply_ticket.html', {'ticket': ticket, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('ticket_posts', pk=post.ticket.board.pk, ticket_pk=post.ticket.pk)

