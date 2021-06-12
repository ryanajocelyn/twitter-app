import React, { useState } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Switch from '@material-ui/core/Switch';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTimelineAsync, selectTimeline, storeSortedTimeline } from './tweetTimelineSlice';
import { selectUser } from '../auth/authSlice';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    container: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    }
}));

export function TimelineAction(props) {
    const classes = useStyles();
    const dispatch = useDispatch();
    const [dateSort, setDateSort] = useState(false);
    const [twtSearch, setTwtSearch] = useState("");
    const [startDate, setStartDate] = useState();
    const [endDate, setEndDate] = useState();
    const timeline = useSelector(selectTimeline);
    const user = useSelector(selectUser);

    const handleChange = (event) => {
        setDateSort(event.target.checked);
    };

    const handleTextChange = (event) => {
        setTwtSearch(event.target.value);
    };
    const handleSdChange = (event) => {
        setStartDate(event.target.value);
    };
    const handleEdChange = (event) => {
        setEndDate(event.target.value);
    };

    const handleApply = () => {
        console.log(`dateSort=${dateSort}: twtSearch=${twtSearch}: startDate=${startDate}: endDate=${endDate}`);
        var tmp_timeline = [...timeline];
        if (twtSearch && twtSearch.length > 0) {
            tmp_timeline = tmp_timeline.filter(twt => twt.tweet.indexOf(twtSearch) !== -1);
        } else if (startDate && endDate) {
            dispatch(fetchTimelineAsync({
                userId: user.userId,
                startDate,
                endDate,
                count: 50
            }));
        } else {
            if (dateSort) {
                tmp_timeline.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
            } else {
                tmp_timeline.sort((a, b) => a.tweet > b.tweet? 1: -1);
            }       
        }

        dispatch(storeSortedTimeline(tmp_timeline));
    };

    return (
        <Paper className={classes.root} variant="outlined" raised>
                    <Grid container className={classes.root} spacing={2}>
                        <Grid item xs={3}>
                            <TextField id="outlined-basic" label="Tweet Text" variant="outlined"
                                size="small" value={twtSearch} onChange={handleTextChange} />
                        </Grid>                                
                        <Grid item xs={2}>
                            <div>
                                <Typography paragraph className={classes.title} color="textSecondary" gutterBottom>
                                    Date Sort:
                            <Switch
                                        checked={dateSort}
                                        onChange={handleChange}
                                        color="primary"
                                        name="Sort By Time"
                                        inputProps={{ 'aria-label': 'secondary checkbox' }}
                                    />
                                </Typography>
                            </div>
                            </Grid>                                
                        <Grid item xs={3}>

                            <TextField
                                id="datetime-local"
                                label="Tweet From"
                                type="datetime-local"
                                className={classes.textField}
                                onChange={handleSdChange}
                                InputLabelProps={{
                                    shrink: true,
                                }}
                            />
                        </Grid>                                
                        <Grid item xs={3}>

                            <TextField
                                id="datetime-local"
                                label="Tweet To"
                                type="datetime-local"
                                className={classes.textField}
                                onChange={handleEdChange}
                                InputLabelProps={{
                                    shrink: true,
                                }}
                            />
                        </Grid>                                
                        <Grid item xs={2}>

                            <Button variant="contained" color="primary" onClick={handleApply}>
                                Apply
                    </Button>
                        </Grid>
                    </Grid>
                <Typography paragraph className={classes.title} color="textSecondary" gutterBottom>

                </Typography>
        </Paper>
    )
}
