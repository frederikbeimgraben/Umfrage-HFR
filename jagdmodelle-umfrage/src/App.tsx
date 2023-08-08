import './App.css';
import { SurveyWidget, RenderExternalProgress } from './SurveyWidget';

function App() {
  return (
    <div className="App">
      <RenderExternalProgress />
      <div className="Pane">
        <SurveyWidget />
      </div>
    </div>
  );
}

export default App;
