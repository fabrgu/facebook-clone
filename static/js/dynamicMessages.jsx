"use strict";

class SuccessMessage extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <li>
        <div className="alert success">
          <span className="closebtn">&times;</span>
        </div>
      </li>
    );
  }
}

class ErrorMessage extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    return(
      <li>
        <div className="alert error">
          <span className="closebtn">&times;</span>
        </div>
      </li>
    );
  }
}

class DynamicMessages extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      successes: [],
      errors: []
    };
  }

  render(){
    const { successes, errors } = this.state;
    const successesToLoad = []
    const errorsToLoad = []
    let successKey = 0;
    for (const success of successes){
      successesToLoad.push(
        <SuccessMessage key={successKey}
          message={success} />
      );
      successKey++;
    }

    let errorKey = 0;
    for (const error of errors){
      errorsToLoad.push(
        <ErrorMessage key={errorKey}
          message={error} />
      );
      errorKey++;
    }

    return(
      <React.Fragment>
        <ul>
          {errorsToLoad}
        </ul>
        <ul>
          {successesToLoad}
        </ul>
      </React.Fragment>
    );
  }
}