import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { colors, createMuiTheme, CssBaseline, MuiThemeProvider } from "@material-ui/core";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { Provider } from 'react-redux';
import App from "./containers/App";
import configureStore from "./store";

library.add(fas);

const store = configureStore();

const darkTheme = createMuiTheme({
    palette: {
        type: 'dark',
        primary: colors.cyan,
        secondary: colors.pink,
    },
});

ReactDOM.render(
    <React.Fragment>
        <CssBaseline />
        <Provider store={store}>
            <MuiThemeProvider theme={darkTheme}>
                <App/>
            </MuiThemeProvider>
        </Provider>
    </React.Fragment>,
    document.getElementById("body")
);
