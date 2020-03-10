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

class Navbar extends React.Component {
  render(){
    return(
      <React.Fragment>
        <ThemeProvider theme={muiTheme}>
          <AppBar position="static" title="Facebook Clone">
            <Toolbar>
              <Typography variant="h5">
                Facebook Clone
              </Typography>
              <form noValidate id="login-form">
                <TextField id="login-email" label="Email" className="login-text"
                />
                <TextField id="login-password" label="Password" className="login-text" />
                <Button variant="contained" size="small" className="login-button">
                  Log In
                </Button>
              </form>
            </Toolbar>
          </AppBar>
        </ThemeProvider>
      </React.Fragment>
    );
  }
}

ReactDOM.render(<Navbar />, document.querySelector("#navigation"));