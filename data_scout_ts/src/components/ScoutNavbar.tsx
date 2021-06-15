import * as React from "react";
import { Navbar, Button, Alignment, ButtonGroup, MenuItem } from "@blueprintjs/core";
import { Link } from "react-router-dom";
import { DefaultItem, DefaultSelect, defaultSelectSettings, highlightText } from "../helpers/select";
import { ItemRenderer } from "@blueprintjs/select";

import autobind from 'class-autobind';
import { UserService } from "../helpers/userService";
import { BasePageProps } from "../helpers/props";
import { ProjectDialog } from "./ProjectDialog"


export interface User {
    id: number;
    username: string;
}

export interface ProjectFull {
    id: number;
    name: string;
    users: UserProjectFull[];
}


export interface UserProjectFull {
    id: number;
    user: User;
    role: string;
}

export interface Project {
    id: number;
    name: string;
}

export interface UserProject {
    id: number;
    project: Project;
    user: number;
    role: string;
}

export interface UserProfile {
    id: number;
    project: UserProject;
    user: number;
}

interface UserProjectItem extends DefaultItem {
    role: string;
    project: number;
}

interface ScoutNavbarState {
    userProjects: UserProject[];
    userProfile: UserProfile;
    projectEdit: number;
    isLoggedIn: boolean;
}

/**
 * Create a new project item.
 * @param title The title
 * @returns 
 */
function createProject(title: string): UserProjectItem {
    return { title: title, id: null, label: "", role: "owner", project: null }
}

/**
 * Render the create project menu item.
 * @param query The name of the new project
 * @param active 
 * @param handleClick 
 * @returns 
 */
function renderCreateProject(query: string, active: boolean, handleClick: React.MouseEventHandler<HTMLElement>) {
    return (
        <MenuItem
            icon="add"
            text={`Create "${query}"`}
            active={active}
            onClick={handleClick}
            shouldDismissPopover={false}
        />
    )
}

/**
 * A navbar containing the primary menu items as well as a user menu.
 * The navbar also handles project editing/creation.
 */
export class ScoutNavbar extends React.Component<BasePageProps, ScoutNavbarState> {
    private userService: UserService;

    constructor(props: BasePageProps) {
        super(props);
        autobind(this);
        this.userService = new UserService(props.addToast, props.setLoggedIn, false);
        this.state = {
            userProjects: undefined,
            userProfile: undefined,
            projectEdit: null,
            isLoggedIn: props.isLoggedIn
        };
        this.refresh();
    }

    /**
     * Refresh the navbar.
     */
    private refresh() {
        this.userService.getUserProjects(this.receiveUserProjects);
        this.userService.getUserProfile(this.receiveUserProfile);
    }

    /**
     * Called when new props are received.
     * @param props The new props
     */
    public componentWillReceiveProps(props: BasePageProps) {
        if (props.isLoggedIn != this.state.isLoggedIn) {
            this.refresh();            
        }
        this.setState({ isLoggedIn: props.isLoggedIn });
    }


    /**
     * Open the edit dialog.
     * @param project The id of the project.
     */
    private openProjectEdit(project: number) {
        this.setState({projectEdit: project});
    }

    /**
     * Render a project in the select list.
     * @returns 
     */
    private projectItemRenderer: ItemRenderer<UserProjectItem> = (item, { handleClick, modifiers, query }) => {
        if (!modifiers.matchesPredicate) {
            return null;
        }
        const text = `${item.title}`;
        return (
            <li>
                <ButtonGroup fill alignText={Alignment.LEFT}>
                    <Button onClick={handleClick} minimal fill>{highlightText(text, query)}</Button>
                    <Button minimal icon="cog" onClick={this.openProjectEdit.bind(this, item.project)}></Button>
                </ButtonGroup>
            </li>
        );
    };

    /**
     * Set the active user project.
     * @param userProject The user project.
     */
    private setUserProject(userProject: UserProject): void {
        this.userService.setCurrentProject(this.state.userProfile.id, userProject.id);
        let userProjects = this.state.userProjects;
        userProjects.push(userProject);

        let userProfile = this.state.userProfile;
        userProfile.project = userProject;
        this.setState({ userProfile: userProfile, userProjects: userProjects });
    }

    /**
     * Callback when the project has been created.
     * @param project The created project.
     */
    private onProjectCreated(project: Project): void {
        this.userService.saveUserProject({id: null, project: project["id"], user: this.state.userProfile.id, role: "owner"}, this.setUserProject);
    }

    /**
     * Called when the user selects a project.
     * @param item 
     */
    private onProjectChange(item: UserProjectItem): void {
        if (item.id === null) {
            // Create a project if it's new
            this.userService.saveProject({id: null, name: item.title}, this.onProjectCreated);
        } else {
            // Set the currently active project
            this.setUserProject(this.state.userProjects.filter((userProject: UserProject) => userProject.id === item.id)[0]);
        }
    }
    
    /**
     * Callback when the user projects are received.
     * @param body A list of user project objects
     */
    protected receiveUserProjects(body: {}) {
        this.setState({userProjects: body["results"]});
    }

    /**
     * Receive the user profile.
     * @param body The user profile
     */
    protected receiveUserProfile(body: {}) {
        this.setState({userProfile: body["results"][0]});
    }

    /**
     * Render the menu items in the navbar.
     * @returns 
     */
    private getMenuItems() {
        if (this.state.userProjects !== undefined && this.state.userProjects !== null) {
            return <>
                    <Link to="/"><Button className="bp3-minimal" icon="home" text="Home" /></Link>
                    <Link to="/data_sources"><Button className="bp3-minimal" icon="document" text="Data Sources" /></Link>
                    <Link to="/recipes"><Button className="bp3-minimal" icon="data-lineage" text="Flows" /></Link>
                    <Link to="/help"><Button className="bp3-minimal" icon="help" text="Help" /></Link>
            </>;
        } else {
            return <></>;
        }
    }

    /**
     * Render the user menu.
     * @returns 
     */
    private getUserMenu() {
        if (this.state.userProjects !== undefined && this.state.userProjects !== null) {
            let projects: UserProjectItem[] = this.state.userProjects.map((userProject: UserProject) => {
                return { title: userProject.project.name, id: userProject.id, label: "", role: userProject.role, project: userProject.project.id }
            });

            let activeProject = projects.filter(
                (userProject: UserProjectItem) => this.state.userProfile !== undefined && userProject.id === this.state.userProfile.project.id)[0];

            return <Navbar.Group align={Alignment.RIGHT}>
                <DefaultSelect {...defaultSelectSettings} itemRenderer={this.projectItemRenderer} items={projects} 
                    onItemSelect={this.onProjectChange} activeItem={activeProject} createNewItemFromQuery={createProject} 
                    createNewItemRenderer={renderCreateProject}>
                    <Button minimal icon="projects" rightIcon="caret-down" text={activeProject === undefined ? "(No project selected)" : activeProject.title} />
                </DefaultSelect>

                {/* <Button className="bp3-minimal" icon="projects" text="Projects" /> */}
                <Navbar.Divider />
                <Link to="/settings"><Button minimal icon="cog" text="" /></Link>
                {/* <Button minimal icon="cog" text="" /> */}
                <Button minimal icon="user" text="" />
            </Navbar.Group>;
        } else {
            return <></>;
        }
    }

    /**
     * Close the edit dialog.
     */
    protected closeProjectEdit() {
        this.setState({projectEdit: null});
    }

    /**
     * Renders the navigation bar.
     * @returns  
     */
    render() {
        return <>
            <ProjectDialog project={this.state.projectEdit} isOpen={this.state.projectEdit !== null} close={this.closeProjectEdit} userService={this.userService} />
            <Navbar className={"scout-navbar"}>
                <Navbar.Group align={Alignment.LEFT}>
                    <Navbar.Heading>Data Scout</Navbar.Heading>
                    <Navbar.Divider />
                    {this.getMenuItems()}
                </Navbar.Group>
                {this.getUserMenu()}
            </Navbar>
            </>;
        }
}
