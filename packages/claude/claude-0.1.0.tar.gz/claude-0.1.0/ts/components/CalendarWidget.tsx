
import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps, BaseWidgetSettings} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import {useInterval} from "./tools";
import {useState} from "react";
import * as moment from 'moment';
import {Moment} from "moment";
import * as classNames from 'classnames';
import {WidgetStyle} from "../tools";
import { FormSelectFieldDescriptor } from './WidgetSettingsDialog';

type Props = CommonWidgetProps<Settings>;

const bodyPadding = 5;

const gridAutoRows = ({config}: Props) => {
    return config.settings.months == 'rolling' ? `${(config.width - 2 * bodyPadding) / 7}px` : '';
}

const styles = () => createStyles({
    body: {
        padding: bodyPadding,
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        fontSize: WidgetStyle.getRelativeSize(0.06).width,
    },
    currentDateRow: {
        textAlign: 'center',
        paddingBottom: '0.5em',
    },
    weekRow: {
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        justifyItems: 'center',
        paddingBottom: '0.5em',
    },
    daysGridContainer: {
        overflow: 'hidden',
        flexGrow: 1,
        position: 'relative',
    },
    daysGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gridAutoRows: gridAutoRows,
        justifyItems: 'stretch',
        alignItems: 'stretch',
        position: 'relative',
        height: ({config}: Props) => config.settings.months == 'fixed' ? '100%' : 'auto',
        '& > div': {
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            fontSize: WidgetStyle.getRelativeSize(0.06).width,
        },
    },
    notCurrentMonthDay: {
        opacity: 0.2,
    },
    currentDay: {
        borderRadius: 5,
        backgroundColor: WidgetStyle.getThemeProp('backgroundColor'),
    }
});

export class Settings extends BaseWidgetSettings {
    months: 'fixed' | 'rolling' = 'fixed';
}

function roundTo(val: number, to: number): number {
    return Math.round(val / to) * to;
}

export default withStyles(styles)((props: Props & WithStyles<typeof styles>) => {

    moment.locale('en-gb');

    let daysGridContainerElement: HTMLElement = null;

    const today = () => moment(new Date().getTime()).startOf('day');

    const { config, classes, dashboardConfig } = props;
    const [currentDate, setCurrentDate] = useState(today());

    useInterval(() => {
        const newVal = today();
        if (!currentDate.isSame(newVal))
            setCurrentDate(newVal);
    }, 1000);

    React.useEffect(() => alignDaysGrid());

    const calcDayPadding = () => {
        const {width, height} = config;
        return roundTo((height - width) / (width * 0.04), 7)
    }

    const dayPadding = config.settings.months == 'rolling' ? calcDayPadding() : 0;

    const firstDayOfWeekForMonth = parseInt(currentDate.clone().startOf('month').format('E'))

    let cyc = currentDate.clone().startOf('month').subtract(firstDayOfWeekForMonth-1, 'd').subtract(dayPadding, 'd');

    let days = [];

    let end = currentDate.clone().add(1, 'month').startOf('month')
    end.add(end.isoWeekday() + dayPadding, 'd')

    while(1) {
        if (cyc.isAfter(end))
            break;

        days.push(cyc.clone());
        cyc.add(1, 'd');
    }

    const currentMonth = currentDate.format('M');

    const renderDay = (day: Moment) => {
        const month = day.format('M');
        const dayNumber = day.format('D');
        const className = classNames({
            [classes.notCurrentMonthDay]: currentMonth != month,
            [classes.currentDay]: day.isSame(today()),
        });
        return (
            <div className={className} key={`${month}.${dayNumber}`}>{dayNumber}</div>
        )
    };

    const alignDaysGrid = () => {
        if (!daysGridContainerElement)
            return;
        let daysGrid = daysGridContainerElement.childNodes[0] as HTMLElement;
        daysGrid.style.top = config.settings.months == 'fixed' ? '0px' :
                                `${(daysGridContainerElement.offsetHeight - daysGrid.scrollHeight) / 2}px`;
    }

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                <div className={classes.currentDateRow}>{currentDate.format('MMMM')}</div>
                <div className={classes.weekRow}>
                    {moment.weekdaysShort(true).map(name => <div key={name}>{name}</div>)}
                </div>
                <div className={classes.daysGridContainer} ref={r => daysGridContainerElement = r}>
                    <div className={classes.daysGrid}>
                        {days.map(renderDay)}
                    </div>
                </div>
            </div>
            <WidgetMenu id={config.id} settings={config.settings} settingsFormFields={[{
                name: 'months',
                label: 'Months',
                type: "select",
                options: [
                    {value: 'fixed', label: 'Fixed'},
                    {value: 'rolling', label: 'Rolling'},
                ],
            } as FormSelectFieldDescriptor ]} />
        </WidgetFrame>
    )
});
