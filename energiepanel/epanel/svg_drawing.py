#!/usr/bin/python
# -*- coding: <encoding name> -*-
import svgwrite
import webbrowser

#function to format floats to the german standart 
def fstr(st):
    string = "{:.2f}".format(st)
    string = string.replace("." , ",")
    return string

""" year_val_dict contains the years as keys and the oil liter/m² as value """
def drawGEKDiagram(base_data, year_val_dict, data_per_year):

    dwg = svgwrite.Drawing('temp.svg', style="display: inline-block; vertical-align: top;", size=("100%","100%"), profile='full' , viewBox="0 0 560 617")

    #top-banner
    topbanner = dwg.g()
    topbanner.add(dwg.rect(insert=(0,0), size=(560,20), fill="lightgray"))

    topbanner.add(dwg.text('GEK Total', insert=(5, 14), fill='black' , font_size="14px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text('(GebäudeEnergieKennzahl Total - basierend auf Endenergie)', insert=(75, 13), fill='black' , font_size="11px" , font_family="Dejavu Sans"))

    #gebaeudeart
    topbanner.add(dwg.text('Gebäude:', insert=(5, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["gebaeudeart"], insert=(120, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans" , font_weight="bold"))

    #baujahr
    topbanner.add(dwg.text('Baujahr:', insert=(5, 55), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["baujahr"], insert=(120, 55), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #adresse
    topbanner.add(dwg.text('Adresse:', insert=(5, 70), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["street"] + " " + str(base_data["number"]), insert=(120, 70), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(str(base_data["plz"]) + " " + base_data["city"], insert=(120, 80), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #eigentümer
    topbanner.add(dwg.text('Eigentümer:', insert=(5, 95), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["owner"], insert=(120, 95), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #energiebezugsflaeche
    topbanner.add(dwg.text('Energiebezugsfläche:', insert=(5, 110), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(str(base_data["energiebezugsflaeche"])+ " m²", insert=(120, 110), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #heizwarme und warmwasser

    topbanner.add(dwg.text("Heizwärme erzeugt mit: " + base_data["heizwaerme"], insert=(270, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text("Warmwasser erzeugt mit: " + base_data["warmwasser"], insert=(270, 50), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    topbanner.add(dwg.line(start=(0, 120), end=(560, 120), stroke='black', stroke_width="1"))

    dwg.add(topbanner)

    #---- end top banner

    main = dwg.g(transform="translate(0, 120)")
    main.add(dwg.text('Öläquivalent', insert=(5, 50), fill='black' , font_size="7px" , font_family="Dejavu Sans"))

    #outer lines
    main.add(dwg.line(start=(0, 55), end=(560, 55), stroke='black', stroke_width="0.5"))
    main.add(dwg.line(start=(60, 0), end=(60, 270), stroke='black', stroke_width="0.2"))
    main.add(dwg.line(start=(140, 0), end=(140, 270), stroke='black', stroke_width="0.9"))

    #Distance of 30 between levels
    main.add(dwg.text('< 3.5 Liter/m²', insert=(5, 70), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 6.0 Liter/m²', insert=(5, 100), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 8.5 Liter/m²', insert=(5, 130), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 11.0 Liter/m²', insert=(5, 160), fill='black' , font_size="7px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 13.5 Liter/m²', insert=(5, 190), fill='black' , font_size="7px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 16.0 Liter/m²', insert=(5, 220), fill='black' , font_size="7px" , font_family="Dejavu Sans"))
    main.add(dwg.text('> 18.5 Liter/m²', insert=(5, 250), fill='black' , font_size="7px" , font_family="Dejavu Sans"))

    #Text Bewertung
    main.add(dwg.text('Bewertung', insert=(65, 20), fill='black' , font_size="13px" , font_family="Dejavu Sans"))

    #colored reference arrows
    x,y,width,text = 60,60, 20, "A"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#339966', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,90, 25, "B"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#1FB714', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,120, 30, "C"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#CCFFCC', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,150, 35, "D"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FFFF99', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,180, 40, "E"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FCF305', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,210, 45, "F"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FF9900', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,240, 50, "G"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#DD0806', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    #Text Entwicklung
    main.add(dwg.text('Entwicklung', insert=(150, 20), fill='black' , font_size="14px" , font_family="Dejavu Sans"))

    #Plot data

    #Add "year" "Ziel"with value 3.5
    year_val_dict["Ziel"] = 3.5

    #save current shift
    x = 160

    for year in year_val_dict:
        value = year_val_dict[year]

        #Show year label
        main.add(dwg.text(year, insert=(x+10, 40), fill='black' , font_size="9px" , font_family="Dejavu Sans", text_anchor="middle"))
        if year == "Ziel":
            main.add(dwg.line(start=(x+40, 0), end=(x+40, 270), stroke='black', stroke_width="0.9"))
            main.add(dwg.line(start=(x-20, 0), end=(x-20, 270), stroke='black', stroke_width="0.9"))
        else: main.add(dwg.line(start=(x+40, 30), end=(x+40, 270), stroke='black', stroke_width="0.2"))

        #draw filled arrow

        #calculate color
        if value <= 3.5: color = "#339966"
        elif value <= 6: color = "#1FB714"
        elif value <= 8.5: color = "#CCFFCC"
        elif value <= 11.0: color = "#FFFF99"
        elif value <= 13.5: color = "#FCF305"
        elif value <= 16: color = "#FF9900"
        else: color = "#DD0806"

        #calculate y coordinate
        min_y = 70
        max_y = 250
        diff = max_y-min_y

        temp_val = value-3.5
        percent = temp_val/(18.5-3.5)
        d_y = percent*(max_y-min_y) + min_y - 10
        d_y = max(d_y,min_y - 10)
        d_y = min(d_y, max_y)

        d_x,width,text = x+5, 35, "{:.1f}".format(value)
        main.add(dwg.polygon(points=[(d_x+0,d_y+0) , (d_x+width,d_y+0), (d_x+width,d_y+20) , (d_x+0,d_y+20) , (d_x-10,d_y+10)], fill=color, stroke="black"))
        main.add(dwg.text(text, insert=(d_x+width-3, d_y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans", text_anchor="end"))

        x += 60

    dwg.add(main)

    #Energiebedarf nach Jahr

    bottombanner = dwg.g(transform="translate(0, 390)")

    bottombanner.add(dwg.line(start=(0, 0), end=(560, 0), stroke='black', stroke_width="0.5"))
    bottombanner.add(dwg.text('Energiebedarf pro Jahr', insert=(5, 16), fill='black' , font_size="11px" , font_family="Dejavu Sans", font_weight="bold"))
    bottombanner.add(dwg.text('in Liter Öläquivalent (OE)', insert=(150, 16), fill='black' , font_size="8px" , font_family="Dejavu Sans"))

    #Linke beschriftungen und linien zeichnen
    bottombanner.add(dwg.line(start=(0, 44), end=(560, 44), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.text('Wärme Endenergie', insert=(5, 56), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 60), end=(560, 60), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.text('Strom allgemein', insert=(5, 72), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 76), end=(560, 76), stroke='black', stroke_width="0.8"))
    bottombanner.add(dwg.text('Energie Total:', insert=(5, 87), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 92), end=(560, 92), stroke='black', stroke_width="0.8"))
    bottombanner.add(dwg.rect(insert=(0,94), size=(560,15), fill="lightgray"))
    bottombanner.add(dwg.text('GEK Total [OE/m²]:', insert=(5, 105), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 120), end=(560, 120), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.text('Kosten Wärme [€]', insert=(5, 131), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 136), end=(560, 136), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.text('Kosten Strom allgemein [€]', insert=(5, 147), fill='black' , font_size="9.7px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 152), end=(560, 152), stroke='black', stroke_width="0.8"))
    bottombanner.add(dwg.text('Kosten Total [€]', insert=(5, 163), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 168), end=(560, 168), stroke='black', stroke_width="0.8"))
    bottombanner.add(dwg.rect(insert=(0,170), size=(560,15), fill="lightgray"))
    bottombanner.add(dwg.text('GEK Kosten Total [€/m²]:', insert=(5, 181), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #winizige Anmerkungen unten links:
    bottombanner.add(dwg.text('Definition Endenergie:', insert=(5, 197), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    bottombanner.add(dwg.text('extern eingekaufte Energie', insert=(140, 197), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.text('Umrechnungsfaktor:', insert=(5, 209), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    bottombanner.add(dwg.text('1 Liter Öläquivalent (OE) = 10 kWh', insert=(140, 209), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.text('m² ist hier die Energiebezugsfläche wie eingegeben', insert=(5, 221), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(140, 30), end=(140, 185), stroke='black', stroke_width="0.2"))

    data_per_year["Ziel"] = {"waerme_endenergie" : 600, "strom_allgemein" : 100 , "kosten_waerme" : 420 , "kosten_strom_allgemein" : 280 , "gek_kosten" : 3.5}

    x = 160
    for year in year_val_dict:
        bottombanner.add(dwg.line(start=(x+40, 30), end=(x+40, 185), stroke='black', stroke_width="0.2"))
        bottombanner.add(dwg.text(year, insert=(x+10, 40), fill='black' , font_size="7px" , font_family="Dejavu Sans", text_anchor="middle"))

        bottombanner.add(dwg.text(str(data_per_year[year]["waerme_endenergie"]), insert=(x + 35, 56), fill='black' , font_size="10px" , font_family="Dejavu Sans" , text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["strom_allgemein"]), insert=(x + 35, 72), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["strom_allgemein"] + data_per_year[year]["waerme_endenergie"]), insert=(x + 35, 87), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(year_val_dict[year]), insert=(x + 35, 105), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["kosten_waerme"]), insert=(x + 35, 131), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["kosten_strom_allgemein"]), insert=(x + 35, 147), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["kosten_waerme"] + data_per_year[year]["kosten_strom_allgemein"]), insert=(x + 35, 163), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["gek_kosten"]), insert=(x + 35, 181), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        x += 60


    dwg.add(bottombanner)

    #--------- ende bottom banner

    dwg.add(dwg.rect(insert=(0,0) , size=(560,617) , fill_opacity="0.0" , stroke="black" , stroke_width="1"))

    return dwg.tostring()


""" year_val_dict contains the years as keys and the oil liter/m² as value """
def drawGEKWaermeDiagram(base_data, year_val_dict, data_per_year):

    dwg = svgwrite.Drawing('temp.svg', style="display: inline-block; vertical-align: top;", size=("100%","100%"), profile='full' , viewBox="0 0 560 540")

    #top-banner
    topbanner = dwg.g()
    topbanner.add(dwg.rect(insert=(0,0), size=(560,20), fill="#ff937b"))

    topbanner.add(dwg.text('GEK Wärme', insert=(5, 14), fill='black' , font_size="14px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text('(GebäudeEnergieKennzahl Wärme - basierend auf Endenergie)', insert=(90, 13), fill='black' , font_size="11px" , font_family="Dejavu Sans"))

    #gebaeudeart
    topbanner.add(dwg.text('Gebäude:', insert=(5, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["gebaeudeart"], insert=(120, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans" , font_weight="bold"))

    #baujahr
    topbanner.add(dwg.text('Baujahr:', insert=(5, 55), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["baujahr"], insert=(120, 55), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #adresse
    topbanner.add(dwg.text('Adresse:', insert=(5, 70), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["street"] + " " + str(base_data["number"]), insert=(120, 70), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(str(base_data["plz"]) + " " + base_data["city"], insert=(120, 80), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #eigentümer
    topbanner.add(dwg.text('Eigentümer:', insert=(5, 95), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["owner"], insert=(120, 95), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #energiebezugsflaeche
    topbanner.add(dwg.text('Energiebezugsfläche:', insert=(5, 110), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(str(base_data["energiebezugsflaeche"])+ " m²", insert=(120, 110), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #heizwarme und warmwasser

    topbanner.add(dwg.text("Heizwärme erzeugt mit: " + base_data["heizwaerme"], insert=(270, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text("Warmwasser erzeugt mit: " + base_data["warmwasser"], insert=(270, 50), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    topbanner.add(dwg.line(start=(0, 120), end=(560, 120), stroke='black', stroke_width="1"))

    dwg.add(topbanner)

    #---- end top banner

    main = dwg.g(transform="translate(0, 120)")
    main.add(dwg.text('Öläquivalent', insert=(5, 50), fill='black' , font_size="7px" , font_family="Dejavu Sans"))

    #outer lines
    main.add(dwg.line(start=(0, 55), end=(560, 55), stroke='black', stroke_width="0.5"))
    main.add(dwg.line(start=(60, 0), end=(60, 270), stroke='black', stroke_width="0.2"))
    main.add(dwg.line(start=(140, 0), end=(140, 270), stroke='black', stroke_width="0.9"))

    #Distance of 30 between levels
    main.add(dwg.text('< 3 Liter/m²', insert=(5, 70), fill='black' , font_size="8px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 5 Liter/m²', insert=(5, 100), fill='black' , font_size="8px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 7 Liter/m²', insert=(5, 130), fill='black' , font_size="8px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 9 Liter/m²', insert=(5, 160), fill='black' , font_size="8px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 11 Liter/m²', insert=(5, 190), fill='black' , font_size="8px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 13 Liter/m²', insert=(5, 220), fill='black' , font_size="8px" , font_family="Dejavu Sans"))
    main.add(dwg.text('> 15 Liter/m²', insert=(5, 250), fill='black' , font_size="8px" , font_family="Dejavu Sans"))

    #Text Bewertung
    main.add(dwg.text('Bewertung', insert=(65, 20), fill='black' , font_size="13px" , font_family="Dejavu Sans"))

    #colored reference arrows
    x,y,width,text = 60,60, 20, "A"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#339966', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,90, 25, "B"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#1FB714', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,120, 30, "C"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#CCFFCC', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,150, 35, "D"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FFFF99', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,180, 40, "E"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FCF305', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,210, 45, "F"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FF9900', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,240, 50, "G"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#DD0806', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    #Text Entwicklung
    main.add(dwg.text('Entwicklung', insert=(150, 20), fill='black' , font_size="14px" , font_family="Dejavu Sans"))

    #Plot data

    #Add "year" "Ziel"with value 3.5
    year_val_dict["Ziel"] = 3.0

    #save current shift
    x = 160

    for year in year_val_dict:
        value = year_val_dict[year]

        #Show year label
        main.add(dwg.text(year, insert=(x+10, 40), fill='black' , font_size="9px" , font_family="Dejavu Sans", text_anchor="middle"))
        if year == "Ziel":
            main.add(dwg.line(start=(x+40, 0), end=(x+40, 270), stroke='black', stroke_width="0.9"))
            main.add(dwg.line(start=(x-20, 0), end=(x-20, 270), stroke='black', stroke_width="0.9"))
        else: main.add(dwg.line(start=(x+40, 30), end=(x+40, 270), stroke='black', stroke_width="0.2"))
        #draw filled arrow

        #calculate color
        if value <= 3: color = "#339966"
        elif value <= 5: color = "#1FB714"
        elif value <= 7: color = "#CCFFCC"
        elif value <= 9: color = "#FFFF99"
        elif value <= 11: color = "#FCF305"
        elif value <= 13: color = "#FF9900"
        else: color = "#DD0806"

        #calculate y coordinate
        min_y = 70
        max_y = 250
        diff = max_y-min_y

        temp_val = value-3.0
        percent = temp_val/(15.0-3.0)
        d_y = percent*(max_y-min_y) + min_y - 10
        d_y = max(d_y,min_y - 10)
        d_y = min(d_y, max_y)

        d_x,width,text = x+5, 35, "{:.1f}".format(value)
        main.add(dwg.polygon(points=[(d_x+0,d_y+0) , (d_x+width,d_y+0), (d_x+width,d_y+20) , (d_x+0,d_y+20) , (d_x-10,d_y+10)], fill=color, stroke="black"))
        main.add(dwg.text(text, insert=(d_x+width-3, d_y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans", text_anchor="end"))

        x += 60

    dwg.add(main)

    #Energiebedarf nach Jahr

    bottombanner = dwg.g(transform="translate(0, 390)")

    bottombanner.add(dwg.line(start=(0, 0), end=(560, 0), stroke='black', stroke_width="0.5"))
    bottombanner.add(dwg.text('Wärmebedarf pro Jahr', insert=(5, 16), fill='black' , font_size="11px" , font_family="Dejavu Sans", font_weight="bold"))
    bottombanner.add(dwg.text('in Liter Öläquivalent (OE)', insert=(147, 16), fill='black' , font_size="8px" , font_family="Dejavu Sans"))

    #Linke beschriftungen und linien zeichnen
    bottombanner.add(dwg.line(start=(0, 44), end=(560, 44), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.text('Wärme Endenergie', insert=(5, 56), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 60), end=(560, 60), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.rect(insert=(0,62), size=(560,15), fill="#ff937b"))
    bottombanner.add(dwg.text('GEK-Wärme [OE/m²]:', insert=(5, 73), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 79), end=(560, 79), stroke='black', stroke_width="0.8"))
    bottombanner.add(dwg.text('Kosten Wärme [€]', insert=(5, 90), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 96), end=(560, 96), stroke='black', stroke_width="0.2"))

    bottombanner.add(dwg.rect(insert=(0,98), size=(560,15), fill="#ff937b"))
    bottombanner.add(dwg.text('E-Wärme Kosten [€/m²]:', insert=(5, 109), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #winizige Anmerkungen unten links:
    bottombanner.add(dwg.text('Definition Endenergie:', insert=(5, 123), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    bottombanner.add(dwg.text('extern eingekaufte Energie', insert=(140, 123), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.text('Umrechnungsfaktor:', insert=(5, 135), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    bottombanner.add(dwg.text('1 Liter Öläquivalent (OE) = 10 kWh', insert=(140, 135), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.text('m² ist hier die Energiebezugsfläche wie eingegeben', insert=(5, 147), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(140, 30), end=(140, 113), stroke='black', stroke_width="0.2"))

    data_per_year["Ziel"] = {"waerme_endenergie" : 600, "kosten_waerme" : 420.0 , "gek_waerme_kosten" : 2.1}

    x = 160
    for year in year_val_dict:
        bottombanner.add(dwg.line(start=(x+40, 30), end=(x+40, 113), stroke='black', stroke_width="0.2"))
        bottombanner.add(dwg.text(year, insert=(x+10, 40), fill='black' , font_size="7px" , font_family="Dejavu Sans", text_anchor="middle"))

        bottombanner.add(dwg.text(str(data_per_year[year]["waerme_endenergie"]), insert=(x + 35, 56), fill='black' , font_size="10px" , font_family="Dejavu Sans" , text_anchor="end"))

        bottombanner.add(dwg.text(fstr(year_val_dict[year]), insert=(x + 35, 73), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["kosten_waerme"]), insert=(x + 35, 90), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))
        bottombanner.add(dwg.text(fstr(data_per_year[year]["gek_waerme_kosten"]), insert=(x + 35, 109), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        x += 60


    dwg.add(bottombanner)

    #--------- ende bottom banner

    dwg.add(dwg.rect(insert=(0,0) , size=(560,540) , fill_opacity="0.0" , stroke="black" , stroke_width="1"))

    return dwg.tostring()


""" year_val_dict contains the years as keys and the oil liter/m² as value """
def drawGEKStromDiagram(base_data, year_val_dict, data_per_year):

    dwg = svgwrite.Drawing('temp.svg', style="display: inline-block; vertical-align: top; font-family: Dejavu Sans;", size=("100%","100%"), profile='full' , viewBox="0 0 560 540")

    #top-banner
    topbanner = dwg.g()
    topbanner.add(dwg.rect(insert=(0,0), size=(560,20), fill="cyan"))

    topbanner.add(dwg.text('GEK Strom', insert=(5, 14), fill='black' , font_size="14px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text('(GebäudeEnergieKennzahl Strom - basierend auf Endenergie)', insert=(84, 13), fill='black' , font_size="11px" , font_family="Dejavu Sans"))

    #gebaeudeart
    topbanner.add(dwg.text('Gebäude:', insert=(5, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["gebaeudeart"], insert=(120, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans" , font_weight="bold"))

    #baujahr
    topbanner.add(dwg.text('Baujahr:', insert=(5, 55), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["baujahr"], insert=(120, 55), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #adresse
    topbanner.add(dwg.text('Adresse:', insert=(5, 70), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["street"] + " " + str(base_data["number"]), insert=(120, 70), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(str(base_data["plz"]) + " " + base_data["city"], insert=(120, 80), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #eigentümer
    topbanner.add(dwg.text('Eigentümer:', insert=(5, 95), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["owner"], insert=(120, 95), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #energiebezugsflaeche
    topbanner.add(dwg.text('Energiebezugsfläche:', insert=(5, 110), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(str(base_data["energiebezugsflaeche"])+ " m²", insert=(120, 110), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #heizwarme und warmwasser

    topbanner.add(dwg.text("Heizwärme erzeugt mit: " + base_data["heizwaerme"], insert=(270, 40), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text("Warmwasser erzeugt mit: " + base_data["warmwasser"], insert=(270, 50), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    topbanner.add(dwg.text(base_data["pv"], insert=(270, 60), fill='black' , font_size="10px" , font_family="Dejavu Sans"))


    topbanner.add(dwg.line(start=(0, 120), end=(560, 120), stroke='black', stroke_width="1"))

    dwg.add(topbanner)

    #---- end top banner

    main = dwg.g(transform="translate(0, 120)")
    main.add(dwg.text('Öläquivalent', insert=(5, 50), fill='black' , font_size="7px" , font_family="Dejavu Sans"))

    #outer lines
    main.add(dwg.line(start=(0, 55), end=(560, 55), stroke='black', stroke_width="0.5"))
    main.add(dwg.line(start=(60, 0), end=(60, 270), stroke='black', stroke_width="0.2"))
    main.add(dwg.line(start=(140, 0), end=(140, 270), stroke='black', stroke_width="0.9"))

    #Distance of 30 between levels
    main.add(dwg.text('< 0.5 Liter/m²', insert=(5, 70), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 1.0 Liter/m²', insert=(5, 100), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 1.5 Liter/m²', insert=(5, 130), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 2.0 Liter/m²', insert=(5, 160), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 2.5 Liter/m²', insert=(5, 190), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('< 3.0 Liter/m²', insert=(5, 220), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))
    main.add(dwg.text('> 3.5 Liter/m²', insert=(5, 250), fill='black' , font_size="7.5px" , font_family="Dejavu Sans"))

    #Text Bewertung
    main.add(dwg.text('Bewertung', insert=(65, 20), fill='black' , font_size="13px" , font_family="Dejavu Sans"))

    #colored reference arrows
    x,y,width,text = 60,60, 20, "A"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#339966', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,90, 25, "B"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#1FB714', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,120, 30, "C"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#CCFFCC', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,150, 35, "D"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FFFF99', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,180, 40, "E"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FCF305', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,210, 45, "F"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#FF9900', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    x,y,width,text = 60,240, 50, "G"
    main.add(dwg.polygon(points=[(x+0,y+0) , (x+width,y+0), (x+width+10,y+10), (x+width,y+20) , (x+0,y+20)], fill='#DD0806', stroke="black"))
    main.add(dwg.text(text, insert=(x+3, y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans"))
    main.add(dwg.line(start=(x+width+10,y+10), end=(560,y+10), stroke='grey', stroke_width="0.1"))

    #Text Entwicklung
    main.add(dwg.text('Entwicklung', insert=(150, 20), fill='black' , font_size="14px" , font_family="Dejavu Sans"))

    #Plot data

    #Add "year" "Ziel"with value 3.5
    year_val_dict["Ziel"] = 0.5

    #save current shift
    x = 160

    for year in year_val_dict:
        value = year_val_dict[year]

        #Show year label
        main.add(dwg.text(year, insert=(x+10, 40), fill='black' , font_size="9px" , font_family="Dejavu Sans", text_anchor="middle"))
        if year == "Ziel":
            main.add(dwg.line(start=(x+40, 0), end=(x+40, 270), stroke='black', stroke_width="0.9"))
            main.add(dwg.line(start=(x-20, 0), end=(x-20, 270), stroke='black', stroke_width="0.9"))
        else: main.add(dwg.line(start=(x+40, 30), end=(x+40, 270), stroke='black', stroke_width="0.2"))

        #calculate color
        if value <= 0.5: color = "#339966"
        elif value <= 1: color = "#1FB714"
        elif value <= 1.5: color = "#CCFFCC"
        elif value <= 2: color = "#FFFF99"
        elif value <= 2.5: color = "#FCF305"
        elif value <= 3: color = "#FF9900"
        else: color = "#DD0806"

        #calculate y coordinate
        min_y = 70
        max_y = 250
        diff = max_y-min_y

        temp_val = value-0.5
        percent = temp_val/(3.5-0.5)
        d_y = percent*(max_y-min_y) + min_y - 10
        d_y = max(d_y,min_y - 10)
        d_y = min(d_y, max_y)

        d_x,width,text = x+5, 35, "{:.1f}".format(value)
        main.add(dwg.polygon(points=[(d_x+0,d_y+0) , (d_x+width,d_y+0), (d_x+width,d_y+20) , (d_x+0,d_y+20) , (d_x-10,d_y+10)], fill=color, stroke="black"))
        main.add(dwg.text(text, insert=(d_x+width-3, d_y+15), fill='black' , font_size="15px" , font_family="Dejavu Sans", text_anchor="end"))

        x += 60

    dwg.add(main)

    #Energiebedarf nach Jahr

    bottombanner = dwg.g(transform="translate(0, 390)")

    bottombanner.add(dwg.line(start=(0, 0), end=(560, 0), stroke='black', stroke_width="0.5"))
    bottombanner.add(dwg.text('Strombedarf pro Jahr', insert=(5, 16), fill='black' , font_size="11px" , font_family="Dejavu Sans", font_weight="bold"))
    bottombanner.add(dwg.text('in Liter Öläquivalent (OE)', insert=(140, 16), fill='black' , font_size="8px" , font_family="Dejavu Sans"))

    #Linke beschriftungen und linien zeichnen
    bottombanner.add(dwg.line(start=(0, 44), end=(560, 44), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.text('Strom allgemein:', insert=(5, 56), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 60), end=(560, 60), stroke='black', stroke_width="0.2"))
    bottombanner.add(dwg.rect(insert=(0,62), size=(560,15), fill="#4b8ecc"))
    bottombanner.add(dwg.text('GEK-Strom [OE/m²]:', insert=(5, 73), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 79), end=(560, 79), stroke='black', stroke_width="0.8"))
    bottombanner.add(dwg.text('Kosten Strom allgemein [€]', insert=(5, 91), fill='black' , font_size="9.7px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(0, 96), end=(560, 96), stroke='black', stroke_width="0.2"))

    bottombanner.add(dwg.rect(insert=(0,98), size=(560,15), fill="#4b8ecc"))
    bottombanner.add(dwg.text('GEK Strom Kosten [€/m²]:', insert=(5, 109), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    #winizige Anmerkungen unten links:
    bottombanner.add(dwg.text('Definition Endenergie:', insert=(5, 123), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    bottombanner.add(dwg.text('extern eingekaufte Energie', insert=(140, 123), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.text('Umrechnungsfaktor:', insert=(5, 135), fill='black' , font_size="10px" , font_family="Dejavu Sans"))
    bottombanner.add(dwg.text('1 Liter Öläquivalent (OE) = 10 kWh', insert=(140, 135), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.text('m² ist hier die Energiebezugsfläche wie eingegeben', insert=(5, 147), fill='black' , font_size="10px" , font_family="Dejavu Sans"))

    bottombanner.add(dwg.line(start=(140, 30), end=(140, 113), stroke='black', stroke_width="0.2"))

    data_per_year["Ziel"] = {"strom_allgemein" : 100, "kosten_strom" : 280.0 , "gek_strom_kosten" : 1.4}

    x = 160
    for year in year_val_dict:
        bottombanner.add(dwg.line(start=(x+40, 30), end=(x+40, 113), stroke='black', stroke_width="0.2"))
        bottombanner.add(dwg.text(year, insert=(x+10, 40), fill='black' , font_size="7px" , font_family="Dejavu Sans", text_anchor="middle"))

        bottombanner.add(dwg.text(fstr(data_per_year[year]["strom_allgemein"]), insert=(x + 35, 56), fill='black' , font_size="10px" , font_family="Dejavu Sans" , text_anchor="end"))

        bottombanner.add(dwg.text(fstr(year_val_dict[year]), insert=(x + 35, 73), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        bottombanner.add(dwg.text(str(int(data_per_year[year]["kosten_strom"])), insert=(x + 35, 90), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))
        bottombanner.add(dwg.text(fstr(data_per_year[year]["gek_strom_kosten"]), insert=(x + 35, 109), fill='black' , font_size="10px" , font_family="Dejavu Sans", text_anchor="end"))

        x += 60


    dwg.add(bottombanner)

    #--------- ende bottom banner

    dwg.add(dwg.rect(insert=(0,0) , size=(560,540) , fill_opacity="0.0" , stroke="black" , stroke_width="1"))

    return dwg.tostring()


# data_per_year = {
#     "2017": {"strom_allgemein" : 346, "kosten_strom" : 968.0 , "gek_strom_kosten" : 4.84},
#     "2018": {"strom_allgemein" : 346, "kosten_strom" : 968.0 , "gek_strom_kosten" : 4.84},
#     "2019": {"strom_allgemein" : 418, "kosten_strom" : 1169.47 , "gek_strom_kosten" : 5.85},
#     "2020": {"strom_allgemein" : 442, "kosten_strom" : 1154.65 , "gek_strom_kosten" : 5.77},
#     "2021": {"strom_allgemein" : 392, "kosten_strom" : 1000 , "gek_strom_kosten" : 4.93},
#     "2022": {"strom_allgemein" : 380, "kosten_strom" : 970 , "gek_strom_kosten" : 4.99},
# }

# drawGEKStromDiagram({"gebaeudeart":"Zweifamilienhaus", "baujahr" : 2000 , "street" : "An der Dörrwies" , "number" : 20, "plz" : 55218, "city" : "Ingelheim" , "owner" : "Martina Löpfe", "energiebezugsflaeche" : 200,
#  "heizwaerme" : "Öl" , "warmwasser" : "Öl"},{"2017" : 1.7, "2018" : 1.7, "2019" : 2.1 ,"2020" : 2.2, "2021": 2.3, "2022": 2.5}, data_per_year) 