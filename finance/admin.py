from django.contrib import admin
from .models import FeeItem, Invoice, Payment

@admin.register(FeeItem)
class FeeItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_item', 'amount', 'status', 'due_date')
    list_filter = ('status', 'fee_item')
    search_fields = ('student__first_name', 'student__roll_number')
    
    # Quick action to mark as paid from the list
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        rows_updated = queryset.update(status='paid')
        self.message_user(request, f"{rows_updated} invoices marked as paid.")
    mark_as_paid.short_description = "Mark selected invoices as Paid"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount_paid', 'date_paid')