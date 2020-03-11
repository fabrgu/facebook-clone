"use strict";

class AddPostSection extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <div>
      </div>
    )
  }
}

class Post extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <div>
      </div>
    )
  }
}

class Feed extends React.Component {
  constructor(props){
    super(props);
    console.log(props);
  }

  render(){
    return(
      <AddPostSection user_id={this.props.user_id} />
    );
  }
}

