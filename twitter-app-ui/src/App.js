import React from 'react';
import './App.css';
import HeaderAppBar from './app/components/common/headerAppBar';
import { TweetTimeline } from './features/timeline/TweetTimeline';

function App() {
  return (
    <div className="App">
      <HeaderAppBar />

      <TweetTimeline />      
    </div>
  );
}

export default App;
