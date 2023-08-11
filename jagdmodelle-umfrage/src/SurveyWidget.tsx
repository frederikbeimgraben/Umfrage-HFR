import { Survey } from 'survey-react-ui';
import { Model } from 'survey-core';
import React from 'react';

import 'survey-core/modern.min.css';
import './SurveyWidget.css';
import "survey-core/survey.i18n";

// Set main color
import { StylesManager } from 'survey-core';
StylesManager.applyTheme("modern");
// Main color should be rgb(24, 127, 44)
StylesManager.ThemeColors["modern"] = {
    "$main-color": "#187f2c"
};

const apiServer = "http://api.beimgraben.net";
const apiEndpoint = "/api/surveys/default";
const evaluationEndpoint = "/api/surveys/default/eval";
const referralCode = "123456";

export function GetSurvey(): Model {
    // Retrieve survey from server
    const request = new XMLHttpRequest();
    request.open("GET", apiServer + apiEndpoint, false);
    request.send(null);

    if (request.status === 200) {
        const survey = JSON.parse(request.responseText);
        survey.locale = "de";
        return new Model(survey);
    }

    throw new Error("Could not retrieve survey from server");
}

const survey = GetSurvey();

class SurveyComponent extends React.Component {
    state: { isCompleted: boolean };

    constructor(props: any) {
      super(props);
      this.state = { isCompleted: false };
      this.onCompleteComponent = this.onCompleteComponent.bind(this);
    }

    onCompleteComponent() {
      this.setState({ isCompleted: true });
    }

    renderResults(survey: Model) {
        var data = survey.data;

        const questions = survey.getAllQuestions();
        
        for (var i = 0; i < questions.length; i++) {
            const question = questions[i];

            // Question i corresponds to data['<i>']
            const question_index = i.toString();
            const response = data[question_index];

            // Get index of <response> in question.choices
            const choices = question.choices;
            var response_index = -1;
            for (var j = 0; j < choices.length; j++) {
                if (choices[j].value === response) {
                    response_index = j;
                    break;
                }
            }

            if (response_index === -1) {
                throw new Error("Could not find response in choices");
            }

            // Set data[question_index] to response_index
            data[question_index] = response_index;
        }

        // Send to server
        const request = new XMLHttpRequest();
        request.open("POST", apiServer + evaluationEndpoint, false);
        request.setRequestHeader("Content-Type", "application/json");

        const payload = {
            // Data as list of responses (integer indices)
            "answers": data,
            // Referral code
            "referral_code": referralCode
        };

        request.send(JSON.stringify(payload));

        if (request.status === 200) {
            const response = JSON.parse(request.responseText);
            console.log(response);
        }

        console.log(request.responseText);

        // Parse results
        const results = JSON.parse(request.responseText);

        // Assert that results is a list of at least two elements
        if (!Array.isArray(results) || results.length < 2) {
            throw new Error("Results is not a list of at least two elements");
        }

        // Only keep first two results within List
        results.length = 2;
        
        // The bars and labels should be placed on top of each other
        /* This is obsolete, since the pages, targets (were pacht and regie) and questions are now generated by an API Server
        <div className="survey-complete-bar survey-complete-graph-bar-pacht" style={{ width: pacht_percent + "%", backgroundColor: pacht_color }}></div>
        <div className="survey-complete-bar survey-complete-graph-bar-regie" style={{ width: regie_percent + "%", backgroundColor: regie_color }}></div> */
        const survey_complete_bars = (
            <div id="survey-complete-bars-layer" className="survey-complete-bars survey-complete-layers">
                <div className="survey-complete-bar-container">
                    {
                        results.map((result: any, index: number) => {
                            const percent = result.percent * 100;
                            const winner = result.winner;

                            const color = winner ? "#187f2c" : "#d3d3d3";

                            return (
                                <div className={
                                    "survey-complete-bar survey-complete-graph-bar-" +
                                    (index === 0 ? "left" : "right")
                                } style={{ width: percent + "%", backgroundColor: color }}></div>
                            )
                        })
                    }
                </div>
            </div>
        )

        // Labels are placed on opposite sides of the bar
        /* This is obsolete, since the pages, targets (were pacht and regie) and questions are now generated by an API Server
        <div className="survey-complete-label survey-complete-label-pacht">Pacht</div>
        <div className="survey-complete-label survey-complete-label-regie">Regie</div>
        */
        const survey_complete_labels = (
            <div id="survey-complete-labels-layer" className="survey-complete-labels survey-complete-layers">
                <div className="survey-complete-label-container">
                    {
                        results.map((result: any, index: number) => {
                            const name = result.target;
                            const winner = result.winner;

                            const color = winner ? "rgb(196, 217, 201)" : "#b3b3b3";

                            return (
                                <div className={
                                    "survey-complete-label survey-complete-label-" + 
                                    (index === 0 ? "left" : "right")
                                } style={{ color: color }}>{name}</div>
                            )
                        })
                    }
                </div>
            </div>
        )

        const winner = results[0].winner ? results[0].target : results[1].target;

        // Render opposing bars graph
        return (
            <div className="survey-complete">
                <div className="survey-complete-title sv-question__header sv-question__header--location--top">
                    <h5 id="sq_100_ariaTitle" className="sv-title sv-question__title sv-question__title--required">
                        <span className="sv-string-viewer">Ergebnisse</span>
                    </h5>
                </div>
                <div id="container">
                    {survey_complete_bars}
                    {survey_complete_labels}
                </div>
                <div className="survey-complete-text">
                    <p>
                        Basierend auf ihren Antworten ist <b>{winner}</b> die bessere Option für Sie.
                    </p>
                </div>
            </div>
        )
    }

    render() {
        return !this.state.isCompleted ? (
            <Survey model={survey}
                    showCompletedPage={false}
                    onComplete={this.onCompleteComponent}/>
        ) : (
            this.renderResults(survey)
        );
    }
}

export function RenderExternalProgress() {
    const [pageNo, setPageNo] = React.useState(survey.currentPageNo);
    const [isRunning, setIsRunning] = React.useState(true);
    survey.onCurrentPageChanged.add((_, options) => {
        setPageNo(options.newCurrentPage.visibleIndex);
    });
    survey.onStarted.add(() => { setIsRunning(true); } );
    survey.onComplete.add(() => { setIsRunning(false); });

    const renderExternalNavigation = () => {
        if (!isRunning) return undefined;

        return (
            <div className="navigation-progress-bar">
                <div className="navigation-progress" style={{ width: (pageNo + 1) / survey.visiblePages.length * 100 + "%" }}></div>
            </div>
        );
    };

    return (
        <div className="navigation">
            {renderExternalNavigation()}
        </div>
    )
};

export function SurveyWidget() {
    return (
        <SurveyComponent />
    );
}