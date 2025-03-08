from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import format_html

from datetime import datetime

class UserManager(BaseUserManager):
    """A new UserManager that uses the email as the username field"""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Keine Email Adresse angegeben.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """Einen Benutzer mit dem gegebenen passwort erstellen."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Adminaccount erstellen."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=False)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Die Telefonnummer muss in folgendem Format eingegeben werden: '+XX123456789' (bis zu 15 Zeichen)")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    owner = models.CharField(max_length=256)
    street = models.CharField(max_length=512)
    number = models.CharField(max_length=16)
    parz = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    plz = models.CharField(max_length=5)

    REQUIRED_FIELDS = []

    objects = UserManager()

class BuildingData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #gebäudedaten

    GEBAEUDEART_CHOICES = (
        ("EINFAMILIENHAUS", _("Einfamilienhaus")),
        ("2FAMILIENHAUS", _("Zweifamilienhaus")),
        ("WOHNGEBAEUDE_3_WOHNEINHEITEN", _("Wohngebäude bis 3 Wohneinheiten")),
        ("FREIE_EINGABE", _("Freie Eingabe (bitte Eintragen)")),
    )

    gebaeudeart = models.CharField(max_length=256, choices=GEBAEUDEART_CHOICES)
    gebaeudeart_freie_eingabe = models.CharField(max_length=256, null=True, blank=True)

    BAUART_CHOICES = (
        ("FREISTEHEND", _("freistehendes Haus")),
        ("ECKHAUS", _("Eckhaus")),
        ("REIHENHAUS", _("Reihenhaus"))
    )

    bauart = models.CharField(max_length=256, choices=BAUART_CHOICES)

    energiebezugsflaeche = models.PositiveIntegerField(default=200, validators=[MinValueValidator(50), MaxValueValidator(600)])
    baujahr = models.PositiveIntegerField(default=1950, validators=[MinValueValidator(1900), MaxValueValidator(2030)])

    #sanierung gebäudehülle
    sanierung_dach = models.IntegerField(validators=[MinValueValidator(1980), MaxValueValidator(2030)], null=True, blank=True)
    sanierung_aussenwaende = models.IntegerField(validators=[MinValueValidator(1980), MaxValueValidator(2030)], null=True, blank=True)
    sanierung_fenster = models.IntegerField(validators=[MinValueValidator(1980), MaxValueValidator(2030)], null=True, blank=True)
    sanierung_kellerdecken = models.IntegerField(validators=[MinValueValidator(1980), MaxValueValidator(2030)], null=True, blank=True)
    sanierung_anderes = models.IntegerField(validators=[MinValueValidator(1980), MaxValueValidator(2030)], null=True, blank=True)

    sanierung_anderes_erklaerung = models.CharField(max_length=1000, null=True, blank=True)

    #wärmeerzeugung und abgabe
    baujahr_gebaeudeheizung = models.IntegerField(default=-1, validators=[MinValueValidator(1980), MaxValueValidator(2030)])
    baujahr_warmwasseraufbereitung = models.IntegerField(default=-1, validators=[MinValueValidator(1980), MaxValueValidator(2030)])

    HEIZUNG_CHOICES = (
        ("HEIZOEL", _("Heizöl")),
        ("GAS", _("Gas")),
        ("HOLZ", _("Holz")),
        ("STROM", _("Strom")),
        ("FLUESSIGGAS", _("Flüssiggas")),
        ("SONNE", _("Sonne")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    HEIZUNG_OTHER_CHOICES = (
        ("NONE", _("keine")),
        ("HEIZOEL", _("Heizöl")),
        ("GAS", _("Gas")),
        ("HOLZ", _("Holz")),
        ("STROM", _("Strom")),
        ("FLUESSIGGAS", _("Flüssiggas")),
        ("SONNE", _("Sonne")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    heizwaerme_erzeugung_1 = models.CharField(max_length=32,default="HEIZOEL", choices = HEIZUNG_CHOICES)
    heizwaerme_erzeugung_1_sonstiges = models.CharField(max_length=128,null=True, blank=True)
    heizwaerme_erzeugung_2 = models.CharField(max_length=32,default="NONE", null=True, blank=True, choices = HEIZUNG_OTHER_CHOICES)
    heizwaerme_erzeugung_2_sonstiges = models.CharField(max_length=128,null=True, blank=True)
    heizwaerme_erzeugung_3 = models.CharField(max_length=32,default="NONE", null=True, blank=True, choices = HEIZUNG_OTHER_CHOICES)
    heizwaerme_erzeugung_3_sonstiges = models.CharField(max_length=128,null=True, blank=True)

    warmwasseraufbereitung_1 = models.CharField(max_length=32,default="HEIZOEL", choices = HEIZUNG_CHOICES)
    warmwasseraufbereitung_1_sonstiges = models.CharField(max_length=128,null=True, blank=True)
    warmwasseraufbereitung_2 = models.CharField(max_length=32,default="NONE", null=True, blank=True, choices = HEIZUNG_OTHER_CHOICES)
    warmwasseraufbereitung_2_sonstiges = models.CharField(max_length=128,null=True, blank=True)
    warmwasseraufbereitung_3 = models.CharField(max_length=32,default="NONE", null=True, blank=True, choices = HEIZUNG_OTHER_CHOICES)
    warmwasseraufbereitung_3_sonstiges = models.CharField(max_length=128,null=True, blank=True)

    leistung_waermeerzeuger = models.PositiveIntegerField(default=20, validators=[MinValueValidator(0), MaxValueValidator(50)])

    WAERMEABGABE_CHOICES = (
        ("HEIZKOERPER", _("Heizkörper")),
        ("FUSSBODENHEIZUNG", _("Fußbodenheizung")),
        ("FUSSBODENHEIZUNG_HEIZKOERPER", _("Heizkörper & Fußbodenheizung")),
        ("SONST_FLAECHENHEIZUNG", _("sonstige Flächenheizung")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    waermeabgabe = models.CharField(max_length=32,default="HEIZKOERPER", choices = WAERMEABGABE_CHOICES)
    waermeabgabe_sonstiges = models.CharField(max_length=128, null=True, blank=True)

    REGELUNG_WAERMEABGABE_CHOICES = (#Thermostatventile, manuelle Ventile, Stellantriebe, Stellantriebe mit Raumtemperaturregelung, sonstiges
        ("THERMOSTATVENTILE", _("Thermostatventile")),
        ("MANUELLE_VENTILE", _("manuelle Ventile")),
        ("THERMOSTAT_MANUELLE_VENTILE", _("Thermostatventile & manuelle Ventile")),
        ("STELLANTRIEBE", _("Stellantriebe")),
        ("STELLANTRIEBE_RAUMTEMP_REGELUNG", _("Stellantriebe mit Raumtemperaturregelung")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    regelung_waermeabgabe = models.CharField(max_length=32,default="THERMOSTATVENTILE", choices = REGELUNG_WAERMEABGABE_CHOICES)
    regelung_waermeabgabe_sonstiges = models.CharField(max_length=128, null=True, blank=True)

    #brauchwarmwasser

    BRAUCHWARMWASSER_CHOICES = (
        ("JA", _("Ja (vorhanden)")),
        ("NEIN", _("Nein (nicht vorhanden)")),
        ("NICHT_BEKANNT", _("nicht bekannt")),
    )

    brauchwarmwasserzirkulation = models.CharField(choices = BRAUCHWARMWASSER_CHOICES, max_length=32,default="NICHT_BEKANNT")
    brauchwarmwasser_speicher_inhalt = models.PositiveIntegerField(validators=[MinValueValidator(20), MaxValueValidator(500)], null=True, blank=True)

    #eigenstromproduktion

    ART_EIGENSTROM_CHOICES = (
        ("KEINE", _("keine")),
        ("PV", _("Photovoltaik")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    art_eigenstromanlage = models.CharField(choices = ART_EIGENSTROM_CHOICES, max_length=64,default="NONE")
    art_eigenstromanlage_sonstiges = models.CharField(max_length=128,null=True, blank=True)
    peak_leistung_eigenstromanlage = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(50.0)], null=True, blank=True)

    kapazitaet_batteriespeicher = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)], null=True, blank=True)

    #geplante investitionen
    investition_waermeerzeugung = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)], null=True, blank=True)
    investition_warmwasseraufbereitung = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)], null=True, blank=True)
    investition_eigenstromproduktion_batteriespeicher = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200000)], null=True, blank=True)
    investition_sanierung_gebaeudehuelle = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500000)], null=True, blank=True)
    investition_andere = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500000)], null=True, blank=True)

    class Meta:
        verbose_name = 'Gebäudedaten ohne Energie'
        verbose_name_plural = 'Gebäudedaten ohne Energie'


class EnergyByYear(models.Model):
    #User ist ein foreign Key, bedeutet dass ein Nutzer mehrere dieser Objekte haben kann
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    jahr = models.IntegerField(validators=[MinValueValidator(2018), MaxValueValidator(2030)])

    #Bedarf

    bedarf_heizoel = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    bedarf_gas = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200000)], blank=True, null=True)
    bedarf_strom = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(100000)])

    bedarf_holz = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    bedarf_holz_hackschnitzel = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20000.0)], blank=True, null=True)
    bedarf_holzpellets = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)

    bedarf_fernwärme_heizstrom = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)], blank=True, null=True)

    #Kosten
    kosten_heizoel = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    kosten_gas = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    kosten_strom = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    kosten_holz = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    kosten_fernwärme = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)
    kosten_andere = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20000)], blank=True, null=True)

    #Eigenstromproduktion
    eigenstrom_jahresertrag = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50000)], blank=True, null=True)
    eigenstrom_netzeinspeisung = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50000)], blank=True, null=True)
    eigenstrom_netzeinspeisung_ertrag = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'jahr'], 
                name='unique year per user'
            )
        ]
        verbose_name = 'Energiedaten nach Jahr'
        verbose_name_plural = 'Energiedaten nach Jahr'

#ResultCache speichert die GEK Werte bei jeder Berechnung für den Nutzer ab. Damit kann dann ein Diagramm zur Vergleich der eigenen GEK Werte mit den der anderen
# Nutzer aufgestellt werden.
class ResultCache(models.Model):
    #User ist ein foreign Key, bedeutet dass ein Nutzer mehrere dieser Objekte haben kann
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jahr = models.IntegerField(validators=[MinValueValidator(2018), MaxValueValidator(2030)])

    gek_strom = models.FloatField()
    gek_strom_kosten = models.FloatField()
    gek_waerme = models.FloatField()
    gek_waerme_kosten = models.FloatField()
    gek_total = models.FloatField()
    gek_total_kosten = models.FloatField()

    bauart = models.CharField(max_length=256)

    ebf = models.IntegerField()

    def account_actions(self, obj):
        return format_html(u'<a href="#" onclick="return false;" class="button" '
                           u'id="id_admin_unit_selected">Unit Details</a>')
    account_actions.short_description = 'Account Actions'
    account_actions.allow_tags = True

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'jahr'], 
                name='unique resultcache per user and year'
            )
        ]
        verbose_name = 'Zwischenspeicher zum Datenvergleich'
        verbose_name_plural = 'Zwischenspeicher zum Datenvergleich'


