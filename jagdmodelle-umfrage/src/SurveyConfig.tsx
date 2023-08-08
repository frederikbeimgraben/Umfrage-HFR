const default_selector = [
    {
        "value": "disagree",
        "text": "Stimme nicht zu"
    },
    {
        "value": "neutral",
        "text": "Neutral"
    },
    {
        "value": "agree",
        "text": "Stimme zu"
    },
    {
        'value': 'not_applicable',
        'text': 'Überspringen'
    }
]

function row(index: number, text: string): any {
    return {
        "value": index,
        "text": text,
        "isRequired": true,
    }
}

let ALL: any[string] = [];

function default_matrix(id: string, rows: string[], title: string): any {
    let sid: string = id + "_matrix";
    ALL[sid] = rows;

    return {
        "type": "matrix",
        "name": id + "_matrix",
        "title": title,
        "columns": default_selector,
        "rows": [ // Iterate over rows with row(index, text)
            ...rows.map((text, index) => row(index, text))
        ],
        "isRequired": true
    }
}

function default_matrix_page(id: string, title: string, mat_title: string, questions: string[]): any {
    return {
        "name": id,
        "elements": [
            default_matrix(id, questions, mat_title)
        ],
        "title": title
    }
}

function radio_page(id: string, title: string, question: string, choices: string[]): any {
    let sid: string = id + "_radio";
    ALL[sid] = choices;
    
    return {
        "name": id,
        "elements": [
            {
                "type": "radiogroup",
                "name": id + "_radio",
                "title": question,
                "valueName": id + "_radio",
                "clearIfInvisible": "none",
                "choices": choices,
                "isRequired": true,
            }
        ],
        "title": title
    }
}

const json_data = {
    "title": "Jagdmodelle Rechner",
    "checkErrorsMode": "onValueChanged",
    "pages": [
        radio_page(
            "model_1",
            "", // "Aktuelles Modell",
            "Welches Bejagungsmodell wenden sie aktuell an?",
            [
                "Pachtjagd",
                "Eigenbewirtschaftung (Regiejagd)",
                "Sonstige"
            ]
        ),
        default_matrix_page(
            "finance",
            "", // "Finanzielle Situation der Gemeinde",
            "Bitte bewerten Sie die folgenden Aussagen:",
            [ // \[[0-9]+[.:]*[0-9]+\]
                "Die finanzielle Gesamtsituation der Kommune ist angespannt.",
                "Die Jagdpacht spielt als konstante Einnahmequelle innerhalb des Haushalts eine wichtige Rolle.",
                "Aufgrund der Kosten, die das Wild  durch notwendige Schutzmaßnahmen (z.B.: Wuchshüllen, Zaun) verursacht, übersteigen die Ausgaben für die Jagd die Einnahmen aus der Jagdpacht deutlich. ",
                "Der Organisationsaufwand und die Verwaltungskosten für unsere Jagdgenossenschaft/Kommune sollen im Bereich der Bejagung so gering wie möglich gehalten werden.",
                "In den nächsten fünf Jahren können vorhandene finanzielle Mittel in die jagdliche Neuorganisation investiert werden. Aber nur, wenn dadurch langfristig Geld eingespart werden kann. Z.B.: aufgrund verringerter Kosten für Schutzmaßnahmen (z.B.: Wuchshüllen, Zaun) oder Pflanzungen. ",
                "Die derzeitigen Pächter spielen beispielsweise durch Gewerbesteuerzahlungen, Finanzierung von Vereinen oder Spenden auch abseits der Jagd eine wichtige Rolle für die Gemeinde. "
            ]
        ),
        radio_page(
            "area_share",
            "", // "Jagdstruktur",
            "Je höher der Feldanteil, desto höher die Wildschadensersatzforderung. Daraus resultieren auch höhere Kosten für die Kommune/Jagdgenossenschaft. Wie hoch ist der Feldanteil in Ihrem gemeinschaftlichen Jagdbezirk?",
            [
                "<25%",
                "25-50%",
                "50-75%",
                ">75%",
                "Überspringen"
            ]
        ),
        default_matrix_page(
            "structure",
            "", // "Jagdstruktur",
            "Bitte bewerten Sie die folgenden Aussagen:",
            [
                "Nehmen wir an die Kommune hätte den Wunsch den gemeinschaftlichen Jagdbezirk durch Eigenbewirtschaftung zu bejagen. Hielten sie es für realistisch, dass die Kommune Ihren Willen in der Jagdgenossenschaft derzeit gegen etwaige Widerstände durchsetzen könnte?",
                "Als Grundeigentümer bin ich bereit Organisationsaufwand und Kosten für die jagdliche Neuorganisation zu übernehmen, möchte im Gegenzug jedoch auch ein direktes Mitbestimmungsrecht, was die Jagdausübung angeht. Damit ist z.B. die Ausführung von Bewegungsjagden gemeint.",
                "Die Kommune/Jagdgenossenschaft hat an der Vermarktung von Wildbret Interesse. Sie möchte der Bevölkerung ein hochwertiges Nahrungsmittel aus dem eigenen Wald zur Verfügung stellen. Deshalb ist sie bereit, die Kosten für Kühlung, ggf. anfallende Weiterverarbeitung und Vertrieb vorzufinanzieren.",
                "Die Kommune/Jagdgenossenschaft möchte so vielen ortsansässigen Jägern wie möglich eine Jagdmöglichkeit in ihrem gemeinschaftlichen Jagdbezirk bieten.",
                "Das aktuelle Verhältnis zwischen Grundeigentümern und Jägern ist gut. Der Grund dafür ist, dass sich die Jäger als Dienstleister der Grundeigentümer verstehen und Ihre Jagd regelmäßig anhand von Vorgaben bzw. Forderungen dieser anpassen.",
                "Neuverpachtung stellt kein Problem dar. Es sind stehts mehr als genug Interessenten vorhanden.",
                "Für eine Eigenbewirtschaftung sind genügend interessierte Jäger vorhanden. Erkennbar ist dies daran, dass ausreichend Anfragen für Jagderlaubnisscheine vorhanden sind. Zusätzlich besteht eine gute Anbindung an Verkehrswegen und/oder Ballungszentren.",
                "Es gäbe eine Person/Personen (z.B.: Forstbedienstete, Forstwirte, o.ä.) die sowohl jagdfachlich als auch zeitlich in der Lage ist/sind die Gesamtorganisation einer Eigenbewirtschaftung zu übernehmen.",
                "Die bisherigen Pächter spielen beispielsweise durch Ehrenämter, Wohnraumvermietung oder Arbeitsplätze auch abseits der Jagd eine wichtige Rolle."
            ]
        ),
        radio_page(
            "model_2",
            "", // "Jagdstruktur",
            "Wählen Sie zwischen den Vorteilen! Die Pacht bietet den Vorteil, dass die Jagdpächter durch die lange Bindung viel ins eigene Revier und damit in den gemeinchaftlichen Jagdbezirk investieren. Die Eigenbewirtschaftung ist aufgrund der kurzen Bindung deutlich flexibler.",
            [
                "Pachtjagd",
                "Eigenbewirtschaftung (Regiejagd)",
                "Überspringen"
            ]
        ),
        // Schäden
        radio_page(
            "damages_hba",
            "", // "Wildschaden in Wald/Feld",
            "Alle Hauptbaumarten können von Natur aus und ohne Schutzmaßnahmen (z.B. Wuchshüllen, Zäune) einen Wald bilden. Dass liegt an der guten Bejagung durch die aktuellen Jäger.",
            [
                "Stimme zu",
                "Stimme teilweise zu",
                "Stimme teilweise nicht zu",
                "Stimme nicht zu",
                "Überspringen"
            ]
        ),
        radio_page(
            "damages_fsc",
            "", // "Wildschaden in Wald/Feld",
            "Bei den FSC oder PEFC zertifizierten Flächen gibt es keine Beanstandungen wegen Wildschäden durch den Zertifizierer. Dies ist der guten Bejagung zu verdanken.",
            [
                "Stimme zu",
                "Neutral",
                "Stimme nicht zu",
                "Überspringen"
            ]
        ),
        radio_page(
            "damages_smk",
            "", // "Wildschaden in Wald/Feld",
            "Schutzmaßnahmen (z.B.: Wuchshüllen, Zäune) sind der größte Kostenfaktor bei Pflanzungen. Pflanzungen sowie verbissintensive Naturverjüngung (Eiche und Tanne) müssen in unserem gemeinschaftlichen Jagdbezirk in mehr als 50% der Fälle gegen Wildschaden geschützt werden.",
            [
                "Stimme zu",
                "Stimme teilweise zu",
                "Stimme teilweise nicht zu",
                "Stimme nicht zu",
                "Überspringen"
            ]
        ),
        radio_page(
            "damages_smw",
            "", // "Wildschaden in Wald/Feld",
            "Die von Jägern getroffenen Schutzmaßnahmen (z.B.: Wuchshüllen, Zäune, gute Bejagung) gegen Wildschaden sind wirkungsvoll.",
            [
                "Stimme zu",
                "Stimme teilweise zu",
                "Stimme teilweise nicht zu",
                "Stimme nicht zu",
                "Überspringen"
            ]
        ),
        radio_page(
            "damages_jkl",
            "", // "Wildschaden in Wald/Feld",
            "Durch die gute Bejagung gibt es kein Problem mit Wildschäden auf landwirtschaftlichen Flächen.",
            [
                "Stimme zu",
                "Stimme teilweise zu",
                "Stimme teilweise nicht zu",
                "Stimme nicht zu",
                "Überspringen"
            ]
        ),
        radio_page(
            "damages_jkp",
            "", // "Wildschaden in Wald/Feld",
            "Durch die gute Bejagung gibt es kein Problem mit Wildschäden auf Flächen wie z.B. Hausgärten, Friedhöfen oder Spielplätzen.",
            [
                "Stimme zu",
                "Stimme teilweise zu",
                "Stimme teilweise nicht zu",
                "Stimme nicht zu",
                "Überspringen"
            ]
        ),
        // Dritte
        radio_page(
            "model_3",
            "", // "Verhältnis Jagende und Dritte",
            "In einer Eigenbewirtschaftung existiert eine zentrale Ansprechperson für Probleme mit Erholungssuchenden (z.B.: Radfahrern, Wanderern usw.) oder anderen Interessengruppen (z.B.: Forstbediensteten, Anwohnern, Naturschützern usw.). Bei der Pacht existiert in jedem Jagdrevier (mehrere Reviere) eine Ansprechperson. Wählen  sie zwischen den beiden Modellen!",
            [
                "Pachtjagd",
                "Eigenbewirtschaftung (Regiejagd)",
                "Überspringen"
            ]
        ),
        default_matrix_page(
            "relations",
            "", // "Verhältnis Jagende und Dritte",
            "Bitte bewerten Sie die folgenden Aussagen:",
            [
                "Die Grundeigentümer sollten die Möglichkeit zur aktiven Regulierung des Wildschadens durch Eingriff in den Jagdbetrieb haben (einmal jährlich, zum 01.04.), auch wenn dies mit einer deutlichen Erhöhung  (z.B.: einer Verdoppelung bis Vervierfachung) des Abschusses einhergeht.",
                "Hätten Sie als Kommune/Jagdgenossenschaft gerne die Möglichkeit, das Jagdausübungsrecht aus triftigen Gründen kurzfristig (jährlich zum 01.04) neu zu vergeben?",
                "Aktuell sind im Pachtvertrag Ausstiegsklauseln für Pächter vorhanden. Diese ermöglichen es z.B. bei einem ASP-Ausbruch oder hohen Wildschadenskosten aus dem Vertrag auszusteigen. Dies ist von Seiten der Kommune/Jagdgenossenschaft nicht erwünscht."
            ]
        )
    ],
    "parse": function(text: string, errors: any) {
        return JSON.parse(text);
    },
    "stringify": function(json: JSON, replacer: any, space: any) {
        return JSON.stringify(json, replacer, space);
    },
    [Symbol.toStringTag]: "SurveyJSON",
}

function simple(pa: number, re: number): any {
    return {
        'p': {
            'p': pa,
            'r': pa
        },
        'r': {
            'p': re,
            'r': re
        }
    }
}

function mix_rp(pa: any, re: any): any {
    return {
        'p': {
            'p': pa['p']['p'],
            'r': re['p']['r']
        },
        'r': {
            'p': pa['r']['p'],
            'r': re['r']['r']
        }
    }
}

function intertwine(a: any[], b: any[]): any[] {
    // Intertwine pacht and regie
    const result: any[] = [];
    for (let i = 0; i < a.length; i++) {
        result.push(
            mix_rp(a[i], b[i])
        );
    }
    return result;
}


const pacht_simple: any = [
    simple(2, 0),
    simple(1, 1),
    simple(0, 2),
    simple(0, 0)
]

const regie_simple: any = [
    simple(0, 2),
    simple(1, 1),
    simple(2, 0),
    simple(0, 0)
]

const pacht_regie_simple: any = intertwine(
    pacht_simple,
    regie_simple
)

const regie_pacht_simple: any = intertwine(
    regie_simple,
    pacht_simple
)

const pacht_regie_complex: any = intertwine(
    [
        simple(3, 0),
        simple(2, 1),
        simple(1, 2),
        simple(0, 3),
        simple(0, 0)
    ],
    [
        simple(0, 3),
        simple(1, 2),
        simple(2, 1),
        simple(3, 0),
        simple(0, 0)
    ]
)

const regie_pacht_complex: any = intertwine(
    [
        simple(0, 3),
        simple(1, 2),
        simple(2, 1),
        simple(3, 0),
        simple(0, 0)
    ],
    [
        simple(3, 0),
        simple(2, 1),
        simple(1, 2),
        simple(0, 3),
        simple(0, 0)
    ]
)

const scores = {
    "model_1_radio": [ // 1: Pacht, Eigenbewirtschaftung, Sonstige
        [    
            simple(0, 0),
            simple(0, 0),
            simple(0, 0)
        ]
    ],
    "finance_matrix": [ // Rows
        // agree; neutral; disagree; not_applicable
        pacht_simple, // 2
        pacht_simple, // 3
        regie_simple, // 4
        pacht_simple, // 5
        regie_simple, // 6
        pacht_simple  // 7
    ],
    "area_share_radio": [ // 8: <25%, 25-50%, 50-75%, >75%, Überspringen
        [
            simple(3, 0),
            simple(2, 1),
            simple(1, 2),
            simple(0, 3),
            simple(0, 0)
        ]
    ],
    "structure_matrix": [ // Rows
        // agree; neutral; disagree; not_applicable
        regie_simple, // 9
        regie_simple, // 10
        regie_simple, // 11
        regie_simple, // 12
        intertwine(
            pacht_simple, // 13
            regie_simple
        ),
        pacht_simple, // 14
        regie_simple, // 15
        regie_simple, // 16
        pacht_simple  // 17
    ],
    "model_2_radio": [ // 18: Pacht, Eigenbewirtschaftung, Überspringen
        [
            simple(1, 0),
            simple(0, 1),
            simple(0, 0)
        ]
    ],
    // Schäden
    "damages_hba_radio": [ // 19: Stimme nicht zu, Stimme teilweise nicht zu, Stimme teilweise zu, Stimme zu, Überspringen
        pacht_regie_complex
    ],
    "damages_fsc_radio": [ // 20: Stimme nicht zu, Neutral, Stimme zu, Überspringen
        pacht_regie_simple
    ],
    "damages_smk_radio": [ // 21: Stimme nicht zu, Stimme teilweise nicht zu, Stimme teilweise zu, Stimme zu, Überspringen
        regie_pacht_complex
    ],
    "damages_smw_radio": [ // 22: Stimme nicht zu, Stimme teilweise nicht zu, Stimme teilweise zu, Stimme zu, Überspringen
        pacht_regie_complex
    ],
    "damages_jkl_radio": [ // 23: Stimme nicht zu, Stimme teilweise nicht zu, Stimme teilweise zu, Stimme zu, Überspringen
        pacht_regie_complex
    ],
    "damages_jkp_radio": [ // 24: Stimme nicht zu, Stimme teilweise nicht zu, Stimme teilweise zu, Stimme zu, Überspringen
        pacht_regie_complex
    ],
    // Dritte
    "model_3_radio": [ // 25: Pacht, Eigenbewirtschaftung, Überspringen
        [
            simple(1, 0),
            simple(0, 1),
            simple(0, 0)
        ]
    ],
    "relations_matrix": [ // Rows
        // agree; neutral; disagree; not_applicable
        regie_simple, // 26
        regie_simple, // 27
        regie_simple  // 28
    ]
}

function matrixIndex(text: string): number {
    switch (text) {
        case "disagree":
            return 0;
        case "neutral":
            return 1;
        case "agree":
            return 2;
        case "not_applicable":
            return 3;
        default:
            return 3;
    }
}


export function CalcScores(json: any): any {
    let score_pj: number = 0;
    let score_eb: number = 0;

    // json["model_1_radio"];
    // Wen pachtjagd, dann let sel = p, sonst r
    let sel;
    if (json["model_1_radio"] === "Pachtjagd") {
        sel = 'p';
    } else {
        sel = 'r';
    }

    // Iterate over all questions
    for (const [key, value] of Object.entries(scores)) {
        const response = json[key];
        // If the key ends with _radio, special case
        if (key.endsWith("_radio")) {
            // index of answer in options
            const index = ALL[key].indexOf(response);
            const cell = value[0][index];
            console.log(cell);
            score_pj += cell['p'][sel];
            score_eb += cell['r'][sel];
        } else {
            for (let i = 0; i < value.length; i++) {
                const row = value[i];
                const cell = row[matrixIndex(response[i])];
                console.log(cell);
                score_pj += cell['p'][sel];
                score_eb += cell['r'][sel];
            }
        }
    }

    return {
        'pacht': score_pj,
        'regie': score_eb
    }
}

export function SurveyConfig(): JSON {
    return json_data as JSON;
}

export default SurveyConfig;