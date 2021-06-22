import * as React from "react";
import autobind from 'class-autobind';

import { Alert, Button, ButtonGroup, H4, Icon, InputGroup, Intent, IToastProps, Tab, Tabs, Tooltip } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { History } from 'history'

import { Grid, Row, Col } from 'react-flexbox-grid';
import { PageProps } from "../../helpers/props";
import { SettingsService, UserService } from "../../helpers/userService";

import { withRouter } from "react-router-dom";
import { ProjectFull, User } from "../ScoutNavbar";
import { ProjectDialog } from "../ProjectDialog";


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
    isOpenDelete: boolean;
}


/**
 * The page with all the data sources.
 */
export class SettingsUserRowComponent extends React.Component<SettingsUserRowProps> {
    private userService: UserService;
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
            user = { "id": null, "username": "" };
        }
        this.state = {
            showPassword: false,
            currentUser: props.currentUser,
            user: user,
            password: "",
            passwordRepeat: "",
            deleted: false,
            isOpenDelete: false
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
            this.setState({
                user: { "id": null, "username": "" },
                password: "",
                passwordRepeat: ""
            });
        }
        this.refresh();
    }

    /**
     * Confirm the delete action.
     */
    private handleDeleteAsk() {
        this.setState({ isOpenDelete: true });
    }

    /**
     * Callback when the user cancels the delete action.
     */
    private handleDeleteCancel() {
        this.setState({ isOpenDelete: false });
    }

    /**
     * Callback when the user confirms the delete action.
     * Delete the user. Note: This shouldn't be possible for the active user.
     */
    private handleDeleteConfirm() {
        this.userService.deleteUser(this.state.user.id, this.finishDelete);
        this.setState({ isOpenDelete: false });
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
                <Alert
                    canEscapeKeyCancel={true}
                    canOutsideClickCancel={true}
                    cancelButtonText="No"
                    confirmButtonText="Yes"
                    icon="trash"
                    intent={Intent.DANGER}
                    isOpen={this.state.isOpenDelete}
                    onCancel={this.handleDeleteCancel}
                    onConfirm={this.handleDeleteConfirm}
                >
                    <p>Are you sure you want to delete <b>{this.state.user.username}</b>?</p>
                </Alert>

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
                        <Button outlined={true} icon="floppy-disk" onClick={this.onSave}>{this.state.user.id === null ? "Create" : "Save"}</Button>
                        <Button outlined={true} icon="delete" intent={Intent.DANGER} onClick={this.handleDeleteAsk}>Delete</Button>
                    </ButtonGroup>
                </Col>
            </Row>
        );
    }
}

interface SettingsProjectRowProps {
    settingsService: SettingsService;
    project: ProjectFull;
    refresh: () => void;
    handleEditOpen: (project: number) => void;
}

interface SettingsProjectRowState {
    project: ProjectFull;
    deleted: boolean;
    isOpenDelete: boolean;
}


/**
 * The page with all the data sources.
 */
export class SettingsProjectRowComponent extends React.Component<SettingsProjectRowProps> {
    private settingsService: SettingsService;
    public state: SettingsProjectRowState;
    private refresh: () => void;
    private handleEditOpen: (project: number) => void;

    /**
     * Creates an instance of data sources.
     * @param props 
     */
    constructor(props: SettingsProjectRowProps) {
        super(props);
        autobind(this);
        this.state = {
            project: props.project,
            deleted: false,
            isOpenDelete: false
        }
        this.settingsService = props.settingsService;
        this.refresh = props.refresh;
        this.handleEditOpen = props.handleEditOpen;
    }

    private handleEditOpenDialog() {
        this.handleEditOpen(this.state.project.id);
    }

    /**
     * Confirm the delete action.
     */
    private handleDeleteAsk() {
        this.setState({ isOpenDelete: true });
    }

    /**
     * Callback when the user cancels the delete action.
     */
    private handleDeleteCancel() {
        this.setState({ isOpenDelete: false });
    }

    /**
     * Callback when the user confirms the delete action.
     * Delete the user. Note: This shouldn't be possible for the active user.
     */
    private handleDeleteConfirm() {
        this.settingsService.deleteProject(this.state.project.id, this.finishDelete);
        this.setState({ isOpenDelete: false });
    }

    protected finishDelete(body: {}) {
        this.settingsService.addToast({ intent: Intent.SUCCESS, message: "The project was deleted" })
        this.setState({ deleted: true });
    }

    /**
     * Renders the settings page
     * @returns  
     */
    render() {
        if (this.state.deleted) {
            return <></>;
        }

        return (
            <Row>
                <Alert
                    canEscapeKeyCancel={true}
                    canOutsideClickCancel={true}
                    cancelButtonText="No"
                    confirmButtonText="Yes"
                    icon="trash"
                    intent={Intent.DANGER}
                    isOpen={this.state.isOpenDelete}
                    onCancel={this.handleDeleteCancel}
                    onConfirm={this.handleDeleteConfirm}
                >
                    <p>Are you sure you want to delete <b>{this.state.project.name}</b>? This will delete <i>all</i> associated resources!</p>
                </Alert>

                <Col md={2}>
                    {this.state.project.name}
                </Col>
                <Col md={1}>
                    <ButtonGroup>
                        <Button outlined={true} icon="edit" onClick={this.handleEditOpenDialog}>Edit</Button>
                        <Button outlined={true} icon="delete" intent={Intent.DANGER} onClick={this.handleDeleteAsk}>Delete</Button>
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
    projects: ProjectFull[];
    projectEdit: number;
}

/**
 * The page with all the data sources.
 */
export class SettingsComponent extends React.Component<PageProps> {
    private settingsService: SettingsService;
    private userService: UserService;
    public state: SettingsState = {
        users: [],
        user: undefined,
        projectEdit: null,
        projects: []
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
        this.refresh();
    }

    /**
     * Refresh the data
     */
    public refresh() {
        this.userService.getUsers(this.receiveUsers);
        this.settingsService.getProjects(this.receiveProjects);
        this.userService.getUserDetail(this.receiveUserDetails);
    }

    public handleEditProjectOpen(project: number) {
        this.setState({ projectEdit: project });
    }

    public handleEditProjectClose() {
        this.setState({ projectEdit: null });
    }

    /**
     * Callback when a list of users has been received.
     * @param body A list of users.
     */
    private receiveUsers(body: { [key: string]: any }) {
        this.setState({ users: body["results"] });
    }

    /**
     * Callback when a list of projects has been received.
     * @param body A list of projects.
     */
    private receiveProjects(body: { [key: string]: any }) {
        this.setState({ projects: body["results"] });
    }

    /**
     * Callback when the user details are received.
     * @param body The UserDetail object.
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
            return <Tab id="settings-projects" title="Projects" className="settings-tab" panel={
                <Grid fluid>
                <Row>
                    <Col md={3}>
                        <H4>Project</H4>
                    </Col>
                    <Col md={1}>
                        {/* Placeholder */}
                    </Col>
                </Row>

                {this.state.projects.map((project: ProjectFull, index: number) =>
                    <SettingsProjectRowComponent settingsService={this.settingsService} project={project} refresh={this.refresh} handleEditOpen={this.handleEditProjectOpen} />
                )}
            </Grid>
            } />;
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
                <ProjectDialog project={this.state.projectEdit} isOpen={this.state.projectEdit !== null} close={this.handleEditProjectClose} userService={this.userService} />
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