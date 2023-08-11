#!/usr/bin/env python3
"""
Generates a JSON file from itself
"""

from typing import Any, Dict, List
import json
import os

try:
    from .tools import *
except ImportError:
    from tools import *

TARGETS = [
    {
        "name": "Regie",
        "states": 3
    },
    {
        "name": "Pacht",
        "states": 3
    }
]

Option = OptionT(TARGETS)

PACHT = "Pachtjagd"
REGIE = "Regiejagd"
SONST = "Sonstige"

JSON = {
    "title": "Jagdmodelle",
    "targets": TARGETS,
    "questions": [
        Question(
            "Welches Bejagungsmodell wenden Sie aktuell an?",
            [
                Option(PACHT, ZERO, [0, 0]),
                Option(REGIE, ZERO, [1, 1]),
                Option(SONST, ZERO, [2, 2])
            ],
            title="Aktuelles Bejagungsmodell"
        ),
        Question(
            "Die finanzielle Gesamtsituation der Kommune ist angespannt.",
            DEFAULT_SET_A,
            title="Finanzielle Situation der Gemeinde"
        ),
        Question(
            "Die Pacht spielt als konstante Einnahmequelle innelb des Haushalts eine wichtige Rolle.",#
            DEFAULT_SET_A,
            title="Finanzielle Situation der Gemeinde"
        ),
        Question(
            "Aufgrund der Kosten, die das Wild  durch notwendige Schutzmaßnahmen (z.B.: Wuchshüllen, Zaun) verursacht, übersteigen die Ausgaben für die Jagd die Einnahmen aus der Jagdpacht deutlich.",
            DEFAULT_SET_B,
            title="Finanzielle Situation der Gemeinde"
        ),
        Question(
            "Der Organisationsaufwand und die Verwaltungskosten für unsere Jagdgenossenschaft/Kommune sollen im Bereich der Bejagung so gering wie möglich gehalten werden.",
            DEFAULT_SET_A,
            title="Finanzielle Situation der Gemeinde"
        ),
        Question(
            "In den nächsten fünf Jahren können vorhandene finanzielle Mittel in die jagdliche Neuorganisation investiert werden. Aber nur, wenn dadurch langfristig Geld eingespart werden kann. Z.B.: aufgrund verringerter Kosten für Schutzmaßnahmen (z.B.: Wuchshüllen, Zaun) oder Pflanzungen.",
            DEFAULT_SET_B,
            title="Finanzielle Situation der Gemeinde"
        ),
        Question(
            "Die derzeitigen Pächter spielen beispielsweise durch Gewerbesteuerzahlungen, Finanzierung von Vereinen oder Spenden auch abseits der Jagd eine wichtige Rolle für die Gemeinde.",
            DEFAULT_SET_A,
            title="Finanzielle Situation der Gemeinde"
        ),
        Question(
            "Je höher der Feldanteil, desto höher die Wildschadensersatzforderung. Daraus resultieren auch höhere Kosten für die Kommune/Jagdgenossenschaft. Wie hoch ist der Feldanteil in Ihrem gemeinschaftlichen Jagdbezirk?",
            [
                Option("<25%",   [3, 0]),
                Option("25-50%", [2, 1]),
                Option("50-75%", [1, 2]),
                Option(">75%",   [0, 3])
            ],
            title="Jagdstruktur"
        ),
        Question(
            "Nehmen wir an die Kommune hätte den Wunsch den gemeinschaftlichen Jagdbezirk durch Eigenbewirtschaftung zu bejagen. Hielten sie es für realistisch, dass die Kommune Ihren Willen in der Jagdgenossenschaft derzeit gegen etwaige Widerstände durchsetzen könnte?",
            [
                Option("Ja",         [0, 2]),
                Option("Nein",       [2, 0]),
                Option("Vielleicht", [1, 1])
            ],
            title="Jagdstruktur"
        ),
        Question(
            "Als Grundeigentümer bin ich bereit Organisationsaufwand und Kosten für die jagdliche Neuorganisation zu übernehmen, möchte im Gegenzug jedoch auch ein direktes Mitbestimmungsrecht, was die Jagdausübung angeht. Damit ist z.B. die Ausführung von Bewegungsjagden gemeint.",
            DEFAULT_SET_B,
            title="Jagdstruktur"
        ),
        Question(
            "Die Kommune/Jagdgenossenschaft hat an der Vermarktung von Wildbret Interesse. Sie möchte der Bevölkerung ein hochwertiges Nahrungsmittel aus dem eigenen Wald zur Verfügung stellen. Deshalb ist sie bereit, die Kosten für Kühlung, ggf. anfallende Weiterverarbeitung und Vertrieb vorzufinanzieren.",
            DEFAULT_SET_B,
            title="Jagdstruktur"
        ),
        Question(
            "Die Kommune/Jagdgenossenschaft möchte so vielen ortsansässigen Jägern wie möglich eine Jagdmöglichkeit in ihrem gemeinschaftlichen Jagdbezirk bieten.",
            DEFAULT_SET_B,
            title="Jagdstruktur"
        ),
        Question(
            "Das aktuelle Verhältnis zwischen Grundeigentümern und Jägern ist gut. Der Grund dafür ist, dass sich die Jäger als Dienstleister der Grundeigentümer verstehen und Ihre Jagd regelmäßig anhand von Vorgaben bzw. Forderungen dieser anpassen.",
            [
                Option(AGREE,    [[2, 0], [0, 2]]),
                Option(DISAGREE, [[0, 2], [2, 0]]),
                Option(NEUTRAL,  [1, 1])
            ],
            title="Jagdstruktur"
        ),
        Question(
            "Neuverpachtung stellt kein Problem dar. Es sind stehts mehr als genug Interessenten vorhanden.",
            DEFAULT_SET_A,
            title="Jagdstruktur"
        ),
        Question(
            "Für eine Eigenbewirtschaftung sind genügend interessierte Jäger vorhanden. Erkennbar ist dies daran, dass ausreichend Anfragen für Jagderlaubnisscheine vorhanden sind. Zusätzlich besteht eine gute Anbindung an Verkehrswegen und/oder Ballungszentren.",
            DEFAULT_SET_B,
            title="Jagdstruktur"
        ),
        Question(
            "Es gäbe eine Person/Personen (z.B.: Forstbedienstete, Forstwirte, o.ä.) die sowohl jagdfachlich als auch zeitlich in der Lage ist/sind die Gesamtorganisation einer Eigenbewirtschaftung zu übernehmen.",
            DEFAULT_SET_B,
            title="Jagdstruktur"
        ),
        Question(
            "Die bisherigen Pächter spielen beispielsweise durch Ehrenämter, Wohnraumvermietung oder Arbeitsplätze auch abseits der Jagd eine wichtige Rolle.",
            DEFAULT_SET_A,
            title="Jagdstruktur"
        ),
        Question(
            "Wählen Sie zwischen den Vorteilen! Die Pacht bietet den Vorteil, dass die Jagdpächter durch die lange Bindung viel ins eigene Revier und damit in den gemeinchaftlichen Jagdbezirk investieren. Die Eigenbewirtschaftung ist aufgrund der kurzen Bindung deutlich flexibler.",
            [
                Option(PACHT, [1, 0]),
                Option(REGIE, [0, 1])
            ],
            title="Jagdstruktur"
        ),
        Question(
            "Alle Hauptbaumarten können von Natur aus und ohne Schutzmaßnahmen (z.B. Wuchshüllen, Zäune) einen Wald bilden. Dass liegt an der guten Bejagung durch die aktuellen Jäger.",
            DEFAULT_2D_APPD_A,
            title="Wildschaden in Wald/Feld"
        ),
        Question(
            "Bei den FSC oder PEFC zertifizierten Flächen gibt es keine Beanstandungen wegen Wildschäden durch den Zertifizierer. Dies ist der guten Bejagung zu verdanken.",
            DEFAULT_2D_APPD_A,
            title="Wildschaden in Wald/Feld"
        ),
        Question(
            "Schutzmaßnahmen (z.B.: Wuchshüllen, Zäune) sind der größte Kostenfaktor bei Pflanzungen. Pflanzungen sowie verbissintensive Naturverjüngung (Eiche und Tanne) müssen in unserem gemeinschaftlichen Jagdbezirk in mehr als 50% der Fälle gegen Wildschaden geschützt werden.",
            DEFAULT_2D_APPD_B,
            title="Wildschaden in Wald/Feld"
        ),
        Question(
            "Die von Jägern getroffenen Schutzmaßnahmen (z.B.: Wuchshüllen, Zäune, gute Bejagung) gegen Wildschaden sind wirkungsvoll.",
            DEFAULT_2D_APPD_A,
            title="Wildschaden in Wald/Feld"
        ),
        Question(
            "Durch die gute Bejagung gibt es kein Problem mit Wildschäden auf landwirtschaftlichen Flächen.",
            DEFAULT_2D_APPD_A,
            title="Wildschaden in Wald/Feld"
        ),
        Question(
            "Durch die gute Bejagung gibt es kein Problem mit Wildschäden auf Flächen wie z.B. Hausgärten, Friedhöfen oder Spielplätzen.",
            DEFAULT_2D_APPD_A,
            title="Wildschaden in Wald/Feld"
        ),
        Question(
            "In einer Eigenbewirtschaftung existiert eine zentrale Ansprechperson für Probleme mit Erholungssuchenden (z.B.: Radfahrern, Wanderern usw.) oder anderen Interessengruppen (z.B.: Forstbediensteten, Anwohnern, Naturschützern usw.). Bei der Pacht existiert in jedem Jagdrevier (mehrere Reviere) eine Ansprechperson. Wählen  sie zwischen den beiden Modellen!",
            [
                Option(PACHT, [1, 0]),
                Option(REGIE, [0, 1])
            ],
            title="Verhältnis Jagende und Dritte"
        ),
        Question(
            "Die Grundeigentümer sollten die Möglichkeit zur aktiven Regulierung des Wildschadens durch Eingriff in den Jagdbetrieb haben (einmal jährlich, zum 01.04.), auch wenn dies mit einer deutlichen Erhöhung (z.B.: einer Verdoppelung bis Vervierfachung) des Abschusses einhergeht.",
            DEFAULT_SET_B,
            title="Verhältnis Jagende und Dritte"
        ),
        Question(
            "Hätten Sie als Kommune/Jagdgenossenschaft gerne die Möglichkeit, das Jagdausübungsrecht aus triftigen Gründen kurzfristig (jährlich zum 01.04) neu zu vergeben?",
            [
                Option("Ja",         [0, 2]),
                Option("Nein",       [2, 0]),
                Option("Vielleicht", [1, 1])
            ],
            title="Verhältnis Jagende und Dritte"
        ),
        Question(
            "Aktuell sind im Pachtvertrag Ausstiegsklauseln für Pächter vorhanden. Diese ermöglichen es z.B. bei einem ASP-Ausbruch oder hohen Wildschadenskosten aus dem Vertrag auszusteigen. Dies ist von Seiten der Kommune/Jagdgenossenschaft nicht erwünscht.",
            DEFAULT_SET_B,
            title="Verhältnis Jagende und Dritte"
        )
    ]
}

# Get base file path and name
base_path = os.path.dirname(__file__)

base_name = os.path.splitext(os.path.basename(__file__))[0]

# Get JSON file name
json_file = os.path.join(base_path, f'{base_name}.json')

# Write JSON to file
with open(json_file, 'w') as f:
    json.dump(JSON, f, indent=4)