import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, FormControl, InputLabel, Select, MenuItem } from '@material-ui/core';
import * as React from "react";
import { useState } from "react";
import { DashboardConfig } from '../types';
import {ClaudeThemeType} from "../tools";

export type Props = {
    show: boolean,
    onClose: () => void
    submit: (data: DashboardConfig) => void,
    title: string,
    data?: DashboardConfig,
}

export default (props: Props) => {

    const {show, onClose, title, submit} = props;

    const [data, setData] = useState(props.data || {
        name: '',
        stepSize: 10,
        background: '',
        theme: 'dark',
    } as DashboardConfig);

    const onSubmit = (ev: React.SyntheticEvent) => {
        ev.preventDefault();
        submit(data);
    };

    const updateData = (partialData: Partial<DashboardConfig>) => {
        setData(Object.assign({}, data, partialData))
    };

    return <Dialog
            open={show}
            onClose={onClose}
            // TransitionComponent={dialogTransition} // use class ...
        >
            <DialogTitle>{title}</DialogTitle>
            <form onSubmit={onSubmit}>
                <DialogContent style={{maxWidth: 300}}>
                    <TextField autoFocus margin="dense" id="name" label="Name" type="text" required fullWidth
                        value={data.name} onChange={ev => updateData({name: ev.target.value})} />
                    <TextField margin="dense" id="stepSize" label="Step size" type="number" required fullWidth
                        value={data.stepSize} onChange={ev => updateData({stepSize: parseInt(ev.target.value)})} />
                    <TextField margin="dense" id="background" label="Background css" type="text" fullWidth
                        value={data.background} onChange={ev => updateData({background: ev.target.value})} />
                    <FormControl fullWidth>
                        <InputLabel>Theme</InputLabel>
                        <Select fullWidth value={data.theme} onChange={ev => updateData({theme: ev.target.value as ClaudeThemeType})} >
                            <MenuItem value="dark">Dark</MenuItem>
                            <MenuItem value="light">Light</MenuItem>
                        </Select>
                    </FormControl>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onClose} color="primary">Cancel</Button>
                    <Button type="submit" color="primary">Submit</Button>
                </DialogActions>
            </form>
        </Dialog>

};
