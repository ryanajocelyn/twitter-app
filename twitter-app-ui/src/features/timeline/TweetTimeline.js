import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTimelineAsync, selectTimeline } from './tweetTimelineSlice';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { TimelineCard } from './TimelineCard';
import { TimelineAction } from './TimelineAction';
import { selectUser } from '../auth/authSlice';


const useStyles = makeStyles((theme) =>({
    root: {
        flexGrow: 1,
        overflow: 'hidden',
        padding: theme.spacing(0, 3),
    }
}));

export function TweetTimeline() {
    const timeline = useSelector(selectTimeline);
    const user = useSelector(selectUser);
    const dispatch = useDispatch();
    const classes = useStyles();

    useEffect(() => {
        if (user && user.isLoggedIn) {
            dispatch(fetchTimelineAsync({
                userId: user.userId,
                count: 50
            }));
        }
    }, [])

    useEffect(()=> {

    }, [timeline]);

    useEffect(()=> {
        if (user && user.isLoggedIn) {
            dispatch(fetchTimelineAsync({
                userId: user.userId,
                count: 50
            }));
        }
    }, [user.isLoggedIn]);

    return (
        <React.Fragment>
            <CssBaseline />
            <Container maxWidth="md" className={classes.root}>
                {
                    user && user.isLoggedIn &&
                    <React.Fragment>
                        <TimelineAction />
                        { timeline.map( twt => <TimelineCard tweet={twt} /> ) }
                    </React.Fragment>
                }

                {
                    (!user || !user.isLoggedIn) &&
                    <Typography paragraph className={classes.title} color="textSecondary" gutterBottom>
                        Login with your Twitter Credential to view your timeline.
                    </Typography> 
                }
            </Container>
        </React.Fragment>
    );
}
