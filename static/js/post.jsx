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
          { this.props.comment }
        </Typography>
      </div>
    );
  }
}
class Post extends React.Component {
  constructor(props){
    super(props);
    this.state = {comment: ''}

    this.handleAddComment = this.handleAddComment.bind(this);
    this.handleNewPostInputChange = this.handleNewPostInputChange.bind(this);
  }

  handleNewPostInputChange(event){
    this.setState({comment: event.target.value})
  }

  async handleAddComment() {
    const post_id = this.props.post_id || '';
    const comment = this.props.comment;
    if (post_id && comment){
      const response = await axios.post(`${window.location.origin}/add_comment`, 
        {
          post_id: post_id,
          user_id: this.props.user_id,
          comment: comment
        });

      if (response.status === 200 && response.data.hasOwnProperty("success")){
        if (response.data["success"]){
          console.log('comment successful!');
        }
      }
    }
  }

  render(){
    return(
      <div style={{ maxWidth: 450, margin: 'auto' }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Post { this.props.post_id } 
            </Typography>
            <Typography color="textSecondary">
              { this.props.posted_on } 
            </Typography>
            <Typography variant="body2" component="p">
              { this.props.message }
            </Typography>
            <Typography variant="body2">
              Comments
            </Typography>
            <CardActions>
              <TextareaAutosize aria-label="add new comment" 
                rowsMin={2} id="new-comment" name="new-comment"
                onChange={this.handleNewCommentInputChange}
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