
import {CommonWidgetProps, LocalStorageSchema} from "./types";

const localStorageHandler = {
    get: (target: LocalStorageSchema, name: string) => {
        const res = window.localStorage.getItem(name);
        return res == undefined ? target[name] : JSON.parse(res);
    },
    set: (target: LocalStorageSchema, name: string, value: any, receiver: any) => {
        window.localStorage.setItem(name, JSON.stringify(value));
        return true;
    },
};

export const claudeLocalStorage = new Proxy<LocalStorageSchema>(new LocalStorageSchema(), localStorageHandler);

export function copy<T>(data: T): T {
    return JSON.parse(JSON.stringify(data))
}

export type ClaudeThemeType = 'light' | 'dark';

export type ClaudeTheme = {
    backgroundColor: string,
    color: string,
}

export const claudeThemes: {[key in ClaudeThemeType]: ClaudeTheme} = {
    dark: {
        backgroundColor: 'rgba(255,255,255,0.1)',
        color: 'white',
    },
    light: {
        backgroundColor: '',
        color: '',
    },
};

type WidgetStyleCallback<T = any> = (props: CommonWidgetProps<{}>) => T;

export namespace WidgetStyle {
    export function getRelativeSize(ratio: number): {width: WidgetStyleCallback<number>, height: WidgetStyleCallback<number>} {
        return {
            width: (props: CommonWidgetProps<{}>) => props.config.width * ratio,
            height: (props: CommonWidgetProps<{}>) => props.config.height * ratio,
        }
    }

    export function getThemeProp<T = {}>(propName: keyof ClaudeTheme) {
        return (props: CommonWidgetProps<T>) => claudeThemes[props.dashboardConfig.theme][propName];
    }
}

