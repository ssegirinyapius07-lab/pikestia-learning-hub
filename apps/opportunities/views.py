from django.shortcuts import render, get_object_or_404
from .models import Opportunity
from django.utils import timezone
from django.db.models import Q

def opp_list(request):
    qs = Opportunity.objects.filter(status='active').filter(
        Q(deadline__isnull=True) | Q(deadline__gt=timezone.now())
    ).order_by('-published_at')
    cat = request.GET.get('category')
    if cat: qs = qs.filter(category=cat)
    return render(request, 'opportunities/list.html', {'opportunities': qs, 'now': timezone.now()})

def opp_detail(request, slug):
    opp = get_object_or_404(Opportunity, slug=slug)
    if opp.is_expired and opp.status=='active':
        opp.status='expired'
        opp.save(update_fields=['status'])
    return render(request, 'opportunities/detail.html', {'opp': opp})
