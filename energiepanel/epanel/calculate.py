import collections
from datetime import datetime

from constance import config

from epanel.models import User, BuildingData, EnergyByYear,ResultCache
from epanel.svg_drawing import drawGEKDiagram, drawGEKStromDiagram, drawGEKWaermeDiagram
from epanel.gek_comp_plot import generateComparisonPlot

from django.contrib.staticfiles.storage import staticfiles_storage

import cairosvg 
import io, os
from PIL import Image
from datetime import datetime

from fpdf import FPDF, HTMLMixin

class PDF(FPDF, HTMLMixin):
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select helvetica italic 8
        self.set_font('helvetica', 'I', 8)
        # Print current and total page numbers
        self.cell(0, 10, f"Stand: {datetime.now().strftime('%d.%m.%Y %H:%M')}  Seite {str(self.page_no()) + '/{nb}'}", 0, 0, 'R')
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.text(20, 15, 'GEK Bericht')
        self.set_font('helvetica', size=12)
        self.text(130, 10, '1000 klimaneutrale Gebäude')
        self.image("epanel/"+staticfiles_storage.url("epanel/logoall.jpg"), x=130,y=11 , w=60)
        # Line break
        self.ln(20)

translate_dict = {"HEIZKOERPER" : "Heizkörper", "FUSSBODENHEIZUNG" : "Fußbodenheizung", "SONST_FLAECHENHEIZUNG" : "sonstige Flächenheizung" , "SONSTIGES" : "Sonstiges",
                "NONE" : "keine", "HEIZOEL" : "Heizöl" , "GAS" : "Gas" , "HOLZ" : "Holz" , "STROM" : "Strom" , "FLUESSIGGAS" : "Flüssiggas" , "SONNE" : "Sonne",
                "EINFAMILIENHAUS" : "Einfamilienhaus", "2FAMILIENHAUS" : "Zweifamilienhaus" , "WOHNGEBAEUDE_3_WOHNEINHEITEN" : "Wohngebäude bis 3 Wohneinheiten",
                "JA" : "Ja", "NEIN" : "Nein", "NICHT_BEKANNT" : "nicht bekannt", "KEINE" : "keine", "PV" : "Photovoltaik",
                "THERMOSTATVENTILE" : "Thermostatventile", "MANUELLE_VENTILE" : "manuelle Ventile", "STELLANTRIEBE" : "Stellantriebe",
                "STELLANTRIEBE_RAUMTEMP_REGELUNG" : "Stellantriebe mit Raumtemperaturregelung",
                "FREISTEHEND" : "Freistehend", "ECKHAUS" : "Eckhaus", "REIHENHAUS" : "Reihenhaus", "FUSSBODENHEIZUNG_HEIZKOERPER" : "Fußbodenheizung & Heizkörper", "THERMOSTAT_MANUELLE_VENTILE" : "Thermostat & manuelle Ventile"} 
def translate(st):
    if st in translate_dict:
        return translate_dict[st]
    return st

def createPDF(user):

    #start calculation of data from user

    buildingData = BuildingData.objects.get(user = user)
    #error handling
    if buildingData is None: return {"error" : "0"}

    energiebezugsflaeche = buildingData.energiebezugsflaeche

    yearData = EnergyByYear.objects.filter(user = user)

    gebaeudeart = translate(buildingData.gebaeudeart)
    if gebaeudeart == "FREIE_EINGABE": gebaeudeart = buildingData.gebaeudeart_freie_eingabe

    heizwarme = translate(buildingData.heizwaerme_erzeugung_1)
    if (heizwarme == "SONSTIGES"): heizwarme = buildingData.heizwaerme_erzeugung_1_sonstiges
    if buildingData.heizwaerme_erzeugung_2 != "NONE":
        if (buildingData.heizwaerme_erzeugung_2 == "SONSTIGES"): heizwarme += ", " + buildingData.heizwaerme_erzeugung_2_sonstiges
        else: heizwarme += ", " + translate(buildingData.heizwaerme_erzeugung_2)
    if buildingData.heizwaerme_erzeugung_3 != "NONE":
        if (buildingData.heizwaerme_erzeugung_3 == "SONSTIGES"): heizwarme += ", " + buildingData.heizwaerme_erzeugung_3_sonstiges
        else: heizwarme += ", " + translate(buildingData.heizwaerme_erzeugung_3)

    warmwasser = translate(buildingData.warmwasseraufbereitung_1)
    if (warmwasser == "SONSTIGES"): warmwasser = buildingData.warmwasseraufbereitung_1_sonstiges
    if buildingData.warmwasseraufbereitung_2 != "NONE":
        if (buildingData.warmwasseraufbereitung_2 == "SONSTIGES"): warmwasser += ", " + buildingData.warmwasseraufbereitung_2_sonstiges
        else: warmwasser += ", " + translate(buildingData.warmwasseraufbereitung_2)
    if buildingData.warmwasseraufbereitung_3 != "NONE":
        if (buildingData.warmwasseraufbereitung_3 == "SONSTIGES"): warmwasser += ", " + buildingData.warmwasseraufbereitung_3_sonstiges
        else: warmwasser += ", " + translate(buildingData.warmwasseraufbereitung_3)

    pv = "keine Eigenstromproduktion"
    if (buildingData.art_eigenstromanlage != "KEINE"):
        if (buildingData.art_eigenstromanlage == "PV"): pv = "PV-Anlage vorhanden"
        else: pv = "Eigenstrom: " + buildingData.art_eigenstromanlage_sonstiges

    basedata = {"gebaeudeart": gebaeudeart
        , "baujahr" : buildingData.baujahr
        , "street" : user.street
        , "number" : user.number
        , "plz" : user.plz
        , "city" : user.city
        , "owner" : user.owner
        , "energiebezugsflaeche" : buildingData.energiebezugsflaeche
        , "heizwaerme" : heizwarme
        , "warmwasser" : warmwasser
        , "pv" : pv
    }

    gek_total, data_per_year = calculateGEKTotal(yearData, energiebezugsflaeche)
    svg_total = drawGEKDiagram(basedata, gek_total, data_per_year)

    gek_waerme, data_per_year_waerme = calculateGEKWaerme(yearData, energiebezugsflaeche)
    svg_waerme = drawGEKWaermeDiagram(basedata, gek_waerme, data_per_year_waerme)

    gek_strom, data_per_year_strom = calculateGEKStrom(yearData, energiebezugsflaeche)
    svg_strom = drawGEKStromDiagram(basedata, gek_strom, data_per_year_strom)

    plot1 = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, export_image = True)
    plot1_total = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, export_image = True , doplot=1)
    plot1_waerme = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, export_image = True , doplot=2)
    plot1_strom = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, export_image = True , doplot=3)

    plot2 = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, export_image = True)
    plot2_total = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, export_image = True, doplot=1)
    plot2_waerme = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, export_image = True, doplot=2)
    plot2_strom = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, export_image = True, doplot=3)

    document = PDF(format="A4" , unit="mm")
    document.set_left_margin(20)
    document.set_right_margin(20)
    document.add_page()

    #Convert SVG to PNGs
    f = io.BytesIO(cairosvg.svg2png(bytestring = svg_total, scale=2.5))
    f.seek(0)
    document.image(f, x=20,y=30 , w=170)

    document.add_page()
    f = io.BytesIO(cairosvg.svg2png(bytestring = svg_waerme, scale=2.5))
    f.seek(0)
    document.image(f, x=20,y=30 , w=170)

    document.add_page()
    f = io.BytesIO(cairosvg.svg2png(bytestring = svg_strom, scale=2.5))
    f.seek(0)
    document.image(f, x=20,y=30 , w=170)

    document.add_page()
    document.set_font('helvetica', 'B', 16)
    document.text(20, 30, 'GEK Vergleich mit anderen Gebäuden')
    document.ln(document.font_size * 1.5)
    document.image(plot1, x=20,y=45 , w=150)
    document.image(plot1_total, x=20,y=155 , w=150)

    document.add_page()
    document.set_font('helvetica', 'B', 16)
    document.text(20, 30, 'GEK Vergleich mit anderen Gebäuden')
    document.ln(document.font_size * 1.5)
    document.image(plot1_waerme, x=20,y=45 , w=150)
    document.image(plot1_strom, x=20,y=155 , w=150)

    document.add_page()
    document.set_font('helvetica', 'B', 16)
    document.text(20, 30, 'GEK Vergleich mit anderen Gebäuden (Prognose)')
    document.ln(document.font_size * 1.5)
    document.image(plot2, x=20,y=65 , w=150)
    document.image(plot2_total, x=20,y=175 , w=150)

    document.set_fill_color(23, 162, 184)
    document.set_font('helvetica', size= 9)
    document.set_text_color(255,255,255)
    document.multi_cell(document.epw, document.font_size * 2.5, "Bei den Daten der zukünftigen Jahre handelt es sich um Prognosen. Daher kann die Darstellung unvollständig oder leer sein.", border=1, ln=3, max_line_height=document.font_size, fill=True)
    document.set_text_color(0,0,0)

    document.add_page()
    document.set_font('helvetica', 'B', 16)
    document.text(20, 30, 'GEK Vergleich mit anderen Gebäuden (Prognose)')
    document.ln(document.font_size * 1.5)
    document.image(plot2_waerme, x=20,y=65 , w=150)
    document.image(plot2_strom, x=20,y=175 , w=150)

    document.set_fill_color(23, 162, 184)
    document.set_font('helvetica', size= 9)
    document.set_text_color(255,255,255)
    document.multi_cell(document.epw, document.font_size * 2.5, "Bei den Daten der zukünftigen Jahre handelt es sich um Prognosen. Daher kann die Darstellung unvollständig oder leer sein.", border=1, ln=3, max_line_height=document.font_size, fill=True)
    document.set_text_color(0,0,0)

    document.set_font('helvetica', size=7)

    document.add_page()

    heizleistungDict = {}
    for year in data_per_year_waerme:
        if year == "Ziel": continue
        if int(year) < datetime.today().year:
            heizleistungDict[year] = data_per_year_waerme[year]["waerme_endenergie"]
    htmlHeizleistung = generateHeizleistungsbedarf(user, buildingData, energiebezugsflaeche, heizleistungDict)

    document.write_html(htmlHeizleistung)

    document.add_page()

    document.set_font('helvetica', 'B', 12)
    d = generateBuildingDataDict(user)

    line_height = document.font_size * 2.5
    col_width = document.epw / 2

    document.set_fill_color(56, 232, 96)
    document.multi_cell(document.epw, document.font_size * 2.5, "Gebäude Grundangaben", border="LTR", ln=3, max_line_height=document.font_size, fill=True)
    document.ln(line_height)

    i = 0
    items = len(d.items())
    for row in d.items():
        i += 1
        for data in row:
            if type(data) is int: data = str(data) 
            if type(data) is float: data = str(data) 
            data2 = data.encode('latin-1', 'replace').decode('latin-1')
            fill = False
            colwidth = col_width
            if "<b>" in data2:
                data2 = data2.replace("<b>" , "")
                data2 = data2.replace("</b>" , "")
                document.set_font('helvetica', 'B', 9)
                fill = True
                colwidth = document.epw
            else:
                document.set_font('helvetica', size=9)
            border = "LR"
            if (i == items):
                border = "LRB"
                if data=="": continue
            document.multi_cell(colwidth, line_height, data2, border=border, ln=3, max_line_height=document.font_size, fill=fill)
        document.ln(line_height)

    document.add_page()

    document.set_font('helvetica', 'B', 12)
    d = generateEnergyByYearDict(user)
    print(d)

    line_height = document.font_size * 2.5
    col_width = document.epw / 2

    document.multi_cell(document.epw, document.font_size * 2.5, "Energiedaten nach Jahr", border="LTRB", ln=3, max_line_height=document.font_size, fill=True)
    document.ln(line_height)
    document.ln(line_height)

    for row in d.items():
        for data in row:
            if type(data) is str:
                data2 = data.encode('latin-1', 'replace').decode('latin-1')
                fill = False
                colwidth = col_width
                border = "LR"
                if "<b>" in data2:
                    data2 = data2.replace("<b>" , "")
                    data2 = data2.replace("</b>" , "")
                    document.set_font('helvetica', 'B', 9)
                    fill = True
                    colwidth = document.epw
                    border = "LRT"
                else:
                    document.set_font('helvetica', size=9)
                document.multi_cell(colwidth, line_height, data2, border=border, ln=3, max_line_height=document.font_size, fill=fill)
            else:
                i = 0
                items = len(data.items())
                for row2 in data.items():
                    i += 1
                    for data3 in row2:
                        if type(data3) is int: data3 = str(data3) 
                        if type(data3) is float: data3 = str(data3) 
                        data2 = data3.encode('latin-1', 'replace').decode('latin-1')
                        if "<b>" in data2:
                            data2 = data2.replace("<b>" , "")
                            data2 = data2.replace("</b>" , "")
                            document.set_font('helvetica', 'B', 9)
                        else:
                            document.set_font('helvetica', size=9)
                        border = "LR"
                        if (i == items):
                            border = "LRB"
                            if data=="": continue
                        document.multi_cell(col_width, line_height, data2, border=border, ln=3, max_line_height=document.font_size)
                    document.ln(line_height)
            document.ln(line_height)
        document.ln(line_height)

    return document.output()


def calculate (user):

    #start calculation of data from user

    buildingData = BuildingData.objects.get(user = user)
    #error handling
    if buildingData is None: return {"error" : "0"}

    energiebezugsflaeche = buildingData.energiebezugsflaeche

    yearData = EnergyByYear.objects.filter(user = user)

    gebaeudeart = translate(buildingData.gebaeudeart)
    if gebaeudeart == "FREIE_EINGABE": gebaeudeart = buildingData.gebaeudeart_freie_eingabe

    heizwarme = translate(buildingData.heizwaerme_erzeugung_1)
    if (heizwarme == "SONSTIGES"): heizwarme = buildingData.heizwaerme_erzeugung_1_sonstiges
    if buildingData.heizwaerme_erzeugung_2 != "NONE":
        if (buildingData.heizwaerme_erzeugung_2 == "SONSTIGES"): heizwarme += ", " + buildingData.heizwaerme_erzeugung_2_sonstiges
        else: heizwarme += ", " + translate(buildingData.heizwaerme_erzeugung_2)
    if buildingData.heizwaerme_erzeugung_3 != "NONE":
        if (buildingData.heizwaerme_erzeugung_3 == "SONSTIGES"): heizwarme += ", " + buildingData.heizwaerme_erzeugung_3_sonstiges
        else: heizwarme += ", " + translate(buildingData.heizwaerme_erzeugung_3)

    warmwasser = translate(buildingData.warmwasseraufbereitung_1)
    if (warmwasser == "SONSTIGES"): warmwasser = buildingData.warmwasseraufbereitung_1_sonstiges
    if buildingData.warmwasseraufbereitung_2 != "NONE":
        if (buildingData.warmwasseraufbereitung_2 == "SONSTIGES"): warmwasser += ", " + buildingData.warmwasseraufbereitung_2_sonstiges
        else: warmwasser += ", " + translate(buildingData.warmwasseraufbereitung_2)
    if buildingData.warmwasseraufbereitung_3 != "NONE":
        if (buildingData.warmwasseraufbereitung_3 == "SONSTIGES"): warmwasser += ", " + buildingData.warmwasseraufbereitung_3_sonstiges
        else: warmwasser += ", " + translate(buildingData.warmwasseraufbereitung_3)

    pv = "keine Eigenstromproduktion"
    if (buildingData.art_eigenstromanlage != "KEINE"):
        if (buildingData.art_eigenstromanlage == "PV"): pv = "PV-Anlage vorhanden"
        else: pv = "Eigenstrom: " + buildingData.art_eigenstromanlage_sonstiges

    basedata = {"gebaeudeart": gebaeudeart
        , "baujahr" : buildingData.baujahr
        , "street" : user.street
        , "number" : user.number
        , "plz" : user.plz
        , "city" : user.city
        , "owner" : user.owner
        , "energiebezugsflaeche" : buildingData.energiebezugsflaeche
        , "heizwaerme" : heizwarme
        , "warmwasser" : warmwasser
        , "pv" : pv
    }

    gek_total, data_per_year = calculateGEKTotal(yearData, energiebezugsflaeche)
    svg_total = drawGEKDiagram(basedata, gek_total, data_per_year)

    gek_waerme, data_per_year_waerme = calculateGEKWaerme(yearData, energiebezugsflaeche)
    svg_waerme = drawGEKWaermeDiagram(basedata, gek_waerme, data_per_year_waerme)

    gek_strom, data_per_year_strom = calculateGEKStrom(yearData, energiebezugsflaeche)
    svg_strom = drawGEKStromDiagram(basedata, gek_strom, data_per_year_strom)

    #Erzeugte Daten in ResultCache speichern um das Diagramm zu plotten
    for year in gek_total:
        if year == "Ziel": continue
        ResultCache.objects.filter(user = user, jahr=year).delete()
        cache = ResultCache()
        cache.user = user
        cache.jahr = year
        cache.ebf = energiebezugsflaeche
        cache.gek_strom = gek_strom[year]
        cache.gek_strom_kosten = data_per_year_strom[year]["gek_strom_kosten"]
        cache.gek_waerme = gek_waerme[year]
        cache.gek_waerme_kosten = data_per_year_waerme[year]["gek_waerme_kosten"]
        cache.gek_total = gek_total[year]
        cache.gek_total_kosten = data_per_year[year]["gek_kosten"]
        cache.bauart = buildingData.bauart
        cache.save()

    svg_plot1 = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user)
    svg_plot2 = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user)

    svg_plot1_total = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, doplot=1)
    svg_plot1_waerme = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, doplot=2)
    svg_plot1_strom = generateComparisonPlot(datetime.today().year-3, datetime.today().year-1, user, doplot=3)

    svg_plot2_total = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, doplot=1)
    svg_plot2_waerme = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, doplot=2)
    svg_plot2_strom = generateComparisonPlot(datetime.today().year, datetime.today().year+2, user, doplot=3)

    heizleistungDict = {}
    for year in data_per_year_waerme:
        if year == "Ziel": continue
        if int(year) < datetime.today().year:
            heizleistungDict[year] = data_per_year_waerme[year]["waerme_endenergie"]
    htmlHeizleistung = generateHeizleistungsbedarf(user, buildingData, energiebezugsflaeche, heizleistungDict)

    return {"gektotal" : svg_total, "gekwaerme" : svg_waerme, "gekstrom" : svg_strom, "plot_first" : svg_plot1, "plot_second" : svg_plot2,
        "plot_1_total" : svg_plot1_total, "plot_1_waerme" : svg_plot1_waerme, "plot_1_strom" : svg_plot1_strom, 
        "plot_2_total" : svg_plot2_total, "plot_2_waerme" : svg_plot2_waerme, "plot_2_strom" : svg_plot2_strom, 
    "buildingdata" : dictToHTMLTable(generateBuildingDataDict(user)) ,"heizleistung":htmlHeizleistung, "energybyyear" : dictTo3DHTMLTable(generateEnergyByYearDict(user))}

def calculateGEKTotal(yearData, energiebezugsflaeche):
    years = []
    yearDataByYear = {}
    for year in yearData:
        years.append(year.jahr)
        yearDataByYear[year.jahr] = year
    list.sort(years)

    data_per_year = {}
    gek_total = {}

    for year in years:
        data = yearDataByYear[year]
        res = {}
        
        #waerme_endenergie
        waerme_endenergie = 0
        if not data.bedarf_heizoel is None: waerme_endenergie += data.bedarf_heizoel
        if not data.bedarf_gas is None: waerme_endenergie += (data.bedarf_gas/10)
        if not data.bedarf_holz is None: waerme_endenergie += (data.bedarf_holz*170) # Holz 1 Ster -> 1700 kWh/Ster = 170 Liter Öläquivalent/Ster
        if not data.bedarf_holz_hackschnitzel is None: waerme_endenergie += (data.bedarf_holz_hackschnitzel*85) # Holzschnitzel -> 850 kWh/Sm3 -> 85 Liter Öläquivalent
        if not data.bedarf_holzpellets is None: waerme_endenergie += (data.bedarf_holzpellets*0.425) # Holzpellets -> 0.425 Liter Öläquivalent/kg
        if not data.bedarf_fernwärme_heizstrom is None: waerme_endenergie += (data.bedarf_fernwärme_heizstrom/10)

        #TODO: Manuell berechnete Wärme berücksichtigen!

        #strom allgemein
        strom_allgemein = 0
        if not data.bedarf_strom is None: strom_allgemein += data.bedarf_strom/10

        #energie total
        energy_total = waerme_endenergie + strom_allgemein
        gek_total_val = energy_total/energiebezugsflaeche

        gek_total[year] = gek_total_val

        #kosten wärme
        kosten_waerme = 0
        if not data.kosten_heizoel is None: kosten_waerme += data.kosten_heizoel
        if not data.kosten_gas is None: kosten_waerme += data.kosten_gas
        if not data.kosten_holz is None: kosten_waerme += data.kosten_holz
        if not data.kosten_fernwärme is None: kosten_waerme += data.kosten_fernwärme
        if not data.kosten_andere is None: kosten_waerme += data.kosten_andere

        #TODO: Photovoltaik!

        kosten_strom = 0
        if not data.kosten_strom is None: kosten_strom += data.kosten_strom

        kosten_total = kosten_strom + kosten_waerme

        gek_kosten_total = kosten_total/energiebezugsflaeche

        add = {"waerme_endenergie" : waerme_endenergie, "strom_allgemein" : strom_allgemein , "kosten_waerme" : kosten_waerme , "kosten_strom_allgemein" : kosten_strom , "gek_kosten" : gek_kosten_total}
        data_per_year[year] = add

    return gek_total, data_per_year

def calculateGEKWaerme(yearData, energiebezugsflaeche):
    years = []
    yearDataByYear = {}
    for year in yearData:
        years.append(year.jahr)
        yearDataByYear[year.jahr] = year
    list.sort(years)

    data_per_year = {}
    gek_total = {}

    for year in years:
        data = yearDataByYear[year]
        res = {}
        
        #waerme_endenergie
        waerme_endenergie = 0
        if not data.bedarf_heizoel is None: waerme_endenergie += data.bedarf_heizoel
        if not data.bedarf_gas is None: waerme_endenergie += (data.bedarf_gas/10)
        if not data.bedarf_holz is None: waerme_endenergie += (data.bedarf_holz*170) # Holz 1 Ster -> 1700 kWh/Ster = 170 Liter Öläquivalent/Ster
        if not data.bedarf_holz_hackschnitzel is None: waerme_endenergie += (data.bedarf_holz_hackschnitzel*85) # Holzschnitzel -> 850 kWh/Sm3 -> 85 Liter Öläquivalent
        if not data.bedarf_holzpellets is None: waerme_endenergie += (data.bedarf_holzpellets*0.425) # Holzpellets -> 0.425 Liter Öläquivalent/kg
        if not data.bedarf_fernwärme_heizstrom is None: waerme_endenergie += (data.bedarf_fernwärme_heizstrom/10)


        gek_total_val = waerme_endenergie/energiebezugsflaeche

        gek_total[year] = gek_total_val

        #kosten wärme
        kosten_waerme = 0
        if not data.kosten_heizoel is None: kosten_waerme += data.kosten_heizoel
        if not data.kosten_gas is None: kosten_waerme += data.kosten_gas
        if not data.kosten_holz is None: kosten_waerme += data.kosten_holz
        if not data.kosten_fernwärme is None: kosten_waerme += data.kosten_fernwärme
        if not data.kosten_andere is None: kosten_waerme += data.kosten_andere

        gek_kosten_total = kosten_waerme/energiebezugsflaeche

        add = {"waerme_endenergie" : waerme_endenergie, "kosten_waerme" : kosten_waerme , "gek_waerme_kosten" : gek_kosten_total}
        data_per_year[year] = add

    return gek_total, data_per_year


def calculateGEKStrom(yearData, energiebezugsflaeche):
    years = []
    yearDataByYear = {}
    for year in yearData:
        years.append(year.jahr)
        yearDataByYear[year.jahr] = year
    list.sort(years)

    data_per_year = {}
    gek_total = {}

    for year in years:
        data = yearDataByYear[year]
        res = {}

        #strom allgemein
        strom_allgemein = 0
        if not data.bedarf_strom is None: strom_allgemein += data.bedarf_strom/10

        #energie total
        gek_total_val = strom_allgemein/energiebezugsflaeche

        gek_total[year] = gek_total_val

        #TODO: Photovoltaik!

        kosten_strom = 0
        if not data.kosten_strom is None: kosten_strom += data.kosten_strom

        gek_kosten_total = kosten_strom/energiebezugsflaeche

        add = {"strom_allgemein" : strom_allgemein , "kosten_strom" : kosten_strom , "gek_strom_kosten" : gek_kosten_total}
        data_per_year[year] = add

    return gek_total, data_per_year

def generateBuildingDataDict(user):
    buildingData = BuildingData.objects.get(user = user)
    result = collections.OrderedDict()
    result["Benutzername"] = user.username

    #title:
    result["<b>Gebäudedaten</b>"] = ""

    result["Gebäudeart"] = translate(buildingData.gebaeudeart)
    if result["Gebäudeart"] == "FREIE_EINGABE": 
        result["Gebäudeart"] = buildingData.gebaeudeart_freie_eingabe + " [*]"

    result["Bauart"] = translate(buildingData.bauart)
    result["Energiebezugsfläche [m²]"] = translate(buildingData.energiebezugsflaeche)
    result["Baujahr"] = translate(buildingData.baujahr)

    #title:
    result["<b>Sanierung der Gebäudehülle</b>"] = ""

    if not buildingData.sanierung_dach is None: result["Sanierung (Dach)"] = translate(buildingData.sanierung_dach)
    if not buildingData.sanierung_aussenwaende is None: result["Sanierung (Außenwände)"] = translate(buildingData.sanierung_aussenwaende)
    if not buildingData.sanierung_fenster is None: result["Sanierung (Fenster)"] = translate(buildingData.sanierung_fenster)
    if not buildingData.sanierung_kellerdecken is None: result["Sanierung (Kellerdecken)"] = translate(buildingData.sanierung_kellerdecken)
    if not buildingData.sanierung_anderes is None: result["Sanierung (anderes)"] = translate(buildingData.sanierung_anderes)
    if not buildingData.sanierung_anderes_erklaerung is None: result["Erläuterung: Sanierung (anderes)"] = translate(buildingData.sanierung_anderes_erklaerung)

    #title:
    result["<b>Wärmeerzeugung und Abgabe</b>"] = ""

    result["Baujahr Gebäudeheizung"] = translate(buildingData.baujahr_gebaeudeheizung)
    result["Baujahr Warmwasseraufbereitung"] = translate(buildingData.baujahr_warmwasseraufbereitung)

    result["1. Priorität: Heizwärmeerzeugung"] = translate(buildingData.heizwaerme_erzeugung_1)
    if result["1. Priorität: Heizwärmeerzeugung"] == "SONSTIGES":
        result["1. Priorität: Heizwärmeerzeugung"] = buildingData.heizwaerme_erzeugung_1_sonstiges + " [*]"

    if not buildingData.heizwaerme_erzeugung_2 is None:
        result["2. Priorität: Heizwärmeerzeugung"] = translate(buildingData.heizwaerme_erzeugung_2)
        if result["2. Priorität: Heizwärmeerzeugung"] == "SONSTIGES":
            result["2. Priorität: Heizwärmeerzeugung"] = buildingData.heizwaerme_erzeugung_2_sonstiges + " [*]"

    if not buildingData.heizwaerme_erzeugung_3 is None:
        result["3. Priorität: Heizwärmeerzeugung"] = translate(buildingData.heizwaerme_erzeugung_3)
        if result["3. Priorität: Heizwärmeerzeugung"] == "SONSTIGES":
            result["3. Priorität: Heizwärmeerzeugung"] = buildingData.heizwaerme_erzeugung_3_sonstiges + " [*]"

    result["1. Priorität: Warmwasseraufbereitung"] = translate(buildingData.warmwasseraufbereitung_1)
    if result["1. Priorität: Warmwasseraufbereitung"] == "SONSTIGES":
        result["1. Priorität: Warmwasseraufbereitung"] = buildingData.warmwasseraufbereitung_1_sonstiges + " [*]"

    if not buildingData.heizwaerme_erzeugung_2 is None:
        result["2. Priorität: Warmwasseraufbereitung"] = translate(buildingData.warmwasseraufbereitung_2)
        if result["2. Priorität: Warmwasseraufbereitung"] == "SONSTIGES":
            result["2. Priorität: Warmwasseraufbereitung"] = buildingData.warmwasseraufbereitung_2_sonstiges + " [*]"

    if not buildingData.heizwaerme_erzeugung_3 is None:
        result["3. Priorität: Warmwasseraufbereitung"] = translate(buildingData.warmwasseraufbereitung_3)
        if result["3. Priorität: Warmwasseraufbereitung"] == "SONSTIGES":
            result["3. Priorität: Warmwasseraufbereitung"] = buildingData.warmwasseraufbereitung_3_sonstiges + " [*]"

    result["Leistung Wärmeerzeuger [kW]"] = translate(buildingData.leistung_waermeerzeuger)
    
    result["Wärmeabgabe"] = translate(buildingData.waermeabgabe)
    if result["Wärmeabgabe"] == "SONSTIGES": 
        result["Wärmeabgabe"] = buildingData.waermeabgabe_sonstiges + " [*]"

    result["Regelung der Wärmeabgabe"] = translate(buildingData.regelung_waermeabgabe)
    if result["Regelung der Wärmeabgabe"] == "SONSTIGES": 
        result["Regelung der Wärmeabgabe"] = buildingData.regelung_waermeabgabe_sonstiges + " [*]"

    #title:
    result["<b>Brauchwarmwasser</b>"] = ""

    result["Brauchwarmwasserzirkulation"] = translate(buildingData.brauchwarmwasserzirkulation)
    if not buildingData.brauchwarmwasser_speicher_inhalt is None: result["Inhalt Brauchwarmwasserspeichers (Liter)"] = translate(buildingData.brauchwarmwasser_speicher_inhalt)

    #title:
    result["<b>Eigenstromproduktion</b>"] = ""

    result["Eigenstromanlage"] = translate(buildingData.art_eigenstromanlage)
    if result["Eigenstromanlage"] == "SONSTIGES": 
        result["Eigenstromanlage"] = buildingData.art_eigenstromanlage_sonstiges + " [*]"

    if result["Eigenstromanlage"] != "keine":
        if not buildingData.peak_leistung_eigenstromanlage is None: result["Peak Leistung der Eigenstromanlage [kWp]"] = translate(buildingData.peak_leistung_eigenstromanlage)
        if not buildingData.kapazitaet_batteriespeicher is None: result["Kapazität Batteriespeicher [kWh]"] = translate(buildingData.kapazitaet_batteriespeicher)

    #title:
    result["<b>Geplante Investitionen in den nächsten 10 Jahren in Euro</b>"] = ""

    if not buildingData.investition_waermeerzeugung is None: result["Investitionen in Wärmeerzeugung"] = translate(buildingData.investition_waermeerzeugung)
    if not buildingData.investition_warmwasseraufbereitung is None: result["Investitionen in Warmwasseraufbereitung"] = translate(buildingData.investition_warmwasseraufbereitung)
    if not buildingData.investition_eigenstromproduktion_batteriespeicher is None: result["Investitionen in Eigenstromproduktion, Batteriespeicher"] = translate(buildingData.investition_eigenstromproduktion_batteriespeicher)
    if not buildingData.investition_sanierung_gebaeudehuelle is None: result["Investitionen in Sanierung der Gebäudehülle"] = translate(buildingData.investition_sanierung_gebaeudehuelle)
    if not buildingData.investition_andere is None: result["Investitionen (anderes)"] = translate(buildingData.investition_andere)
    
    return result

def generateEnergyByYearDict(user):
    years = EnergyByYear.objects.filter(user = user)
    result = collections.OrderedDict()

    for jahr in years:

        yresult = {}

        if not jahr.bedarf_heizoel is None: yresult["Bedarf Heizöl [Liter]"] = translate(jahr.bedarf_heizoel)
        if not jahr.bedarf_gas is None: yresult["Bedarf Gas [kWh]"] = translate(jahr.bedarf_gas)
        yresult["Bedarf Strom [kWh]"] = translate(jahr.bedarf_strom)
        if not jahr.bedarf_holz is None: yresult["Bedarf Holz [Ster]"] = translate(jahr.bedarf_holz)
        if not jahr.bedarf_holz_hackschnitzel is None: yresult["Bedarf Holz (Hackschnitzel) [Srm]"] = translate(jahr.bedarf_holz_hackschnitzel)
        if not jahr.bedarf_holzpellets is None: yresult["Bedarf Holzpellets [kg]"] = translate(jahr.bedarf_holzpellets)
        if not jahr.bedarf_fernwärme_heizstrom is None: yresult["Bedarf Fernwärme/Heizstrom [kWh]"] = translate(jahr.bedarf_fernwärme_heizstrom)

        if not jahr.kosten_heizoel is None: yresult["Kosten Heizöl"] = translate(jahr.kosten_heizoel)
        if not jahr.kosten_gas is None: yresult["Kosten Gas"] = translate(jahr.kosten_gas)
        if not jahr.kosten_strom is None: yresult["Kosten Strom"] = translate(jahr.kosten_strom)
        if not jahr.kosten_holz is None: yresult["Kosten Holz"] = translate(jahr.kosten_holz)
        if not jahr.kosten_fernwärme is None: yresult["Kosten Fernwärme"] = translate(jahr.kosten_fernwärme)
        if not jahr.kosten_andere is None: yresult["Kosten (andere)"] = translate(jahr.kosten_andere)

        if not jahr.eigenstrom_jahresertrag is None: yresult["Eigenstrom Jahresertrag [kWh]"] = translate(jahr.eigenstrom_jahresertrag)
        if not jahr.eigenstrom_netzeinspeisung is None: yresult["Netzeinspeisung Eigenstrom [kWh]"] = translate(jahr.eigenstrom_netzeinspeisung)
        if not jahr.eigenstrom_netzeinspeisung_ertrag is None: yresult["Netzeinspeisung Eigenstrom [Euro]"] = translate(jahr.eigenstrom_netzeinspeisung_ertrag)
    
        result["<b>Daten für "+str(jahr.jahr)+"</b>"] = yresult

    return collections.OrderedDict(sorted(result.items()))


def dictToHTMLTable(dic):
    html = "<table  class=\"table\">"

    for key, value in dic.items():
        html += "<tr><td width=\"60%\">" + str(key) + "</td><td>" + str(value) + "</td></tr>"

    html += "</table>"
    return html

def dictTo3DHTMLTable(dic):
    html = "<table  class=\"table\">"

    for key, value in dic.items():
        if type(value) is str:
            html += "<tr><td width=\"60%\">" + str(key) + "</td><td>" + str(value) + "</td></tr>"
        else:
            html += "<tr><td width=\"60%\">" + str(key) + "</td><td>" 
            for key, value in value.items():
                html += "<tr><td width=\"60%\">" + str(key) + "</td><td>" + str(value) + "</td></tr>"
            html += "</td></tr>"

    html += "</table>"
    return html

def fstr(st):
    string = "{:.2f}".format(st)
    string = string.replace("." , ",")
    return string

#map year to "Wärme Endenergie" value
def generateHeizleistungsbedarf(user, buildingdata, ebf, year_waerme_dict):
    html = "<h3>Abschätzung der Heizleistung, kW</h3><br>"
    html += "Wärmeenergiebedarf pro Jahr, in ÖE:<br>"
    html += "<table  class=\"table\"><tr>"
    size = int(100/(len(year_waerme_dict)+1))
    for year in year_waerme_dict:
        html += "<th width='"+str(size)+"%'>" + str(year) + "</th>"
    html += "<th  width='"+str(size)+"%' style='text-align: right' align='right'>Mittelwert</th></tr><tr>"
    value = 0
    counter = 0
    for year in year_waerme_dict:
        counter += 1
        value += year_waerme_dict[year]
        html += "<td>" + fstr(year_waerme_dict[year]) + "</td>"
    mittelwert = value/counter
    html += "<td style='text-align: right' align='right'>" + fstr(mittelwert) + "</td></tr></table>"

    vbs = 0
    vbs_str = ""
    if buildingdata.heizwaerme_erzeugung_1 == buildingdata.warmwasseraufbereitung_1:
        vbs = config.VBS_WITH_WW
        vbs_str = "Vollbetriebstunden mit WW"
    else:
        vbs = config.VBS_WITHOUT_WW
        vbs_str = "Vollbetriebstunden ohne WW"

    heizleistungsbedarf = mittelwert*10/vbs

    #Ergebnistabelle
    html += "<table  class=\"table\">"
    html += "<tr><th width='70%'><b>Heizleistung, abgeschätzt</b></th><th width='30%' style='text-align: right' align='right'>" + fstr(heizleistungsbedarf) + " kW</th></tr>"
    html += "<tr><td>"+vbs_str+"</td><td style='text-align: right' align='right'>" + str(vbs) + " h</td></tr>"
    html += "<tr><td>Heizleistung, abgeschätzt pro m² EBF</td><td style='text-align: right' align='right'>" + fstr(heizleistungsbedarf/ebf*1000) + " Watt/m² (*)</td></tr>"
    html += "<tr><td>Leistung ihres Wärmeerzeugers</td><td style='text-align: right' align='right'>" + str(buildingdata.leistung_waermeerzeuger) + "kW</td></tr>" 
    html += "</table><br>"
    html += "<small>* Dieser Wert sollte bei unter 40W liegen</small>"
    return html