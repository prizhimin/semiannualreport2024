from django.contrib import admin
from .models import Company, Report, UserCompany, CreatorsSummaryReport


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'line_number')
    search_fields = ('name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'company')
    list_filter = ('created_at', 'user', 'company')
    search_fields = ('user__username', 'company__name')


admin.site.register(UserCompany)
admin.site.register(CreatorsSummaryReport)


