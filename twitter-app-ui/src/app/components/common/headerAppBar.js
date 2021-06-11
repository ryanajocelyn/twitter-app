import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import MenuDrawer from './menuDrawer';
import { closeMenu, selectMenuState, showMenu } from './commonSlice';
import axios from 'axios'
import queryString from 'query-string';
import { setUserProfile, selectUser } from '../../../features/auth/authSlice';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
}));

export default function HeaderAppBar() {
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

    const twitterLogin = () => {
        console.log('twitter login');
        (async () => {

            try {
                //OAuth Step 1
                const response = await axios({
                    url: `/api/v1/twitter/oauth/request_token`,
                    method: 'POST'
                });

                const { oauth_token } = response.data;

                //Oauth Step 2
                window.location.href = `https://api.twitter.com/oauth/authenticate?oauth_token=${oauth_token}`;
            } catch (error) {
                console.error(error);
            }

        })();
        // window.location.href = 'http://localhost:5000/authenticate/twitter';
        // window.location.href = 'http://localhost:5000/api/v1/auth/login';
    };

    useEffect(() => {
        (async () => {

            const { oauth_token, oauth_verifier } = queryString.parse(window.location.search);

            if (oauth_token && oauth_verifier) {
                try {
                    //Oauth Step 3
                    await axios({
                        url: `/api/v1/twitter/oauth/access_token`,
                        method: 'POST',
                        data: { oauth_token, oauth_verifier }
                    });
                } catch (error) {
                    console.error(error);
                }
            }

            try {
                //Authenticated Resource Access
                const { data: { name, profile_image_url, status, id_str } } = await axios({
                    url: `/api/v1/twitter/users/profile_banner`,
                    method: 'GET'
                });

                dispatch(setUserProfile({
                    isLoggedIn: true,
                    userId: id_str,
                    name, 
                    imageUrl: profile_image_url,
                    status
                    //url: entities.url.urls[0].expanded_url
                }))
            } catch (error) {
                console.error(error);
            }
        })();
    }, []);

    useEffect(()=> {

    }, [user.isLoggedIn]);

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu"
                        onClick={toggleDrawer(true)}>
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" className={classes.title}>
                        Twitter App
                    </Typography>     
                    <Button color="inherit" onClick={twitterLogin}>
                        {user.isLoggedIn ? 'Logout' : 'Login' }
                    </Button>
                </Toolbar>
            </AppBar>
            <MenuDrawer showMenu={menuState} closeMenu={toggleDrawer} />
        </div>
    );
}
