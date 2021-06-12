import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    user: {
        isLoggedIn: false,
        userId: null,
        name: null,
        imageUrl: null,
        status: null,
        url: null
    }
};

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setUserProfile: (state, action) => {
            state.user = { ...state.user, ...action.payload};
        }, 
        clearUserProfile: (state) => {
            state.user =  initialState;
        }
    }
});

export const { setUserProfile, clearUserProfile } = authSlice.actions;

export const selectUser = (state) => state.auth.user;

export default authSlice.reducer;
