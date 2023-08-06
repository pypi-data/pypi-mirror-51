// ==============================================================================
// Copyright (C) 2019 - Philip Paquette, Steven Bocco
//
//  This program is free software: you can redistribute it and/or modify it under
//  the terms of the GNU Affero General Public License as published by the Free
//  Software Foundation, either version 3 of the License, or (at your option) any
//  later version.
//
//  This program is distributed in the hope that it will be useful, but WITHOUT
//  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
//  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
//  details.
//
//  You should have received a copy of the GNU Affero General Public License along
//  with this program.  If not, see <https://www.gnu.org/licenses/>.
// ==============================================================================
import React from 'react';
import {Forms} from "../../core/forms";
import {STRINGS} from "../../../diplomacy/utils/strings";
import PropTypes from "prop-types";

export class JoinForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.initState();
    }

    initState() {
        return {
            [this.getPowerNameID()]: this.getDefaultPowerName(),
            [this.getPasswordID()]: ''
        };
    }

    getPowerNameID() {
        return `power_name_${this.props.game_id}`;
    }

    getPasswordID() {
        return `registration_password_${this.props.game_id}`;
    }

    getDefaultPowerName() {
        return (this.props.powers && this.props.powers.length && this.props.powers[0]) || '';
    }

    render() {
        const onChange = Forms.createOnChangeCallback(this, this.props.onChange);
        const onSubmit = Forms.createOnSubmitCallback(this, this.props.onSubmit);
        return (
            <form className={'form-inline'}>
                <div className={'form-group'}>
                    {Forms.createLabel(this.getPowerNameID(), 'Power:')}
                    <select id={this.getPowerNameID()} className={'from-control custom-select ml-2'}
                            value={Forms.getValue(this.state, this.getPowerNameID())} onChange={onChange}>
                        {Forms.createSelectOptions(STRINGS.ALL_POWER_NAMES, true)}
                    </select>
                </div>
                <div className={'form-group mx-2'}>
                    {Forms.createLabel(this.getPasswordID(), '', 'sr-only')}
                    <input id={this.getPasswordID()} type={'password'} className={'form-control'}
                           placeholder={'registration password'}
                           value={Forms.getValue(this.state, this.getPasswordID())}
                           onChange={onChange}/>
                </div>
                {Forms.createSubmit('join', false, onSubmit)}
            </form>
        );
    }
}

JoinForm.propTypes = {
    game_id: PropTypes.string.isRequired,
    powers: PropTypes.arrayOf(PropTypes.string),
    onChange: PropTypes.func,
    onSubmit: PropTypes.func
};
