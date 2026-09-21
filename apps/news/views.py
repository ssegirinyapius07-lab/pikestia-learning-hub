from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import NewsArticle


def news_list(request):
    query = request.GET.get('q', '').strip()[:100]
    category = request.GET.get('category', '').strip()

    articles = (
        NewsArticle.objects.filter(status=NewsArticle.Status.PUBLISHED)
        .select_related('author')
        .order_by('-featured', '-published_at', '-created_at')
    )

    if query:
        articles = articles.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(body__icontains=query)
            | Q(author__full_name__icontains=query)
        )

    if category in NewsArticle.Category.values:
        articles = articles.filter(category=category)

    paginator = Paginator(articles, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(
        request,
        'news/list.html',
        {
            'articles': page_obj.object_list,
            'page_obj': page_obj,
            'query': query,
            'selected_category': category if category in NewsArticle.Category.values else '',
            'categories': NewsArticle.Category.choices,
        },
    )


def news_detail(request, slug):
    article = get_object_or_404(
        NewsArticle.objects.select_related('author'),
        slug=slug,
        status=NewsArticle.Status.PUBLISHED,
    )
    related = (
        NewsArticle.objects.filter(
            status=NewsArticle.Status.PUBLISHED,
            category=article.category,
        )
        .exclude(id=article.id)
        .select_related('author')
        .order_by('-published_at', '-created_at')[:4]
    )

    return render(
        request,
        'news/detail.html',
        {
            'article': article,
            'related': related,
        },
    )
