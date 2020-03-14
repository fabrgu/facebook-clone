"use strict";

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark'
  },
  spacing: 2
});

class Feed extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isLoaded: false,
      posts: []
    }
  }

  componentDidMount() {
    axios.get(`${window.location.origin}/posts_for_feed`)
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

  render(){
    const { isLoaded, posts } = this.state
    let element = <Loading />;
    if (isLoaded){
      const postsToLoad = []
      for (const post of posts){
        postsToLoad.push(
          <Post key={post.post_id} 
            post_id={post.post_id}
            user_id={this.props.user_id} 
            message={post.message}
            posted_on={post.posted_on} />
        );
      }

      element = postsToLoad;
    }
    return(
      <div className="feed-centered">
        <ThemeProvider theme={darkTheme}>
          <AddPostSection user_id={this.props.user_id} />
          {element}
        </ThemeProvider>
      </div>
    );
  }
}

