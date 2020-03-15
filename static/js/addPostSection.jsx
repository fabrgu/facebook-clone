"use strict";

const {
  Paper,
  Grid,
  TextareaAutosize
} = MaterialUI

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark'
  },
  spacing: 2
});

class AddPostSection extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <div style={{flex: 1}}>
        <Paper variant='outlined' 
          style={{ margin: 'auto', maxWidth: 450 }}>
          <Grid container>
            <Grid item xs={12} sm container alignItems="flex-end">
              <Grid item xs container direction="column" 
                alignContent='space-around' spacing={2}>
                <Grid item xs>
                  <Typography gutterBottom variant="subtitle1">
                    What's on your mind?
                  </Typography>
                  <TextareaAutosize aria-label="add new post" 
                    rowsMin={5} id="new-post" name="new-post"
                    onChange={this.props.handleNewPostInputChange}
                    value={this.props.newPostMessage}
                    />
                </Grid>
              </Grid>
              <Grid item>
                <Button variant="contained" size="small" style={{margin: 5}}
                  onClick={this.props.addNewPost} className="add-post">
                  Add Post
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </Paper>
      </div>
    )
  }
}
