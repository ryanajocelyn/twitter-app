import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import commonReducer from './components/common/commonSlice';
import timelineReducer from '../features/timeline/tweetTimelineSlice';
import authReducer from '../features/auth/authSlice';

export const store = configureStore({
    reducer: {
        counter: counterReducer,
        common: commonReducer,
        timeline: timelineReducer,
        auth: authReducer
    },
});
