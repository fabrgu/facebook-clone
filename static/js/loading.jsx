"use strict";

const {
  CircularProgress
} = MaterialUI

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