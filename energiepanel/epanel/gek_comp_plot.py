
from typing import get_type_hints
from epanel.models import ResultCache

import matplotlib
import matplotlib.pyplot as plt, mpld3
from matplotlib.path import Path
import numpy as np
import io
import base64

matplotlib.use('Agg')


def generateComparisonPlot(year_from, year_to, highlight_user, export_image=False , doplot=0):
    result = ResultCache.objects.filter(jahr__gte=year_from, jahr__lte=year_to)
    usersid = result.values_list('user', flat = True).distinct()
    
    values = {} #Maps userid to a list of (gek_total, gek_waerme, gek_strom, ebf and counter)
    #counter is used to filter out users that didnt provide all years in range

    for set in result:
        id = set.user
        if not id in values:
            values[id] = [0,0,0,set.ebf,0,set.bauart]
        values[id][0] += set.gek_total
        values[id][1] += set.gek_waerme
        values[id][2] += set.gek_strom
        values[id][4] += 1
    
    #Filter out user with no data
    for id in values.copy():
        if (values[id][4] < year_to-year_from):
            del values[id]

    fig, ax = plt.subplots(figsize=(6,4))

    gek_total = []
    gek_ebf = []
    gek_waerme = []
    gek_strom = []

    bauart_freistehend = []
    bauart_freistehend_ebf = []
    bauart_reihenhaus = []
    bauart_reihenhaus_ebf = []
    bauart_eckhaus = []
    bauart_eckhaus_ebf = []

    local_total = 0
    local_waerme = 0
    local_strom = 0
    local_ebf = 0
    local_bauart = ""
    plot_user = False

    for id in values:
        if id == highlight_user:
            local_total = values[id][0]/values[id][4]
            local_waerme = values[id][1]/values[id][4]
            local_strom = values[id][2]/values[id][4]
            local_ebf = values[id][3]
            local_bauart = values[id][5]
            plot_user = True
        gek_total.append(values[id][0]/values[id][4])
        gek_waerme.append(values[id][1]/values[id][4])
        gek_strom.append(values[id][2]/values[id][4])
        gek_ebf.append(values[id][3])
        if values[id][5] == "FREISTEHEND":
            if doplot == 0 or doplot == 1: bauart_freistehend.append(values[id][0]/values[id][4])
            if doplot == 0 or doplot == 2: bauart_freistehend.append(values[id][1]/values[id][4])
            if doplot == 0 or doplot == 3: bauart_freistehend.append(values[id][2]/values[id][4])
            if doplot == 0 or doplot == 1: bauart_freistehend_ebf.append(values[id][3])
            if doplot == 0 or doplot == 2: bauart_freistehend_ebf.append(values[id][3])
            if doplot == 0 or doplot == 3: bauart_freistehend_ebf.append(values[id][3])
        elif values[id][5] == "REIHENHAUS":
            if doplot == 0 or doplot == 1: bauart_reihenhaus.append(values[id][0]/values[id][4])
            if doplot == 0 or doplot == 2: bauart_reihenhaus.append(values[id][1]/values[id][4])
            if doplot == 0 or doplot == 3: bauart_reihenhaus.append(values[id][2]/values[id][4])
            if doplot == 0 or doplot == 1: bauart_reihenhaus_ebf.append(values[id][3])
            if doplot == 0 or doplot == 2: bauart_reihenhaus_ebf.append(values[id][3])
            if doplot == 0 or doplot == 3: bauart_reihenhaus_ebf.append(values[id][3])
        elif values[id][5] == "ECKHAUS":
            if doplot == 0 or doplot == 1: bauart_eckhaus.append(values[id][0]/values[id][4])
            if doplot == 0 or doplot == 2: bauart_eckhaus.append(values[id][1]/values[id][4])
            if doplot == 0 or doplot == 3: bauart_eckhaus.append(values[id][2]/values[id][4])
            if doplot == 0 or doplot == 1: bauart_eckhaus_ebf.append(values[id][3])
            if doplot == 0 or doplot == 2: bauart_eckhaus_ebf.append(values[id][3])
            if doplot == 0 or doplot == 3: bauart_eckhaus_ebf.append(values[id][3])

    #plot bauart
    b1 = ax.plot(bauart_freistehend_ebf, bauart_freistehend , marker=getSymbolFreistehend() ,  color='black', markerfacecolor="None", label='Freistehend' , markersize=9 , linestyle='None')
    b2 = ax.plot(bauart_reihenhaus_ebf, bauart_reihenhaus , marker=getSymbolReihenhaus() , color='black', markerfacecolor=None , label='Reihenhaus' , markersize=9 , linestyle='None')
    b3 = ax.plot(bauart_eckhaus_ebf, bauart_eckhaus , marker=getSymbolEckhaus() , color='black', markerfacecolor=None , label='Eckhaus' , markersize=9 , linestyle='None')

    p1,p2,p3 = None, None, None

    if doplot == 0 or doplot == 1: p1 = ax.plot(gek_ebf, gek_total , 'o' , color='gray' , label='E-Total')
    if doplot == 0 or doplot == 2: p2 = ax.plot(gek_ebf, gek_waerme , 'o' , color='red' , label='E-Wärme')
    if doplot == 0 or doplot == 3: p3 = ax.plot(gek_ebf, gek_strom , 'o' , color='blue' , label='E-Strom')

    #plot local values
    if plot_user:
        if doplot == 0 or doplot == 1: ax.plot(local_ebf, local_total , 'o' , color='black' , markerfacecolor='gray', markersize=12)
        if doplot == 0 or doplot == 2: ax.plot(local_ebf, local_waerme , 'o' , color='black' , markerfacecolor='red', markersize=12)
        if doplot == 0 or doplot == 3: ax.plot(local_ebf, local_strom , 'o' , color='black' , markerfacecolor='blue', markersize=12)

        if doplot == 0 or doplot == 1: ax.plot(local_ebf, local_total , marker=getSymbol(local_bauart) , color='black' , markerfacecolor='gray', markersize=15)
        if doplot == 0 or doplot == 2: ax.plot(local_ebf, local_waerme , marker=getSymbol(local_bauart) , color='black' , markerfacecolor='red', markersize=15)
        if doplot == 0 or doplot == 3: ax.plot(local_ebf, local_strom , marker=getSymbol(local_bauart) , color='black' , markerfacecolor='blue', markersize=15)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    handles = [b1[0], b2[0], b3[0]]
    if p1 != None: handles.append(p1[0])
    if p2 != None: handles.append(p2[0])
    if p3 != None: handles.append(p3[0])

    lgd = ax.legend(handles=None, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax.set_ylabel('GEK Liter Öl-Äquivalent')
    ax.set_xlabel('Energiebedarfsfläche in m²')

    typestr = ""
    if doplot == 1: typestr = " (E-Total)"
    if doplot == 2: typestr = " (E-Wärme)"
    if doplot == 3: typestr = " (E-Strom)"

    ax.set_title('Gebäudekennziffern ø '+str(year_from)+' bis ' +str(year_to) + typestr)

    if export_image:
        #Save to "fake" file
        f = io.BytesIO()
        fig.savefig(f,  bbox_extra_artists=(lgd,), bbox_inches='tight', format = "png")
        f.seek(0)
        return f

    #return '<img align="left" src="data:image/png;base64,%s">' % pic_hash
    return mpld3.fig_to_html(fig)

def getSymbol(bauart):
    if bauart == "FREISTEHEND":
        return getSymbolFreistehend()
    elif bauart == "ECKHAUS":
        return getSymbolEckhaus()
    elif bauart == "REIHENHAUS":
        return getSymbolReihenhaus()

def getSymbolFreistehend():
    verts = [
        (1., 1.),
        (1., -1.),
        (1., -1.), 

        (1., -1.),
        (-1., -1.), 
        (-1., -1.),

        (-1., -1.),
        (-1., 1.), 
        (-1., 1.),

        (-1., 1.),
        (1., 1.), 
        (1., 1.),
    ]

    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CLOSEPOLY,

        Path.MOVETO,
        Path.LINETO,
        Path.CLOSEPOLY,

        Path.MOVETO,
        Path.LINETO,
        Path.CLOSEPOLY,

        Path.MOVETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]

    return Path(verts, codes)
    #return "s"

def getSymbolEckhaus():
    verts = [
        (1., 1.),  # left, bottom
        (1., -1.),  # left, top
        (1., -1.),  # left, top
        (1., -1.),  # left, top
        (-1., -1.),  # right, top
        (-1., 1.),  # right, bottom
        (1., 1.),  # ignored
        (-1., 1.),  # ignored
        (-1., 1.),  # ignored
    ]

    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CLOSEPOLY,
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]

    return Path(verts, codes)

def getSymbolReihenhaus():
    verts = [
        (1., 1.),  # left, bottom
        (1., -1.),  # left, top
        (-1., -1.),  # right, top
        (-1., 1.),  # right, bottom
        (1., 1.),  # ignored
    ]

    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]

    return Path(verts, codes)