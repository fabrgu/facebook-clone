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
    this.state = {message: ''};

    this.handleAddPost = this.handleAddPost.bind(this);
    this.handleNewPostInputChange = this.handleNewPostInputChange.bind(this);
  }

  handleNewPostInputChange(event){
    this.setState({message: event.target.value});
  }

  async handleAddPost() {
    const userId = this.props.userId || '';
    const message = this.state.message;
    if (message && userId) {
      const response = await axios.post(`${window.location.origin}/add_post`, {
        user_id: userId,
        message: message
      });

      if (response.status === 200 && response.data.hasOwnProperty("success")){
        if (response.data["success"]){
          console.log('post successful!');
        }
      }
    }

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
