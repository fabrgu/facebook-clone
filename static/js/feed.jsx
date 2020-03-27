"use strict";

const {
  CircularProgress,
  Card,
  CardContent,
  CardActions,
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

class Loading extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <React.Fragment>
        <CircularProgress style={{ marginTop: 15 }}/>
      </React.Fragment>
    )
  }
}

class Comment extends React.Component {
  constructor(props){
    super(props);

  }

  render(){
    return(
      <div>
        <Typography paragraph>
          { this.props.comment.user.first_name } {this.props.comment.user.last_name} says:
          <br /> { this.props.comment.comment }
        </Typography>
      </div>
    );
  }
}

class Post extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      newCommentText: '', 
      comments: this.props.post.comments 
    };
    this.handleAddComment = this.handleAddComment.bind(this);
    this.handleNewCommentInputChange = this.handleNewCommentInputChange.bind(this);
    this.showMessage = this.showMessage.bind(this);
  }

  handleNewCommentInputChange(event){
    this.setState({newCommentText: event.target.value});
  }

  showMessage(type, title, message){
    Swal.fire({
      icon: type,
      title: title,
      text: message
    });
  }

  async handleAddComment() {
    const post_id = this.props.post.post_id || '';
    const comment = this.state.newCommentText;
    if (post_id && comment){
      const response = await axios.post(`${window.location.origin}/add_comment`, 
        {
          post_id: post_id,
          user_id: this.props.userId,
          comment: comment
        });
      if (response.status === 200 && response.data.hasOwnProperty("success")){
        if (response.data["success"] && response.data.hasOwnProperty("comment")){
          const existingComments = this.state.comments;
          const newComment = response.data["comment"];
          existingComments.push(newComment);
          this.setState({comments: existingComments, newCommentText: ''});
        } else {
          this.showMessage('error', 'Oops...', 'Something went wrong!');
        }
      } else {
        this.showMessage('error', 'Oops...', 'Something went wrong!');
      }
    }
  }

  render(){
    const comments = this.state.comments;
    const commentElements = [];
    for (const comment of comments){
       commentElements.push(
         <Comment key={comment.comment_id} 
           comment={comment} />
       );
    }
    return(
      <div style={{ maxWidth: 450, margin: 'auto', marginTop: 10 }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              { this.props.post.user.first_name }&nbsp;
              { this.props.post.user.last_name } 
            </Typography>
            <Typography color="textSecondary">
              { this.props.post.posted_on } 
            </Typography>
            <Typography variant="body2" component="p">
              { this.props.post.message }
            </Typography>
            <Typography variant="body2">
              <b>Comments</b>
            </Typography>
            {commentElements}
            <CardActions>
              <TextareaAutosize aria-label="add new comment" 
                rowsMin={2} id="new-comment" name="new-comment"
                onChange={this.handleNewCommentInputChange} 
                value={this.state.newCommentText}
              />
              <Button size="small" style={{color: '#000000', backgroundColor: '#e0e0e0'}}
                onClick={this.handleAddComment}>
                Add Comment
              </Button>
            </CardActions>
          </CardContent>
        </Card>
      </div>
    );
  }
}

class AddPostSection extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <div style={{flex: 1, marginTop: 10}}>
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

class Feed extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isLoaded: false,
      posts: [],
      newPostMessage: ''
    }

    this.addNewPost = this.addNewPost.bind(this);
    this.handleNewPostInputChange = this.handleNewPostInputChange.bind(this);
    this.showMessage = this.showMessage.bind(this);
  }

  componentDidMount() {
    const fullUrl = this.props.userProfile ? 
              `${window.location.origin}/posts_for_user_feed` :
              `${window.location.origin}/posts_for_feed`;

    axios.get(fullUrl)
      .then((response) => {
        let posts_to_load = Array.isArray(response.data) ? response.data : [];
        this.setState({
          isLoaded: true,
          posts: posts_to_load
        })
      })
      .catch((error) => {
        console.log(error);
      });
  }

  showMessage(type, title, message){
    Swal.fire({
      icon: type,
      title: title,
      text: message
    });
  }

  handleNewPostInputChange(event){
    this.setState({newPostMessage: event.target.value});
  }

  async addNewPost(){
    const userId = this.props.userId || '';
    const message = this.state.newPostMessage;
    if (message && userId) {
      const response = await axios.post(`${window.location.origin}/add_post`, {
        user_id: userId,
        message: message
      });

      if (response.status === 200 && response.data.hasOwnProperty("success")){
        if (response.data["success"] && response.data.hasOwnProperty("post")){
          const existingPosts = this.state.posts;
          const post = response.data["post"];
          existingPosts.unshift(post)
          this.setState({
            posts: existingPosts,
            newPostMessage: ''
          });
        } else {
          this.showMessage('error', 'Oops...','Something went wrong!');
        }
      } else {
        this.showMessage('error', 'Oops...','Something went wrong!');
      }
    }
  }

  render(){
    const { isLoaded, posts } = this.state;
    let element = <Loading />;
    if (isLoaded){
      const postsToLoad = []
      for (const post of posts){
        postsToLoad.push(
          <Post key={post.post_id}
            post={post} 
            userId={this.props.userId} />
        );
      }

      element = postsToLoad;
    }
    return(
      <div className="centered">
        <ThemeProvider theme={darkTheme}>
        {this.props.userProfile &&
          <AddPostSection userId={this.props.userId} 
            addNewPost={this.addNewPost}
            newPostMessage={this.state.newPostMessage}
            handleNewPostInputChange={this.handleNewPostInputChange} />
        }
        {element}
        </ThemeProvider>
      </div>
    );
  }
}

