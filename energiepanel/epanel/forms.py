from django import forms
from django.contrib.auth.forms import UserCreationForm
from epanel.models import User, BuildingData, EnergyByYear

from django.utils.translation import gettext as _

from datetime import datetime

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=200,label = "Benutzername")
    email = forms.EmailField(max_length=200,label = "E-Mail Adresse", help_text='Diese E-Mail Adresse wird zum erneuten Anmelden verwendet.')
    last_name = forms.CharField(label = "Name", required=True)
    first_name = forms.CharField(label = "Vorname(n)", required=True)

    phone_number = forms.CharField(label = "Telefonnummer", required=True , help_text='Die Telefonnummer muss im Format +XX123456789 eingegeben werden (XX = Ländercode)')

    password1 = forms.CharField(label = "Passwort" , widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label = "Passwort wiederholen" , widget=forms.PasswordInput, required=True)
    password2.after = "Gebäudedaten"
    
    owner = forms.CharField(label = "Eigentümer", required=True)
    street = forms.CharField(label = "Straße", required=True)
    number = forms.CharField(label = "Nummer", required=True)
    parz = forms.CharField(label = "Parzelle", required=True, help_text='https://www.geoportal.rlp.de/ siehe meistgenutzte Karten | Liegenschaften RP')
    city = forms.CharField(label = "Ort", required=True)
    plz = forms.CharField(label = "PLZ", required=True)

    acceptterms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Bestätigung",
                      choices=[("accept","Eigentümer stimmt zu, dass Daten anonymisiert für die Kommunikation der Projekterfolge veröffentlicht werden dürfen.")] , required=True)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'phone_number', 'email', 'password1', 'password2', 'owner' , 'street' , 'number' , 'parz', 'city', 'plz')

class BuildingDataForm(forms.ModelForm):
    #gebäudedaten
    GEBAEUDEART_CHOICES = (
        ("EINFAMILIENHAUS", _("Einfamilienhaus")),
        ("2FAMILIENHAUS", _("Zweifamilienhaus")),
        ("WOHNGEBAEUDE_3_WOHNEINHEITEN", _("Wohngebäude bis 3 Wohneinheiten")),
        ("FREIE_EINGABE", _("Freie Eingabe (bitte unten Eintragen)")),
    )
    gebaeudeart = forms.ChoiceField(choices = GEBAEUDEART_CHOICES, label="Gebäudeart", initial='', widget=forms.Select(attrs={'show-id':'div_id_gebaeudeart_freie_eingabe','show-on':'3'}), required=True)
    gebaeudeart_freie_eingabe = forms.CharField(label = "Freie Eingabe", required=False, help_text='Bitte Ausfüllen wenn \"Freie Auswahl\" bei Gebäudeart gewahlt wurde.')

    BAUART_CHOICES = (
        ("FREISTEHEND", _("freistehendes Haus")),
        ("ECKHAUS", _("Eckhaus")),
        ("REIHENHAUS", _("Reihenhaus"))
    )
    bauart = forms.ChoiceField(choices = BAUART_CHOICES, label="Bauart", initial='', required=True)

    energiebezugsflaeche = forms.IntegerField(label = "Energiebezugsfläche (m²)", required = True, help_text='Eine Anleitung zur Berechnung der Energiebezugsfläche finden sie hier. https://www.energiepaket-bl.ch/assets/content/files/Definition_Energiebezugsflaeche.pdf')

    baujahr = forms.IntegerField(label = "Baujahr Gebäude", required = True)
    baujahr.after = "Sanierung der Gebäudehülle"
    baujahr.after_id = "sanierung"

    #sanierung gebäudehülle
    sanierung_dach = forms.IntegerField(label = "Sanierung des Dachs", required = False, help_text='Geben sie das Jahr ein, bei denen die Wärmedämmung der Gebäudehülle verbessert wurde. Wurde nichts gemacht lassen sie die Felder bitte leer.')
    sanierung_aussenwaende = forms.IntegerField(label = "Sanierung der Aussenwände", required = False, help_text='Wenn das Dach oder der Dachboden nachträglich wärmegedämmt wurde, geben sie das Jahr der Sanierung an.')
    sanierung_fenster = forms.IntegerField(label = "Sanierung der Fenster", required = False, help_text='Wenn die Fenster nachträglich saniert wurden, geben Sie das Jahr der Sanierung an')
    sanierung_kellerdecken = forms.IntegerField(label = "Sanierung der Kellerdecken", required = False, help_text='Wenn die Kellerdecken nachträglich saniert wurden, geben Sie das Jahr der Sanierung an.')
    sanierung_anderes = forms.IntegerField(label = "Andere Sanierungsarbeiten", required = False, help_text='Geben sie das Jahr der anderen Sanierungsarbeiten an.')

    sanierung_anderes_erklaerung = forms.CharField(label = "Andere Sanierungsarbeiten (Erklärung)", required=False, help_text='Bitte Ausfüllen sollten andere Sanierungsarbeiten erfolgt sein.')
    sanierung_anderes_erklaerung.after = "Wärmeerzeugung und Abgabe"
    sanierung_anderes_erklaerung.after_id = "waerrmeerzeugung"

    #wärmeerzeugung und abgabe
    baujahr_gebaeudeheizung = forms.IntegerField(label = "Baujahr der Gebäudeheizung", required = True)
    baujahr_warmwasseraufbereitung = forms.IntegerField(label = "Baujahr der Warmwasseraufbereitung", required = True)

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

    heizwaerme_erzeugung_1 = forms.ChoiceField(choices = HEIZUNG_CHOICES, label="Art der Heizwärmeerzeugung 1. Priorität", initial='', widget=forms.Select(attrs={'show-id':'div_id_heizwaerme_erzeugung_1_sonstiges','show-on':'6'}), required=True, help_text='Bitte geben sie hier an, wie der größte Teil der Heizwärme erzeugt wird.')
    heizwaerme_erzeugung_1_sonstiges = forms.CharField(label = "Heizwärmeerzeugung 1. Priorität (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Heizwärmeerzeugung \"Sonstiges\" gewählt wurde.')

    heizwaerme_erzeugung_2 = forms.ChoiceField(choices = HEIZUNG_OTHER_CHOICES, label="Art der Heizwärmeerzeugung 2. Priorität", initial='', widget=forms.Select(attrs={'show-id':'div_id_heizwaerme_erzeugung_2_sonstiges','show-on':'7'}), required=False, help_text='Wenn sie die Heizwärme noch auf eine weitere Art erzeugen geben sie dies bitte hier an.')
    heizwaerme_erzeugung_2.open_collapse = True
    heizwaerme_erzeugung_2.collapse_title = "Art der Heizwärmeerzeugung 2. Priorität"
    heizwaerme_erzeugung_2.collapse_id = "collapse1"
    heizwaerme_erzeugung_2_sonstiges = forms.CharField(label = "Heizwärmeerzeugung 2. Priorität (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Heizwärmeerzeugung \"Sonstiges\" gewählt wurde.')
    heizwaerme_erzeugung_2_sonstiges.close_collapse = True

    heizwaerme_erzeugung_3 = forms.ChoiceField(choices = HEIZUNG_OTHER_CHOICES, label="Art der Heizwärmeerzeugung 3. Priorität", initial='', widget=forms.Select(attrs={'show-id':'div_id_heizwaerme_erzeugung_3_sonstiges','show-on':'7'}), required=False)
    heizwaerme_erzeugung_3.open_collapse = True
    heizwaerme_erzeugung_3.collapse_title = "Art der Heizwärmeerzeugung 3. Priorität"
    heizwaerme_erzeugung_3.collapse_id = "collapse2"
    heizwaerme_erzeugung_3_sonstiges = forms.CharField(label = "Heizwärmeerzeugung 3. Priorität (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Heizwärmeerzeugung \"Sonstiges\" gewählt wurde.')
    heizwaerme_erzeugung_3_sonstiges.close_collapse = True

    warmwasseraufbereitung_1 = forms.ChoiceField(choices = HEIZUNG_CHOICES, label="Art der Warmwasseraufbereitung 1. Priorität", initial='', widget=forms.Select(attrs={'show-id':'div_id_warmwasseraufbereitung_1_sonstiges','show-on':'6'}), required=True)
    warmwasseraufbereitung_1_sonstiges = forms.CharField(label = "Warmwasseraufbereitung 1. Priorität (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Warmwasseraufbereitung \"Sonstiges\" gewählt wurde.')

    warmwasseraufbereitung_2 = forms.ChoiceField(choices = HEIZUNG_OTHER_CHOICES, label="Art der Warmwasseraufbereitung 2. Priorität", initial='',widget=forms.Select(attrs={'show-id':'div_id_warmwasseraufbereitung_2_sonstiges','show-on':'7'}), required=False)
    warmwasseraufbereitung_2.open_collapse = True
    warmwasseraufbereitung_2.collapse_title = "Art der Warmwasseraufbereitung 2. Priorität"
    warmwasseraufbereitung_2.collapse_id = "collapse3"
    warmwasseraufbereitung_2_sonstiges = forms.CharField(label = "Warmwasseraufbereitung 2. Priorität (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Warmwasseraufbereitung \"Sonstiges\" gewählt wurde.')
    warmwasseraufbereitung_2_sonstiges.close_collapse = True

    warmwasseraufbereitung_3 = forms.ChoiceField(choices = HEIZUNG_OTHER_CHOICES, label="Art der Warmwasseraufbereitung 3. Priorität", initial='',widget=forms.Select(attrs={'show-id':'div_id_warmwasseraufbereitung_3_sonstiges','show-on':'7'}), required=False)
    warmwasseraufbereitung_3.open_collapse = True
    warmwasseraufbereitung_3.collapse_title = "Art der Warmwasseraufbereitung 3. Priorität"
    warmwasseraufbereitung_3.collapse_id = "collapse4"
    warmwasseraufbereitung_3_sonstiges = forms.CharField(label = "Warmwasseraufbereitung 3. Priorität (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Warmwasseraufbereitung \"Sonstiges\" gewählt wurde.')
    warmwasseraufbereitung_3_sonstiges.close_collapse = True

    leistung_waermeerzeuger = forms.IntegerField(label = "Leistung des Wärmeerzeugers (kW)", required = True)

    WAERMEABGABE_CHOICES = (
        ("HEIZKOERPER", _("Heizkörper")),
        ("FUSSBODENHEIZUNG", _("Fußbodenheizung")),
        ("FUSSBODENHEIZUNG_HEIZKOERPER", _("Heizkörper & Fußbodenheizung")),
        ("SONST_FLAECHENHEIZUNG", _("sonstige Flächenheizung")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    waermeabgabe = forms.ChoiceField(choices = WAERMEABGABE_CHOICES, label="Wärmeabgabe", initial='', widget=forms.Select(attrs={'show-id':'div_id_waermeabgabe_sonstiges','show-on':'3'}), required=True)
    waermeabgabe_sonstiges = forms.CharField(label = "Wärmeabgabe (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei Wärmeabgabe \"Sonstiges\" gewählt wurde.')

    REGELUNG_WAERMEABGABE_CHOICES = (#Thermostatventile, manuelle Ventile, Stellantriebe, Stellantriebe mit Raumtemperaturregelung, sonstiges
        ("THERMOSTATVENTILE", _("Thermostatventile")),
        ("MANUELLE_VENTILE", _("manuelle Ventile")),
        ("THERMOSTAT_MANUELLE_VENTILE", _("Thermostatventile & manuelle Ventile")),
        ("STELLANTRIEBE", _("Stellantriebe")),
        ("STELLANTRIEBE_RAUMTEMP_REGELUNG", _("Stellantriebe mit Raumtemperaturregelung")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    regelung_waermeabgabe = forms.ChoiceField(choices = REGELUNG_WAERMEABGABE_CHOICES, label="Regelung Wärmeabgabe", initial='', widget=forms.Select(attrs={'show-id':'div_id_regelung_waermeabgabe_sonstiges','show-on':'4'}), required=True)
    regelung_waermeabgabe_sonstiges = forms.CharField(label = "Regelung Wärmeabgabe (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei \"Regelung Wärmeabgabe\" \"Sonstiges\" gewählt wurde.')
    regelung_waermeabgabe_sonstiges.after = "Brauchwarmwasser"
    regelung_waermeabgabe_sonstiges.after_id = "brauchwarmwasser"

    #brauchwarmwasser

    BRAUCHWARMWASSER_CHOICES = (
        ("JA", _("Ja (vorhanden)")),
        ("NEIN", _("Nein (nicht vorhanden)")),
        ("NICHT_BEKANNT", _("nicht bekannt")),
    )

    brauchwarmwasserzirkulation = forms.ChoiceField(choices = BRAUCHWARMWASSER_CHOICES, label="Brauchwarmwasserzirkulation", initial='NICHT_BEKANNT', widget=forms.Select(), required=True
        , help_text='Um an der Zapfstelle möglichst schnell Brauchwarmwasser zu bekommen, ist oft eine Brauchwarmwasserzirkulationspumpe installiert. Dies pumpt das Brauchwarmwasser vom Warmwassererzeuger zur Zapfstelle und zurück. Prüfen Sie, ob eine solche Pumpe vorhanden ist. Wenn Sie sich nicht sicher sind, wählen sie "nicht bekannt".')
    brauchwarmwasser_speicher_inhalt = forms.IntegerField(label = "Inhalt des Brauchwarmwasserspeichers (Liter)", required = False, help_text="Sollte keine Brauchwarmwasserzirkulation vorhanden sein oder der Speicherinhalt nicht bekannt sein kann dieses Feld freigelassen werden.")
    brauchwarmwasser_speicher_inhalt.after = "Eigenstromproduktion"
    brauchwarmwasser_speicher_inhalt.after_id = "eigenstromproduktion"

    #eigenstromproduktion

    ART_EIGENSTROM_CHOICES = (
        ("KEINE", _("keine")),
        ("PV", _("Photovoltaik")),
        ("SONSTIGES", _("Sonstiges (bitte angeben)")),
    )

    art_eigenstromanlage = forms.ChoiceField(choices = ART_EIGENSTROM_CHOICES, label="Art der Eigenstromanlage", initial='',widget=forms.Select(attrs={'show-id':'div_id_art_eigenstromanlage_sonstiges','show-on':'2'}), required=True)
    art_eigenstromanlage_sonstiges = forms.CharField(label = "Art der Eigenstromanlage (Sonstiges)", required=False, help_text='Bitte Ausfüllen wenn bei \"Art der Eigenstromanlage\" \"Sonstiges\" gewählt wurde.')

    peak_leistung_eigenstromanlage = forms.FloatField(label="Peak Leistung der Eigenstromanlage (kWp)", required=False, max_value=50, min_value=0.5, widget=forms.NumberInput(attrs={'step': "0.01"}), help_text='Wenn nicht bekannt oder nicht vorhanden Feld bitte frei lassen.') 

    kapazitaet_batteriespeicher = forms.FloatField(label = "Kapazität Batteriespeicher in kWh", required = False, help_text="Wenn nicht bekannt oder nicht vorhanden Feld bitte frei lassen.")
    kapazitaet_batteriespeicher.after = "Geplante Investitionen in den nächsten 10 Jahren in €"
    kapazitaet_batteriespeicher.after_id = "investitionen"

    #geplante investitionen
    investition_waermeerzeugung = forms.IntegerField(label = "In neue Wärmeerzeugung", required = False, help_text="Wenn nicht nicht vorhanden Feld bitte frei lassen.")
    investition_warmwasseraufbereitung = forms.IntegerField(label = "In neue Warmwasseraufbereitung", required = False, help_text="Wenn nicht nicht vorhanden Feld bitte frei lassen.")
    investition_eigenstromproduktion_batteriespeicher = forms.IntegerField(label = "In Eigenstromproduktion, Batteriespeicher", required = False, help_text="Wenn nicht nicht vorhanden Feld bitte frei lassen.")
    investition_sanierung_gebaeudehuelle = forms.IntegerField(label = "In Sanierung der Gebäudehülle", required = False, help_text="Wenn nicht nicht vorhanden Feld bitte frei lassen.")
    investition_andere = forms.IntegerField(label = "andere", required = False, help_text="Wenn nicht nicht vorhanden Feld bitte frei lassen.")

    class Meta:
        model = BuildingData
        fields = ('gebaeudeart', 'gebaeudeart_freie_eingabe', 'bauart', 'energiebezugsflaeche', 'baujahr', 'sanierung_dach'
        , 'sanierung_aussenwaende', 'sanierung_fenster', 'sanierung_kellerdecken' , 'sanierung_anderes' , 'sanierung_anderes_erklaerung'
        , 'baujahr_gebaeudeheizung', 'baujahr_warmwasseraufbereitung', 'heizwaerme_erzeugung_1' , 'heizwaerme_erzeugung_1_sonstiges'
        , 'heizwaerme_erzeugung_2', 'heizwaerme_erzeugung_2_sonstiges', 'heizwaerme_erzeugung_3' , 'heizwaerme_erzeugung_3_sonstiges'
        , 'warmwasseraufbereitung_1', 'warmwasseraufbereitung_1_sonstiges', 'warmwasseraufbereitung_2' , 'warmwasseraufbereitung_2_sonstiges'
        , 'warmwasseraufbereitung_3', 'warmwasseraufbereitung_3_sonstiges', 'leistung_waermeerzeuger' , 'waermeabgabe'
        , 'waermeabgabe_sonstiges', 'regelung_waermeabgabe', 'regelung_waermeabgabe_sonstiges' , 'brauchwarmwasserzirkulation'
        , 'brauchwarmwasser_speicher_inhalt', 'art_eigenstromanlage', 'art_eigenstromanlage_sonstiges' , 'peak_leistung_eigenstromanlage'
        , 'kapazitaet_batteriespeicher', 'investition_waermeerzeugung', 'investition_warmwasseraufbereitung' , 'investition_eigenstromproduktion_batteriespeicher'
        , 'investition_sanierung_gebaeudehuelle', 'investition_andere')

class EnergyDataForm(forms.ModelForm):

    YEAR_CHOICES = (
        (datetime.today().year-3, str(datetime.today().year-3)),
        (datetime.today().year-2, str(datetime.today().year-2)),
        (datetime.today().year-1, str(datetime.today().year-1)),
        (datetime.today().year, str(datetime.today().year) + " (Erfolgskontrolle)"),
        (datetime.today().year+1, str(datetime.today().year+1) + " (Erfolgskontrolle)"),
        (datetime.today().year+2, str(datetime.today().year+2) + " (Erfolgskontrolle)"),
    )

    jahr = forms.ChoiceField(choices = YEAR_CHOICES, label="Jahr", required=True)

    acceptoverwrite = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="",
                      choices=[("accept","Ich habe bereits Daten für dieses Jahr eingereicht und möchte diese überschreiben.")] , required=False)

    acceptoverwrite.after = "Endenergiebedarf"

    #Endenergiebedarf

    bedarf_heizoel = forms.IntegerField(label = "Heizöl (Liter)", required = False, help_text="Diese Daten erhalten sie von ihrem Öllieferanten. Wenn nicht nicht vorhanden Feld bitte frei lassen.")
    bedarf_gas = forms.IntegerField(label = "Gas (kWh)", required = False, help_text="Diese Daten erhalten sie von ihrem Gaslieferanten. Wenn nicht nicht vorhanden Feld bitte frei lassen.")
    bedarf_strom = forms.IntegerField(label = "Strom (kWh)", required = True, help_text="Diese Daten erhalten sie von ihrem Stromlieferanten. Wenn nicht nicht vorhanden Feld bitte frei lassen. Eigenstrom kWh und Erlöse nicht verrechnen!")

    bedarf_holz = forms.FloatField(label = "Holz als Stückholz in Raummeter (Ster)", required = False)
    bedarf_holz_hackschnitzel = forms.IntegerField(label = "Holz als Hackschnitzel in Schüttraummeter (Srm)", required = False)
    bedarf_holzpellets = forms.IntegerField(label = "Holzpellets in kg", required = False)

    bedarf_fernwärme_heizstrom = forms.IntegerField(label = "Fernwärme oder Heiz-Strom in kWh", required = False)
    bedarf_fernwärme_heizstrom.after = "Endenergiekosten"

    #Endenergiekosten
    kosten_heizoel = forms.IntegerField(label = "Heizöl (€)", required = False, help_text="Diese Daten erhalten sie von ihrem Öllieferanten.")
    kosten_gas = forms.IntegerField(label = "Gas (€)", required = False, help_text="Diese Daten erhalten sie von ihrem Gaslieferanten.")
    kosten_strom = forms.IntegerField(label = "Strom (€)", required = False, help_text="Diese Daten erhalten sie von ihrem Stromlieferanten.")
    kosten_holz = forms.IntegerField(label = "Holz, alle Arten(€)", required = False)
    kosten_fernwärme = forms.IntegerField(label = "Fernwärme (€)", required = False)
    kosten_andere = forms.IntegerField(label = "Andere (€)", required = False)
    kosten_andere.after = "Eigenstromproduktion"

    #Eigenstromproduktion

    eigenstrom_jahresertrag = forms.IntegerField(label = "Jahresertrag in kWh", required = False)
    eigenstrom_jahresertrag.pv = True

    eigenstrom_netzeinspeisung = forms.IntegerField(label = "Netzeinspeisung in kWh", required = False)
    eigenstrom_netzeinspeisung.pv = True

    eigenstrom_netzeinspeisung_ertrag = forms.IntegerField(label = "Netzeinspeisung in € pro Jahr", required = False) 
    eigenstrom_netzeinspeisung_ertrag.pv = True

    eigenstrom_netzeinspeisung_ertrag.after = "Abschicken"  


    class Meta:
        model = EnergyByYear
        fields = ('jahr','acceptoverwrite','bedarf_heizoel','bedarf_gas','bedarf_strom','bedarf_holz','bedarf_holz_hackschnitzel','bedarf_holzpellets','bedarf_fernwärme_heizstrom',
            'kosten_heizoel','kosten_gas','kosten_strom','kosten_holz','kosten_fernwärme','kosten_andere','eigenstrom_jahresertrag','eigenstrom_netzeinspeisung','eigenstrom_netzeinspeisung_ertrag')