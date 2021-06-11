import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    menuState: false
};

export const commonSlice = createSlice({
    name: 'common',
    initialState,
    reducers: {
        showMenu: (state) => {
            state.menuState = true
        },
        closeMenu: (state) => {
            state.menuState = false
        }
    }
});

export const { showMenu, closeMenu } = commonSlice.actions;

export const selectMenuState = (state) => state.common.menuState;

export default commonSlice.reducer;