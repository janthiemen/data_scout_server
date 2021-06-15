import * as React from "react";
import autobind from 'class-autobind';

import { Button, ButtonGroup, H4, Icon, InputGroup, Intent, IToastProps, Tab, Tabs, Tooltip } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { History } from 'history'

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { SettingsService, UserService } from "../../helpers/userService";

import { withRouter } from "react-router-dom";
import { User } from "../ScoutNavbar";


interface SettingsUserRowProps {
    userService: UserService;
    currentUser: number;
    user: User;
    refresh: () => void;
}

interface SettingsUserRowState {
    showPassword: boolean;
    user: User;
    currentUser: number;
    password: string;
    passwordRepeat: string;
    deleted: boolean;
}


/**
 * The page with all the data sources.
 */
export class SettingsUserRowComponent extends React.Component<SettingsUserRowProps> {
    private userService: UserService;
    // private addToast: (toast: IToastProps, key?: string) => string;
    // private history: History;
    public state: SettingsUserRowState;
    private refresh: () => void;

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: SettingsUserRowProps) {
        super(props);
        autobind(this);
        let user = props.user;
        if (props.user === undefined) {
            user = {"id": null, "username": ""};
        }
        this.state = {
            showPassword: false,
            currentUser: props.currentUser,
            user: user,
            password: "",
            passwordRepeat: "",
            deleted: false
        }
        this.userService = props.userService;
        this.refresh = props.refresh;
    }

    /**
     * Called when the password was changed.
     * @param e The event
     */
    private onPasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
        this.setState({ password: event.target.value });
    }
    private onPasswordRepeatChange(event: React.ChangeEvent<HTMLInputElement>) {
        this.setState({ passwordRepeat: event.target.value });
    }
    private onUsernameChange(event: React.ChangeEvent<HTMLInputElement>) {
        let user = this.state.user;
        user.username = event.target.value;
        this.setState({ user: user });
    }

    /**
     * Update the password.
     */
    private onSave() {
        if (this.state.user !== undefined && this.state.user.id !== null) {
            this.userService.changePassword(this.state.user.id, this.state.password, this.state.passwordRepeat, this.finishSave);
        } else {
            this.userService.createUser(this.state.user.username, this.state.password, this.state.passwordRepeat, this.finishSave);
        }
    }

    protected finishSave(body: {}) {
        if (this.state.user !== undefined && this.state.user.id !== null) {
            this.userService.addToast({ intent: Intent.SUCCESS, message: "The password was changed" });
        } else {
            this.userService.addToast({ intent: Intent.SUCCESS, message: "The user was created" });
            this.setState({ user: {"id": null, "username": ""},
                            password: "",
                            passwordRepeat: ""
                        });
        }
        this.refresh();
    }

    /**
     * Delete the user. Note: This shouldn't be possible for the active user.
     */
    private onDelete() {
        this.userService.deleteUser(this.state.user.id, this.finishDelete);
    }
    protected finishDelete(body: {}) {
        this.userService.addToast({ intent: Intent.SUCCESS, message: "The user was deleted" })
        this.setState({ deleted: true });
    }

    private renderUsername() {
        if (this.state.user !== undefined && this.state.user.id !== null) {
            return <span>{this.state.user.username}</span>
        } else if (this.state.user !== undefined) {
            return <InputGroup
                placeholder="Enter new username"
                type="text"
                value={this.state.user.username} 
                onChange={this.onUsernameChange}
            />
        }
    }

    /**
     * Renders the settings page
     * @returns  
     */
    render() {
        if (this.state.deleted) {
            return <></>;
        }

        const lockButton = (
            <Tooltip content={`${this.state.showPassword ? "Hide" : "Show"} Password`}>
                <Button
                    icon={this.state.showPassword ? "unlock" : "lock"}
                    intent={Intent.WARNING}
                    minimal={true}
                    onClick={() => this.setState({ showPassword: !this.state.showPassword })}
                />
            </Tooltip>
        );
        
        return (
            <Row> 
                <Col md={2}>
                    {this.renderUsername()}
                </Col>
                <Col md={3}>
                    <InputGroup
                        placeholder="Enter new password"
                        rightElement={lockButton}
                        type={this.state.showPassword ? "text" : "password"}
                        value={this.state.password} 
                        onChange={this.onPasswordChange}
                    />
                </Col>
                <Col md={3}>
                    <InputGroup
                        placeholder="Repeat password"
                        rightElement={lockButton}
                        type={this.state.showPassword ? "text" : "password"}
                        value={this.state.passwordRepeat}
                        onChange={this.onPasswordRepeatChange}
                    />
                </Col>
                <Col md={1}>
                    <ButtonGroup>
                        <Button outlined={true} icon="floppy-disk" onClick={this.onSave}>Save</Button>
                        <Button outlined={true} icon="delete" intent={Intent.DANGER} onClick={this.onDelete}>Delete</Button>
                    </ButtonGroup>
                </Col>
            </Row>
        );
    }

}

interface UserDetail extends User {
    is_staff: boolean;
    first_name: string;
    last_name: string;
}

interface SettingsState {
    users: User[];
    user: UserDetail;
}

/**
 * The page with all the data sources.
 */
export class SettingsComponent extends React.Component<PageProps> {
    private settingsService: SettingsService;
    private userService: UserService;
    private addToast: (toast: IToastProps, key?: string) => string;
    private history: History;
    public state: SettingsState = {
        users: [],
        user: undefined
    }

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: PageProps) {
        super(props);
        autobind(this);
        this.settingsService = new SettingsService(props.addToast, props.setLoggedIn);
        this.userService = new UserService(props.addToast, props.setLoggedIn);
        this.history = props.history;

        this.addToast = props.addToast;
        this.refresh();
    }

    /**
     * Refresh the data
     */
    public refresh() {
        this.userService.getUsers(this.receiveUsers);
        this.userService.getUserDetail(this.receiveUserDetails);
    }

    /**
     * Callback when a list of users has been received.
     * @param body A list of users.
     */
     private receiveUsers(body: {[key: string]: any}) {
        this.setState({ users: body["results"] });
    }

    /**
     * Callback when a list of users has been received.
     * @param body A list of users.
     */
    private receiveUserDetails(body: UserDetail) {
        this.setState({ user: body });
    }

    private renderUsers() {
        console.log(this.state.user);
        if (this.state.user !== undefined && this.state.user.is_staff) {
            return <Tab id="settings-users" title="Users" className="settings-tab" panel={
                    <Grid fluid>
                        <Row>
                            <Col md={2}>
                                <H4>Username</H4>
                            </Col>
                            <Col md={3}>
                                <H4>Password</H4>
                            </Col>
                            <Col md={3}>
                                <H4>Repeat password</H4>
                            </Col>
                            <Col md={1}>
                                {/* Placeholder */}
                            </Col>
                        </Row>

                        {this.state.users.map((user: User, index: number) => 
                            <SettingsUserRowComponent userService={this.userService} currentUser={this.state.user.id} user={user} refresh={this.refresh} /> 
                        )}
                        <hr />
                        <SettingsUserRowComponent userService={this.userService} currentUser={this.state.user.id} user={undefined} refresh={this.refresh} /> 
                    </Grid>
                } />;
        } else {
            return <></>
        }
    }

    private renderProjects() {
        console.log(this.state.user);
        if (this.state.user !== undefined && this.state.user.is_staff) {
            return <Tab id="settings-projects" title="Projects" className="settings-tab" panel={<div>Bladiebla react</div>} />;
        } else {
            return <></>
        }
    }

    /**
     * Renders the settings page
     * @returns  
     */
    render() {
        console.log(this.state.users);
        return (
            <>
                <Tabs id="TabsExample" vertical={true}>
                    <Tab id="settings-general" className="settings-tab" title="General" panel={
                        <div>
                            There are no general settings (yet).
                        </div>
                    } />
                    {this.renderUsers()}
                    {this.renderProjects()}
                </Tabs>
            </>
        );
    }

}

export const Settings = withRouter(SettingsComponent)