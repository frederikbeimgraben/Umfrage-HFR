import { Survey } from 'survey-react-ui';
import { SurveyConfig, CalcScores } from "./SurveyConfig";
import { Model, Question, ValidateQuestionEvent, CurrentPageChangingEvent } from 'survey-core';
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

const surveyJson: JSON = SurveyConfig();

export function GetSurvey(): Model {
    const survey = new Model(surveyJson);
    survey.locale = "de";
    var hasErrors = false;
    var target: Question;

    // Check if matrix questions are fully answered
    const validateColumns = (sender: Model, options: ValidateQuestionEvent) => {
        if (options.name.includes("_matrix")) {
            const question = options.question;
            const rows = question.rows;
            // const columns = question.columns;
            const answers = question.value;
            const missing = rows.filter((row: any) => {
                return !answers[row.value];
            });

            target = options.question;

            if (missing.length > 0) {
                hasErrors = true;
            } else {
                hasErrors = false;
            }
        }
    };

    const validatePage = (sender: Model, options: CurrentPageChangingEvent) => {
        console.log(target);
        if (hasErrors) {
            // Show error on target question
            target.addError("Bitte beantworten Sie alle Fragen.");
            // Scroll to target question
            target.scrollIntoView();

            // Prevent page change
            options.allowChanging = false;
        } else {
            // Allow page change
            options.allowChanging = true;
        }
    };

    // Validate upon pressing next button
    survey.onValidateQuestion.add(validateColumns);

    survey.onCurrentPageChanging.add(validatePage);

    return survey;
}

const survey = GetSurvey();

class SurveyComponent extends React.Component {
    state: { isCompleted: boolean; };

    constructor(props: any) {
      super(props);
      this.state = { isCompleted: false };
      this.onCompleteComponent = this.onCompleteComponent.bind(this);
    }

    onCompleteComponent() {
      this.setState({ isCompleted: true });
    }

    renderResults(survey: Model) {
        const scores = CalcScores(survey.data);
        console.log(scores);
    
        const pacht = scores["pacht"];
        const regie = scores["regie"];
    
        const pacht_percent = Math.round(pacht / (pacht + regie) * 100);
        const regie_percent = Math.round(regie / (pacht + regie) * 100);
        
        // The bars and labels should be placed on top of each other
        const survey_complete_bars = (
            <div id="survey-complete-bars-layer" className="survey-complete-bars survey-complete-layers">
                <div className="survey-complete-bar-container">
                    <div className="survey-complete-bar survey-complete-graph-bar-pacht" style={{ width: pacht_percent + "%" }}></div>
                    <div className="survey-complete-bar survey-complete-graph-bar-regie" style={{ width: regie_percent + "%" }}></div>
                </div>
            </div>
        )

        // Labels are placed on opposite sides of the bar
        const survey_complete_labels = (
            <div id="survey-complete-labels-layer" className="survey-complete-labels survey-complete-layers">
                <div className="survey-complete-label-container">
                    <div className="survey-complete-label survey-complete-label-pacht">Pacht</div>
                    <div className="survey-complete-label survey-complete-label-regie">Regie</div>
                </div>
            </div>
        )

        const betterOption = pacht > regie ? "Pacht" : "Regie";

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
                        Basierend auf Ihren Antworten ist <b>{betterOption}jagd</b> die bessere Option für ihr Revier.
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
    survey.onComplete.add((sender, options) => {
        console.log(JSON.stringify(sender.data, null, 3));
    });

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