import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { fetchTimeline, syncTimeline } from './tweetTimelineAPI';

const initialState = {
  timeline: [],
  status: 'idle',
  syncStatus: 'idle',
};

export const fetchTimelineAsync = createAsyncThunk(
  'timeline/fetchTimeline',
  async (criteria) => {
    const response = await fetchTimeline(criteria);

    // The value we return becomes the `fulfilled` action payload
    return response.data;
  }
);

export const syncTimelineAsync = createAsyncThunk(
  'timeline/syncTimeline',
  async (userId) => {
    const response = await syncTimeline(userId);

    // The value we return becomes the `fulfilled` action payload
    return response.data;
  }
);

export const timelineSlice = createSlice({
  name: 'timeline',
  initialState,
  reducers: {
    storeSortedTimeline: (state, action) => {
      state.timeline = action.payload
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTimelineAsync.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTimelineAsync.fulfilled, (state, action) => {
        state.status = 'idle';
        state.timeline = action.payload;
      })
      .addCase(syncTimelineAsync.pending, (state) => {
        state.syncStatus = 'loading';
      })
      .addCase(syncTimelineAsync.fulfilled, (state, action) => {
        state.syncStatus = 'idle';
        state.timeline = action.payload;
      });
  },
});

export const { storeSortedTimeline } = timelineSlice.actions;

export const selectTimeline = (state) => state.timeline.timeline;

export default timelineSlice.reducer;
