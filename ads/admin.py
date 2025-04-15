from django.contrib import admin
from ads.models import Ad, ExchangeProposal, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "description",
        "image_url",
        "category",
        "condition",
        "created_at",
    )
    list_filter = ("condition", "created_at")
    search_fields = ("title",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = (
        'ad_sender',
        'ad_receiver',
        'status',
        'created_at',
        'comment'
    )
    search_fields = ('ad_sender__title', 'ad_receiver__title', 'status')
    list_filter = ('status',)
    readonly_fields = ('created_at',)
