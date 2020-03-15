"use strict";

const {
  Card,
  CardContent,
  CardActions
} = MaterialUI

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
  }

  handleNewCommentInputChange(event){
    this.setState({newCommentText: event.target.value});
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
        }
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
      <div style={{ maxWidth: 450, margin: 'auto' }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              { this.props.post.user.first_name } 
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
              <Button size="small" onClick={this.handleAddComment}>
                Add Comment
              </Button>
            </CardActions>
          </CardContent>
        </Card>
      </div>
    );
  }
}