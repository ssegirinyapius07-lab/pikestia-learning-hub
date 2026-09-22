from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Opportunity


def opp_list(request):
    query = request.GET.get('q', '').strip()[:100]
    category = request.GET.get('category', '').strip()

    opportunities = Opportunity.objects.filter(
        status=Opportunity.Status.ACTIVE,
    ).filter(
        Q(deadline__isnull=True) | Q(deadline__gt=timezone.now())
    ).order_by('-published_at')

    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(eligibility__icontains=query)
            | Q(location__icontains=query)
            | Q(source_name__icontains=query)
        )

    valid_categories = {value for value, _ in Opportunity.Category.choices}
    if category in valid_categories:
        opportunities = opportunities.filter(category=category)
    else:
        category = ''

    paginator = Paginator(opportunities, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    filter_params = {}
    if query:
        filter_params['q'] = query
    if category:
        filter_params['category'] = category

    return render(
        request,
        'opportunities/list.html',
        {
            'opportunities': page_obj.object_list,
            'page_obj': page_obj,
            'query': query,
            'selected_category': category,
            'categories': Opportunity.Category.choices,
            'filter_query': urlencode(filter_params),
        },
    )


def opp_detail(request, slug):
    now = timezone.now()
    opp = get_object_or_404(
        Opportunity,
        slug=slug,
        status=Opportunity.Status.ACTIVE,
    )

    if opp.deadline and opp.deadline <= now:
        opp.status = Opportunity.Status.EXPIRED
        opp.save(update_fields=['status'])
        from django.http import Http404
        raise Http404

    return render(request, 'opportunities/detail.html', {'opp': opp})
