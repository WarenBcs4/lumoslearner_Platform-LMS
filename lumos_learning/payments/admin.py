from django.contrib import admin
from .models import Payment, PaymentHistory, Refund


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0
    readonly_fields = ('status', 'notes', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_name', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'course__title', 'material__title')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [PaymentHistoryInline]
    
    actions = ['mark_completed', 'mark_failed', 'mark_refunded']
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"Marked {queryset.count()} payments as completed.")
    mark_completed.short_description = "Mark selected payments as completed"
    
    def mark_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f"Marked {queryset.count()} payments as failed.")
    mark_failed.short_description = "Mark selected payments as failed"
    
    def mark_refunded(self, request, queryset):
        queryset.update(status='refunded')
        self.message_user(request, f"Marked {queryset.count()} payments as refunded.")
    mark_refunded.short_description = "Mark selected payments as refunded"


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('payment', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__user__username',)
    readonly_fields = ('created_at',)


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('payment', 'status', 'refund_amount', 'created_at', 'processed_by')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__user__username', 'reason')
    readonly_fields = ('created_at',)
    
    actions = ['approve_refunds', 'reject_refunds', 'mark_processed']
    
    def approve_refunds(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"Approved {queryset.count()} refunds.")
    approve_refunds.short_description = "Approve selected refunds"
    
    def reject_refunds(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"Rejected {queryset.count()} refunds.")
    reject_refunds.short_description = "Reject selected refunds"
    
    def mark_processed(self, request, queryset):
        queryset.update(status='processed', processed_by=request.user)
        self.message_user(request, f"Marked {queryset.count()} refunds as processed.")
    mark_processed.short_description = "Mark selected refunds as processed"