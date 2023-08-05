import { CSSProperties } from "react";

export type ClaudeTheme = {
    title: string,
    controlBar: {
        openerColor: string,
    },
    dashboard: CSSProperties,
    widget: CSSProperties,
}

export type ClaudeThemeType = 'blue';

export const claudeThemes: {[key in ClaudeThemeType]: ClaudeTheme} = {
    blue: {
        title: 'Blue',
        controlBar: {
            openerColor: 'white',
        },
        dashboard: {
            backgroundImage: 'url(/static/pics/canvas_blue_texture_surface_shadow_44965_1920x1200.jpg)'
        },
        widget: {
            color: '#eee',
            backgroundColor: 'rgba(0,0,0,0.4)',
        }
    }
};
