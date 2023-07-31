from django.contrib import admin
from .models import ShortenedLink
from .utils import count_link_clicks

class ShortenedLinkAdmin(admin.ModelAdmin):
    list_display = ('original_link', 'shortened_link', 'link_title', 'click_count')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for link in queryset:
            link.click_count = count_link_clicks(link.shortened_link)
            link.save()
        return queryset

admin.site.register(ShortenedLink, ShortenedLinkAdmin)
