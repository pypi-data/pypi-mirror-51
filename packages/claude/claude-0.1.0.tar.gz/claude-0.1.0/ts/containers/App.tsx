import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import * as React from "react";
import { connect } from 'react-redux';
import Dashboard from "../components/Dashboard";
import { DashboardConfig, State, WidgetConfigList } from "../types";
import ControlBar from "./ControlBar";

const styles = () => createStyles({
    root: {
        height: '100%',
    }
});

type StateProps = {
    dashboardConfig: DashboardConfig,
    widgetConfigs: WidgetConfigList,
}

const App = withStyles(styles)(React.memo((props: StateProps & WithStyles<typeof styles>) => {

    const {dashboardConfig, widgetConfigs} = props;

    return <div className={props.classes.root}>
        <ControlBar />
        {dashboardConfig ? <Dashboard config={dashboardConfig} widgets={widgetConfigs} /> : null}
    </div>
}))

function mapStateToProps(state: State): StateProps {
    const { currentDashboardId, dashboards, widgets } = state;
    return {
        dashboardConfig: dashboards[currentDashboardId],
        widgetConfigs: Object.values(widgets).filter(w => w.dashboardId == currentDashboardId),
    }
}

export default connect<StateProps>(mapStateToProps)(App);
