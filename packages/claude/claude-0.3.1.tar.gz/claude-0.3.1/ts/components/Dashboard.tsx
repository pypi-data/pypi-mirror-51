import * as React from "react";
import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import { WidgetConfig, DashboardConfig, WidgetConfigList, UpdateWidgetConfigAction } from "../types";
import widgetRegistry from '../widgetRegistry'
import { claudeThemes } from "../themes";

const styles = () => createStyles({
    body: {
        height: '100%',
    }
});

export interface Props {
    config: DashboardConfig,
    widgets: WidgetConfigList,
}

export default withStyles(styles)(React.memo((props: Props & WithStyles<typeof styles>) => {

    function factory(wconf: WidgetConfig) {
        const settingsType = widgetRegistry[wconf.type].settingsType;
        return React.createElement(widgetRegistry[wconf.type].factory, { // TODO: factory type is 'any'
            config: {...wconf, settings: Object.assign({}, new settingsType(), wconf.settings)} ,
            dashboardConfig: props.config,
            key: wconf.id,
        });
    }

    return (
        <div className={props.classes.body} style={{...claudeThemes[props.config.theme].dashboard}} >
            {props.widgets.map(factory)}
        </div>
    )
}))
