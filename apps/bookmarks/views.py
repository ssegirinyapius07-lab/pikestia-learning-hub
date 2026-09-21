from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Bookmark
from apps.learning.models import LearningResource

@login_required
def my_bookmarks(request):
    bookmarks = request.user.bookmarks.select_related('resource','topic','opportunity').all()
    return render(request, 'bookmarks/list.html', {'bookmarks': bookmarks})

@login_required
@require_POST
def toggle_bookmark(request):
    resource_id = request.POST.get('resource_id')
    if resource_id:
        res = get_object_or_404(LearningResource, id=resource_id)
        bm, created = Bookmark.objects.get_or_create(user=request.user, resource=res)
        if not created:
            bm.delete()
    return redirect(request.META.get('HTTP_REFERER','/'))
