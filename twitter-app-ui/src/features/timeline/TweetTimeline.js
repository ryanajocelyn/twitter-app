import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTimelineAsync, selectTimeline } from './tweetTimelineSlice';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import { TimelineCard } from './TimelineCard';
import { TimelineAction } from './TimelineAction';


const useStyles = makeStyles((theme) =>({
    root: {
        flexGrow: 1,
        overflow: 'hidden',
        padding: theme.spacing(0, 3),
    }
}));

export function TweetTimeline() {
    const timeline = useSelector(selectTimeline);
    const dispatch = useDispatch();
    const classes = useStyles();

    useEffect(() => {
        dispatch(fetchTimelineAsync(50));
    }, [])

    useEffect(()=> {

    }, [timeline]);

    return (
        <React.Fragment>
            <CssBaseline />
            <Container maxWidth="md" className={classes.root}>
                <TimelineAction />
                { timeline.map( twt => <TimelineCard tweet={twt} /> ) }
            </Container>
        </React.Fragment>
    );
}
