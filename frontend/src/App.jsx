import React from 'react';
//import 'antd/dist/antd.css';
import './App.css'; // Импортируем стили
import BettingResultsTable from './BettingResultsTable';

const App = () => (
    <div>
        <h1>Результаты матчей</h1>
        <BettingResultsTable />
    </div>
);

export default App;
