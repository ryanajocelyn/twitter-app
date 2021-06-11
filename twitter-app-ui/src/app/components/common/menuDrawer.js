import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import TwitterIcon from '@material-ui/icons/Twitter';
import { closeMenu, selectMenuState, showMenu } from './commonSlice';
import { syncTimelineAsync } from '../../../features/timeline/tweetTimelineSlice';
import { selectUser } from '../../../features/auth/authSlice';

const useStyles = makeStyles({
    list: {
        width: 250,
    },
    fullList: {
        width: 'auto',
    },
});

export default function MenuDrawer(props) {
    const classes = useStyles();
    const dispatch = useDispatch();
    const menuState = useSelector(selectMenuState);
    const user = useSelector(selectUser);

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }

        if (open) {
            dispatch(showMenu());
        } else {
            dispatch(closeMenu());
        }
    };

    const syncTweets = () => {
        dispatch(syncTimelineAsync(user.userId));
    };

    const list = (anchor) => (
        <div
            className={clsx(classes.list)}
            role="presentation"
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
        >
            <List>
                <ListItem button key="SyncTweet" onClick={syncTweets}>
                    <ListItemIcon><TwitterIcon /></ListItemIcon>
                    <ListItemText primary="Sync Tweet" />
                </ListItem>
            </List>
            <Divider />
        </div>
    );

    return (
        <div>
            <React.Fragment key="left">
                <Drawer anchor="left" open={menuState} onClose={toggleDrawer(false)}>
                    {list("left")}
                </Drawer>
            </React.Fragment>
        </div>
    );
}
