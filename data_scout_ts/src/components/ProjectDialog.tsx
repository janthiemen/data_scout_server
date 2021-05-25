import * as React from "react";
import autobind from 'class-autobind';
import { Dialog, Classes, Button, Intent, FormGroup, InputGroup, ControlGroup, HTMLSelect } from "@blueprintjs/core";
import { UserService } from "../helpers/userService";
import { Project, ProjectFull, User, UserProject, UserProjectFull } from "./ScoutNavbar";
import { DefaultItem, DefaultSelect, defaultSelectSettings } from "../helpers/select";


interface ProjectDialogProps {
    userService: UserService;
    project: number;
    isOpen: boolean;
    close: () => void;
}
interface ProjectDialogState {
    project: ProjectFull;
    isOpen: boolean;
    definition: string;
    users: User[];
    newUserProject: {user: User, role: string};
}

export class ProjectDialog extends React.Component<ProjectDialogProps, ProjectDialogState> {
    private userService: UserService;
    private close: () => void;

    constructor(props: ProjectDialogProps) {
        super(props);
        autobind(this);
        this.userService = props.userService;
        this.close = props.close;
        this.state = {
            newUserProject: { user: undefined, role: "" },
            project: { id: null, name: "", users: [] },
            isOpen: props.isOpen,
            users: [],
            definition: ""
        };
        this.requestProject(props.project);
        this.userService.getUsers(this.receiveUsers);
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    componentWillReceiveProps(props: ProjectDialogProps) {
        this.setState({
            isOpen: props.isOpen
        });
        this.requestProject(props.project);
    }

    private requestProject(project: number) {
        if (project !== null && project !== undefined) {
            this.userService.getProject(project, this.receiveProject);
        }
    }

    private refreshProject(body: {}) {
        this.requestProject(this.state.project.id);
    }

    private receiveProject(body: ProjectFull) {
        this.setState({ project: body })
    }

    private receiveUsers(body: {[key: string]: any}) {
        this.setState({ users: body["results"] });
    }

    private getUsers(): UserProjectFull[] {
        if (this.state.project !== undefined) {
            return this.state.project.users;
        } else {
            return [];
        }
    }

    private handleDelete(userProject: number) {
        console.log(userProject);
        this.userService.deleteUserProject(userProject, this.refreshProject)
    }

    private selectUser(user: DefaultItem) {
        let newUserProject = this.state.newUserProject;
        newUserProject.user = {"id": user.id, "username": user.title}
        this.setState({ newUserProject: newUserProject });
    }

    private selectRole(event: React.ChangeEvent<HTMLSelectElement>) {
        let newUserProject = this.state.newUserProject;
        newUserProject.role = event.target.value;
        this.setState({ newUserProject: newUserProject });
    }

    private addUser() {
        this.userService.saveUserProject({
                id: null, 
                project: this.state.project.id, 
                user: this.state.newUserProject.user.id, 
                role: this.state.newUserProject.role
            }, this.refreshProject);
    }

    private renderUserProject(userProject: UserProjectFull) {
        return <tr>
            <td>{userProject.user.username}</td>
            <td>{userProject.role}</td>
            <td>
                {this.renderDelete(userProject)}
            </td>
        </tr>
    }

    private renderDelete(userProject: UserProjectFull) {
        if (userProject.role !== "owner") {
            // TODO: Remove the delete button if the current user is not an admin or owner
            return <Button outlined intent={Intent.DANGER} rightIcon="delete"
                onClick={this.handleDelete.bind(this, userProject.id)}
                key={`userproject-delete-${userProject.id}`}
                className={Classes.FIXED}></Button>;
        } else {
            return <></>;
        }
    }

    private updateName(event: React.ChangeEvent<HTMLInputElement>) {
        let project = this.state.project;
        project.name = event.target.value;
        this.setState({ project: project });
    }

    /**
     * Renders export dialog.
     * @returns  
     */
    render() {
        let userItems: DefaultItem[] = this.state.users.map((user: User) => {
            return { title: user.username, id: user.id, label: "" }
        });


        return <Dialog icon="data-lineage" title="Pipeline definition" isOpen={this.state.isOpen} onClose={this.close}>
            <div className={Classes.DIALOG_BODY}>
                Project
                <FormGroup label="Name" labelFor="name" labelInfo="(required)" helperText="The human readable name of the project">
                    <InputGroup id="name" placeholder="Placeholder text" onChange={this.updateName} value={this.state.project.name} />
                </FormGroup>

                <br />
                <ControlGroup>
                    <DefaultSelect {...defaultSelectSettings} items={userItems} onItemSelect={this.selectUser}>
                        <Button icon="user" rightIcon="caret-down" 
                                text={this.state.newUserProject.user === undefined ? "(Select a user)" : this.state.newUserProject.user.username} />
                    </DefaultSelect>
                    <HTMLSelect options={["(Select a role)", "editor", "admin", "owner"]} onChange={this.selectRole} />
                    <Button rightIcon="add" onClick={this.addUser}></Button>
                </ControlGroup>

                <table className="bp3-html-table bp3-interactive" style={{ "width": "100%" }}>
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Role</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.getUsers().map((userProject: UserProjectFull, index: number) => this.renderUserProject(userProject))}
                    </tbody>
                </table>
            </div>
        </Dialog >
    }
}
