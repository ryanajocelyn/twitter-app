import React from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) =>({
    root: {
        flexGrow: 1,
        overflow: 'hidden',
        padding: theme.spacing(0, 3),
    },
    paper: {
        maxWidth: 800,
        margin: `${theme.spacing(1)}px auto`,
        padding: theme.spacing(2),
    },
    bullet: {
        display: 'inline-block',
        margin: '0 2px',
        transform: 'scale(0.8)',
    },
    title: {
        fontSize: 14,
    },
    pos: {
        'text-align': 'right',
        fontSize: 'small'
    },
    iconPos: {
        flex: 'auto'
    }
}));


export function TimelineCard(props) {
    const classes = useStyles();
    const twt = props.tweet;

    return (
        <Paper className={classes.paper}>
            <Card className={classes.root} variant="outlined" raised>
                <CardContent>
                    <Typography paragraph className={classes.title} color="textSecondary" gutterBottom>
                        {twt.tweet}
                    </Typography>
                </CardContent>
                <CardActions>
                    <Typography className={classes.pos} color="textSecondary" align="right">
                        {twt.created_at}
                    </Typography>
                    <Typography className={classes.iconPos}> </Typography>
                    <IconButton aria-label="add to favorites">
                        <FavoriteIcon />
                    </IconButton>
                    <IconButton aria-label="share">
                        <ShareIcon />
                    </IconButton>
                </CardActions>
            </Card>
        </Paper>
    )
}
