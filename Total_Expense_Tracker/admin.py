from django.contrib import admin # type: ignore
from .models import Transaction
from .models import Shift
from .models import GlobalVariable

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'type')

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id','date_created')

class GlobalVariableAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(GlobalVariable, GlobalVariableAdmin)