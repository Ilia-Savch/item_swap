from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Ad, Category, ExchangeProposal
from .forms import AdForm, CategoryCreateForm, ExchangeProposalForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
import logging

logger = logging.getLogger("item_swap")


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def form_valid(self, form):
        if not form.is_valid():
            logger.info(form.errors)
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if condition:
            queryset = queryset.filter(condition__iexact=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_condition'] = self.request.GET.get('condition', '')
        context['categories'] = Category.objects.all()
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'


class ExchangeProposalCreateView(CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/exchange_proposal_create.html'

    success_url = reverse_lazy('ads:incoming_proposals')

    def form_valid(self, form):
        form.instance.status = 'pending'
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class IncomingProposalsView(ListView):
    model = ExchangeProposal
    template_name = 'ads/incoming_proposals.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        status = self.request.GET.get('status')

        queryset = ExchangeProposal.objects.filter(
            ad_receiver__user=self.request.user)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class OutgoingProposalsView(ListView):
    model = ExchangeProposal
    template_name = 'ads/outgoing_proposals.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        status = self.request.GET.get('status')

        queryset = ExchangeProposal.objects.filter(
            ad_sender__user=self.request.user)

        if status:
            queryset = queryset.filter(status=status)

        return queryset


class ExchangeProposalStatusUpdateView(UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/exchange_proposal_status_update.html'
    success_url = reverse_lazy('ads:incoming_proposals')

    def get_object(self):
        proposal = super().get_object()
        if proposal.ad_receiver.user != self.request.user:
            raise PermissionDenied(
                "Вы не можете изменить статус этого предложения обмена.")
        return proposal

    def form_valid(self, form):
        if form.cleaned_data['status'] in ['accepted', 'rejected']:
            pass
        return super().form_valid(form)


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'ads/category_create.html'
    success_url = '/new-ad/'
