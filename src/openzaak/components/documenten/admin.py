from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from privates.admin import PrivateMediaMixin

from openzaak.utils.admin import (
    AuditTrailAdminMixin,
    AuditTrailInlineAdminMixin,
    EditInlineAdminMixin,
    ListObjectActionsAdminMixin,
    UUIDAdminMixin,
    link_to_related_objects,
)

from .api import viewsets
from .models import (
    EnkelvoudigInformatieObject,
    EnkelvoudigInformatieObjectCanonical,
    Gebruiksrechten,
    ObjectInformatieObject,
)


@admin.register(Gebruiksrechten)
class GebruiksrechtenAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("informatieobject", "startdatum", "einddatum")
    list_filter = ("startdatum", "einddatum")
    search_fields = (
        "uuid",
        "informatieobject__enkelvoudiginformatieobject__uuid",
        "informatieobject__enkelvoudiginformatieobject__identificatie",
        "omschrijving_voorwaarden",
    )
    date_hierarchy = "startdatum"
    ordering = ("startdatum", "informatieobject")
    raw_id_fields = ("informatieobject",)
    viewset = viewsets.GebruiksrechtenViewSet


@admin.register(ObjectInformatieObject)
class ObjectInformatieObjectAdmin(
    AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin
):
    list_display = ("informatieobject", "object_type", "get_object_display")
    list_filter = ("object_type",)
    list_select_related = ("informatieobject", "_zaak", "_besluit")
    search_fields = (
        "uuid",
        "informatieobject__enkelvoudiginformatieobject__uuid",
        "informatieobject__enkelvoudiginformatieobject__identificatie",
        "_zaak__uuid",
        "_zaak__identificatie",
        "_zaak_url",
        "_besluit__uuid",
        "_besluit__identificatie",
        "_besluit_url",
    )
    ordering = ("informatieobject",)
    raw_id_fields = ("informatieobject", "_zaak", "_besluit")
    viewset = viewsets.ObjectInformatieObject

    def get_object_display(self, obj):
        return obj._zaak or obj._zaak_url or obj._besluit or obj._besluit_url

    get_object_display.short_description = "object"


class GebruiksrechtenInline(EditInlineAdminMixin, admin.TabularInline):
    model = Gebruiksrechten
    fields = GebruiksrechtenAdmin.list_display
    fk_name = "informatieobject"


class ObjectInformatieObjectInline(
    AuditTrailAdminMixin, EditInlineAdminMixin, admin.TabularInline
):
    model = ObjectInformatieObject
    fields = ObjectInformatieObjectAdmin.list_display
    fk_name = "informatieobject"

    def get_object_display(self, obj):
        return obj._zaak or obj._zaak_url or obj._besluit or obj._besluit_url

    get_object_display.short_description = "object"


class EnkelvoudigInformatieObjectInline(
    AuditTrailInlineAdminMixin, admin.StackedInline
):
    model = EnkelvoudigInformatieObject
    raw_id_fields = ("canonical", "_informatieobjecttype")
    readonly_fields = ("uuid",)
    extra = 1
    verbose_name = _("versie")
    verbose_name_plural = _("versies")
    viewset = viewsets.EnkelvoudigInformatieObjectViewSet


def unlock(modeladmin, request, queryset):
    queryset.update(lock="")


@admin.register(EnkelvoudigInformatieObjectCanonical)
class EnkelvoudigInformatieObjectCanonicalAdmin(AuditTrailAdminMixin, admin.ModelAdmin):
    list_display = ["__str__", "get_not_lock_display"]
    inlines = [
        EnkelvoudigInformatieObjectInline,
        GebruiksrechtenInline,
        ObjectInformatieObjectInline,
    ]
    actions = [unlock]

    def get_not_lock_display(self, obj) -> bool:
        return not bool(obj.lock)

    get_not_lock_display.short_description = "free to change"
    get_not_lock_display.boolean = True

    def get_viewset(self, request):
        return None


@admin.register(EnkelvoudigInformatieObject)
class EnkelvoudigInformatieObjectAdmin(
    AuditTrailAdminMixin,
    ListObjectActionsAdminMixin,
    UUIDAdminMixin,
    PrivateMediaMixin,
    admin.ModelAdmin,
):
    list_display = (
        "identificatie",
        "bronorganisatie",
        "creatiedatum",
        "titel",
        "versie",
        "_locked",
    )
    list_filter = ("bronorganisatie",)
    search_fields = ("identificatie", "uuid")
    ordering = ("-begin_registratie",)
    date_hierarchy = "creatiedatum"
    raw_id_fields = ("canonical", "_informatieobjecttype")
    viewset = viewsets.EnkelvoudigInformatieObjectViewSet
    private_media_fields = ("inhoud",)

    fieldsets = (
        (
            _("Identificatie"),
            {
                "fields": (
                    "uuid",
                    "identificatie",
                    "canonical",
                    "bronorganisatie",
                    "creatiedatum",
                    "versie",
                )
            },
        ),
        (
            _("Typering"),
            {"fields": ("_informatieobjecttype_url", "_informatieobjecttype",)},
        ),
        (
            _("Documentgegevens"),
            {
                "fields": (
                    "vertrouwelijkheidaanduiding",
                    "titel",
                    "auteur",
                    "status",
                    "beschrijving",
                    "formaat",
                    "taal",
                    "bestandsnaam",
                    "inhoud",
                    "link",
                    "indicatie_gebruiksrecht",
                )
            },
        ),
        (
            _("Verzending/ontvangst"),
            {"fields": ("ontvangstdatum", "verzenddatum",), "classes": ("collapse",),},
        ),
        (
            _("Ondertekening"),
            {
                "fields": ("ondertekening_soort", "ondertekening_datum",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Integriteit"),
            {
                "fields": (
                    "integriteit_algoritme",
                    "integriteit_waarde",
                    "integriteit_datum",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def _locked(self, obj) -> bool:
        return obj.locked

    _locked.boolean = True
    _locked.short_description = _("locked")

    def get_object_actions(self, obj):
        return (
            link_to_related_objects(Gebruiksrechten, obj.canonical),
            link_to_related_objects(ObjectInformatieObject, obj.canonical),
        )
