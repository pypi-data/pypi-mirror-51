import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps, BaseWidgetSettings} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import * as ReconnectingWebSocket from 'reconnectingwebsocket';

const styles = () => createStyles({
    body: {

    }
});


export class Settings extends BaseWidgetSettings {
    name: string = 'Olaf';
}

class ChromecastManager {


    private sockets: {[s: string]: {

    }};

}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                das widget body
            </div>
            <WidgetMenu id={config.id} settings={config.settings} settingsFormFields={[]} />
        </WidgetFrame>
    )
});

// const teve = new ReconnectingWebSocket(`ws://${window.location.host}/chromecast-proxy/Olaf`);

// teve.onopen = () => {
//     console.log('chromecast-proxy connected')
// }
// teve.onmessage = (event) => {
//     console.log(JSON.parse(event.data))
// }
// teve.onclose = () => {
//     console.log('chromecast-proxy closed')
// }
