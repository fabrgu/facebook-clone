"use strict";

const {
  AppBar,
  Toolbar,
  Typography,
  TextField,
  Button,
  ThemeProvider,
  createMuiTheme,
  colors
} = MaterialUI;


const muiTheme = createMuiTheme({
  palette: {
    primary: colors.lightBlue
  }
});

class Logout extends React.Component {
  constructor(props) {
    super(props);

    this.handleLogout = this.handleLogout.bind(this);
  }

  async handleLogout(){
    const response = await axios.post(`${window.location.origin}/logout`);
    if (response.status === 200 && response.data.hasOwnProperty("logged_out")){
      if (response.data["logged_out"]){
        window.location = window.location.origin;
      }
    }
  }

  render(){
    return(
      <React.Fragment>
        <Button variant="contained" size="small"
            onClick={this.handleLogout} className="logout-button">
            Log Out
        </Button>
      </React.Fragment>
    );
  }
}
class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {login_email: '', login_password: ''};

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.validForm = this.validForm.bind(this);
  }

  validForm(){
    return this.state.login_email !== '' && this.state.login_password !== '';
  }

  handleInputChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    this.setState({[name]: value});
  }

  async handleSubmit(event){
    if (this.validForm()){
      const response = await axios.post(`${window.location}login`, { 
        email: this.state.login_email,
        password: this.state.login_password
      });

      if (response.status === 200 && response.data.hasOwnProperty("success")){
        if (response.data["success"]){
          window.location = `${window.location.origin}/feed`;
        }
      }
    }

  }

  render(){
    return(
      <React.Fragment>
        <form action='/login' method="POST" id="login-form">
          <TextField id="login-email" name="login_email" label="Email" 
            required className="login-text"
            onChange={this.handleInputChange}
          />
          <TextField id="login-password" label="Password" 
            name="login_password" type="password"
            className="login-text" onChange={this.handleInputChange}
            autoComplete="current_password" required />
          <Button variant="contained" size="small"
            onClick={this.handleSubmit} className="login-button">
            Log In
          </Button>
        </form>
      </React.Fragment>
    );
  }
}

class Navbar extends React.Component {
  constructor(props){
    super(props);
  }

  render(){
    const isLoggedIn = this.props.loggedIn;
    let navLogEl;
    if (isLoggedIn){
      navLogEl = <Logout />;
    } else {
      navLogEl = <Login />;
    }
    return(
      <React.Fragment>
        <ThemeProvider theme={muiTheme}>
          <AppBar position="static" title="Facebook Clone">
            <Toolbar>
              <Typography variant="h5" style={{flex : 1}}>
                Facebook Clone
              </Typography>
              {navLogEl}
            </Toolbar>
          </AppBar>
        </ThemeProvider>
      </React.Fragment>
    );
  }
}
