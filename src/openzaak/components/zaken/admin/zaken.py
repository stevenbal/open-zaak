from django.contrib import admin

from openzaak.utils.admin import (
    AuditTrailAdminMixin,
    EditInlineAdminMixin,
    ListObjectActionsAdminMixin,
    UUIDAdminMixin,
    link_to_related_objects,
)

from ..models import (
    KlantContact,
    RelevanteZaakRelatie,
    Resultaat,
    Rol,
    Status,
    Zaak,
    ZaakBesluit,
    ZaakEigenschap,
    ZaakInformatieObject,
    ZaakObject,
)
from .betrokkenen import (
    MedewerkerInline,
    NatuurlijkPersoonInline,
    NietNatuurlijkPersoonInline,
    OrganisatorischeEenheidInline,
    VestigingInline,
)
from .objecten import (
    AdresInline,
    BuurtInline,
    GemeenteInline,
    GemeentelijkeOpenbareRuimteInline,
    HuishoudenInline,
    InrichtingselementInline,
    KadastraleOnroerendeZaakInline,
    KunstwerkdeelInline,
    MaatschappelijkeActiviteitInline,
    OpenbareRuimteInline,
    OverigeInline,
    PandInline,
    SpoorbaandeelInline,
    TerreindeelInline,
    TerreinGebouwdObjectInline,
    WaterdeelInline,
    WegdeelInline,
    WijkInline,
    WoonplaatsInline,
    WozDeelobjectInline,
    WozObjectInline,
    WozWaardeInline,
    ZakelijkRechtInline,
)


@admin.register(Status)
class StatusAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "datum_status_gezet")
    list_select_related = ("zaak",)
    list_filter = ("datum_status_gezet",)
    search_fields = (
        "uuid",
        "zaak__identificatie",
        "zaak__uuid",
        "statustoelichting",
    )
    ordering = ("datum_status_gezet",)
    date_hierarchy = "datum_status_gezet"
    raw_id_fields = ("zaak", "_statustype")
    viewset = "openzaak.components.zaken.api.viewsets.StatusViewSet"


@admin.register(ZaakObject)
class ZaakObjectAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "object_type", "object", "relatieomschrijving")
    list_select_related = ("zaak",)
    list_filter = ("object_type",)
    search_fields = (
        "uuid",
        "object",
        "relatieomschrijving",
        "zaak__identificatie",
        "zaak__uuid",
    )
    ordering = ("object_type", "object")
    raw_id_fields = ("zaak",)
    viewset = "openzaak.components.zaken.api.viewsets.ZaakObjectViewSet"
    inlines = [
        AdresInline,
        BuurtInline,
        GemeenteInline,
        GemeentelijkeOpenbareRuimteInline,
        HuishoudenInline,
        InrichtingselementInline,
        KadastraleOnroerendeZaakInline,
        KunstwerkdeelInline,
        MaatschappelijkeActiviteitInline,
        OpenbareRuimteInline,
        OverigeInline,
        PandInline,
        SpoorbaandeelInline,
        TerreindeelInline,
        TerreinGebouwdObjectInline,
        WaterdeelInline,
        WegdeelInline,
        WijkInline,
        WoonplaatsInline,
        WozDeelobjectInline,
        WozObjectInline,
        WozWaardeInline,
        ZakelijkRechtInline,
        NatuurlijkPersoonInline,
        NietNatuurlijkPersoonInline,
        OrganisatorischeEenheidInline,
        VestigingInline,
        MedewerkerInline,
    ]


@admin.register(KlantContact)
class KlantContactAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "identificatie", "datumtijd", "kanaal")
    list_select_related = ("zaak",)
    list_filter = ("datumtijd",)
    search_fields = (
        "uuid",
        "identificatie",
        "toelichting",
        "kanaal",
        "zaak__identificatie",
        "zaak__uuid",
    )
    date_hierarchy = "datumtijd"
    ordering = ("-identificatie", "datumtijd")
    raw_id_fields = ("zaak",)
    viewset = "openzaak.components.zaken.api.viewsets.KlantContactViewSet"


@admin.register(ZaakEigenschap)
class ZaakEigenschapAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "_eigenschap", "_eigenschap_url", "waarde")
    list_select_related = ("zaak",)
    list_filter = ("_naam",)
    search_fields = (
        "uuid",
        "_naam",
        "zaak__identificatie",
        "zaak__uuid",
    )
    ordering = ("zaak", "_eigenschap", "_eigenschap_url")
    raw_id_fields = ("zaak", "_eigenschap")
    viewset = "openzaak.components.zaken.api.viewsets.ZaakEigenschapViewSet"


@admin.register(ZaakInformatieObject)
class ZaakInformatieObjectAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = (
        "zaak",
        "_informatieobject",
        "_informatieobject_url",
        "registratiedatum",
        "titel",
        "beschrijving",
    )
    list_select_related = ("zaak", "_informatieobject")
    list_filter = ("aard_relatie",)
    search_fields = (
        "uuid",
        "zaak__identificatie",
        "zaak__uuid",
        "_informatieobject__enkelvoudiginformatieobject__uuid",
        "_informatieobject__enkelvoudiginformatieobject__identificatie",
        "_informatieobject_url",
    )
    date_hierarchy = "registratiedatum"
    ordering = ("zaak", "_informatieobject", "_informatieobject_url")
    raw_id_fields = ("zaak", "_informatieobject")
    viewset = "openzaak.components.zaken.api.viewsets.ZaakInformatieObjectViewSet"


@admin.register(Resultaat)
class ResultaatAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "toelichting")
    list_select_related = ("zaak", "_resultaattype")
    search_fields = (
        "uuid",
        "toelichting",
        "_resultaattype__uuid",
        "_resultaattype_url",
        "zaak__identificatie",
        "zaak__uuid",
    )
    ordering = ("zaak",)
    raw_id_fields = ("zaak", "_resultaattype")
    viewset = "openzaak.components.zaken.api.viewsets.ResultaatViewSet"


@admin.register(Rol)
class RolAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "betrokkene", "betrokkene_type")
    list_select_related = ("zaak",)
    list_filter = ("betrokkene_type", "indicatie_machtiging", "registratiedatum")
    search_fields = (
        "uuid",
        "zaak__identificatie",
        "zaak__uuid",
        "betrokkene",
        "omschrijving",
        "roltoelichting",
    )
    date_hierarchy = "registratiedatum"
    ordering = ("registratiedatum", "betrokkene")
    raw_id_fields = ("zaak", "_roltype")
    viewset = "openzaak.components.zaken.api.viewsets.RolViewSet"
    inlines = [
        NatuurlijkPersoonInline,
        NietNatuurlijkPersoonInline,
        OrganisatorischeEenheidInline,
        VestigingInline,
        MedewerkerInline,
    ]


@admin.register(RelevanteZaakRelatie)
class RelevanteZaakRelatieAdmin(admin.ModelAdmin):
    list_display = ("zaak", "_relevant_zaak", "_relevant_zaak_url", "aard_relatie")
    list_filter = ("aard_relatie",)
    search_fields = (
        "zaak__uuid",
        "zaak__identificatie",
        "_relevant_zaak__uuid",
        "_relevant_zaak__identificatie",
        "_relevant_zaak_url",
    )
    ordering = ("zaak", "_relevant_zaak", "_relevant_zaak_url")
    raw_id_fields = ("zaak", "_relevant_zaak")
    list_select_related = ("zaak", "_relevant_zaak")


@admin.register(ZaakBesluit)
class ZaakBesluitAdmin(AuditTrailAdminMixin, UUIDAdminMixin, admin.ModelAdmin):
    list_display = ("zaak", "_besluit", "_besluit_url")
    list_select_related = ("zaak", "_besluit")
    search_fields = (
        "uuid",
        "zaak__uuid",
        "zaak__identificatie",
        "_besluit__uuid",
        "_besluit__identificatie",
        "_besluit_url",
    )
    ordering = ("zaak", "_besluit", "_besluit_url")
    raw_id_fields = ("zaak", "_besluit")
    viewset = "openzaak.components.zaken.api.viewsets.ZaakBesluitViewSet"


# inline classes for Zaak
class StatusInline(EditInlineAdminMixin, admin.TabularInline):
    model = Status
    fields = StatusAdmin.list_display
    fk_name = "zaak"


class ZaakObjectInline(EditInlineAdminMixin, admin.TabularInline):
    model = ZaakObject
    fields = ZaakObjectAdmin.list_display
    fk_name = "zaak"


class ZaakEigenschapInline(EditInlineAdminMixin, admin.TabularInline):
    model = ZaakEigenschap
    fields = ZaakEigenschapAdmin.list_display
    fk_name = "zaak"


class ZaakInformatieObjectInline(EditInlineAdminMixin, admin.TabularInline):
    model = ZaakInformatieObject
    fields = ZaakInformatieObjectAdmin.list_display
    fk_name = "zaak"


class KlantContactInline(EditInlineAdminMixin, admin.TabularInline):
    model = KlantContact
    fields = KlantContactAdmin.list_display
    fk_name = "zaak"


class RolInline(EditInlineAdminMixin, admin.TabularInline):
    model = Rol
    fields = RolAdmin.list_display
    fk_name = "zaak"


class ResultaatInline(EditInlineAdminMixin, admin.TabularInline):
    model = Resultaat
    fields = ResultaatAdmin.list_display
    fk_name = "zaak"


class RelevanteZaakRelatieInline(EditInlineAdminMixin, admin.TabularInline):
    model = RelevanteZaakRelatie
    fields = RelevanteZaakRelatieAdmin.list_display
    fk_name = "zaak"


class ZaakBesluitInline(EditInlineAdminMixin, admin.TabularInline):
    model = ZaakBesluit
    fields = ZaakBesluitAdmin.list_display
    fk_name = "zaak"


@admin.register(Zaak)
class ZaakAdmin(
    AuditTrailAdminMixin, ListObjectActionsAdminMixin, UUIDAdminMixin, admin.ModelAdmin
):
    list_display = (
        "identificatie",
        "registratiedatum",
        "startdatum",
        "einddatum",
        "archiefstatus",
    )
    search_fields = (
        "identificatie",
        "uuid",
        "_zaaktype_url",
        "_zaaktype__identificatie",
    )
    date_hierarchy = "registratiedatum"
    list_filter = ("startdatum", "archiefstatus", "vertrouwelijkheidaanduiding")
    ordering = ("-identificatie", "startdatum")
    inlines = [
        StatusInline,
        ZaakObjectInline,
        ZaakInformatieObjectInline,
        KlantContactInline,
        ZaakEigenschapInline,
        RolInline,
        ResultaatInline,
        RelevanteZaakRelatieInline,
        ZaakBesluitInline,
    ]
    raw_id_fields = ("_zaaktype", "hoofdzaak")
    viewset = "openzaak.components.zaken.api.viewsets.ZaakViewSet"

    def get_object_actions(self, obj):
        return (
            link_to_related_objects(Status, obj),
            link_to_related_objects(Rol, obj),
            link_to_related_objects(ZaakEigenschap, obj),
            link_to_related_objects(Resultaat, obj),
            link_to_related_objects(ZaakObject, obj),
            link_to_related_objects(ZaakInformatieObject, obj),
            link_to_related_objects(KlantContact, obj),
            link_to_related_objects(ZaakBesluit, obj),
            link_to_related_objects(RelevanteZaakRelatie, obj, rel_field_name="zaak"),
        )
