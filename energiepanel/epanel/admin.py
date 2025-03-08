from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from csvexport.actions import csvexport
from django.utils.http import urlencode
from django_object_actions import DjangoObjectActions

from .models import User, BuildingData, EnergyByYear, ResultCache

class BuildingDataAdmin(admin.StackedInline):
    model = BuildingData

class EnergyByYearAdmin(admin.TabularInline):
    model = EnergyByYear

class ResultCacheAdmin(admin.TabularInline):
    model = ResultCache

@admin.register(User)
class UserAdmin(DjangoObjectActions, DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    actions = [csvexport]

    def get_actions(self, request):
        actions = super().get_actions(request)
        #TODO: check for group
        return actions

    inlines = [
        BuildingDataAdmin,
        EnergyByYearAdmin,
        ResultCacheAdmin
    ]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'owner', 'street', 'number', 'parz', 'city', 'plz')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','first_name', 'last_name', 'phone_number', 'owner', 'street', 'number', 'parz', 'city', 'plz'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'owner', 'street', 'number', 'parz', 'city', 'plz','is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'owner', 'street', 'number', 'parz', 'city', 'plz','is_staff')
    ordering = ('email',)

    def publish_this(self, request, obj):
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect("/calculation_admin/?" + urlencode({"username" : obj.username}))
    publish_this.label = "Auswerten"
    publish_this.short_description = "Diesen Nutzer auswerten"

    change_actions = ('publish_this', )


@admin.register(EnergyByYear)
class EnergyByYearAdminGlobal(admin.ModelAdmin):
    model = EnergyByYear

    actions = [csvexport]
    list_display = ('user','jahr','bedarf_heizoel','bedarf_gas','bedarf_strom','bedarf_holz','bedarf_holz_hackschnitzel','bedarf_holzpellets','bedarf_fernwärme_heizstrom',
            'kosten_heizoel','kosten_gas','kosten_strom','kosten_holz','kosten_fernwärme','kosten_andere','eigenstrom_jahresertrag','eigenstrom_netzeinspeisung','eigenstrom_netzeinspeisung_ertrag')

@admin.register(ResultCache)
class ResultCacheAdminGlobal(admin.ModelAdmin):
    model = ResultCache

    actions = [csvexport]
    list_display = ('user','jahr','gek_strom','gek_strom_kosten','gek_waerme','gek_waerme_kosten','gek_total','gek_total_kosten','bauart','ebf')
