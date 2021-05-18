import * as React from "react";
import { Navbar, Button, Alignment, ButtonGroup, MenuItem } from "@blueprintjs/core";
import { Link } from "react-router-dom";
import { DefaultItem, DefaultSelect, defaultSelectSettings, highlightText } from "../helpers/select";
import { ItemRenderer } from "@blueprintjs/select";

import autobind from 'class-autobind';
import { Dialog, Classes, Intent } from "@blueprintjs/core";
import { UserService, WranglerService } from "../helpers/userService";
import { BasePageProps, PageProps } from "../helpers/props";


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
}

// interface ScoutNavbarProps {
//     userService: UserService;
// }
interface ScoutNavbarState {
    userProjects: UserProject[];
    userProfile: UserProfile;
}

function createProject(title: string): UserProjectItem {
    return { title: title, id: null, label: "", role: "owner" }
}

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


export class ScoutNavbar extends React.Component<BasePageProps, ScoutNavbarState> {
    private userService: UserService;

    constructor(props: BasePageProps) {
        super(props);
        autobind(this);
        this.userService = new UserService(props.addToast, props.setLoggedIn, false);
        this.state = {
            userProjects: undefined,
            userProfile: undefined,
        };
        this.userService.getUserProjects(this.receiveUserProjects)
        this.userService.getUserProfile(this.receiveUserProfile)
    }

    private projectItemRenderer: ItemRenderer<UserProjectItem> = (item, { handleClick, modifiers, query }) => {
        if (!modifiers.matchesPredicate) {
            return null;
        }
        const text = `${item.title}`;
        return (
            <li>
                <ButtonGroup fill alignText={Alignment.LEFT}>
                    <Button onClick={handleClick} minimal fill>{highlightText(text, query)}</Button>
                    <Button minimal icon="cog"></Button>
                </ButtonGroup>
            </li>
        );
    };

    private setUserProject(userProject: UserProject): void {
        this.userService.setCurrentProject(this.state.userProfile.id, userProject.id);
        let userProjects = this.state.userProjects;
        userProjects.push(userProject);

        let userProfile = this.state.userProfile;
        userProfile.project = userProject;
        this.setState({ userProfile: userProfile, userProjects: userProjects });
    }

    private onProjectCreated(project: Project): void {
        this.userService.saveUserProject({id: null, project: project["id"], user: this.state.userProfile.id, role: "owner"}, this.setUserProject);
    }

    private onProjectChange(item: UserProjectItem): void {
        if (item.id === null) {
            this.userService.saveProject({id: null, name: item.title}, this.onProjectCreated)
        } else {
            this.setUserProject(this.state.userProjects.filter((userProject: UserProject) => userProject.id === item.id)[0]);
        }
    }
    
    protected receiveUserProjects(body: {}) {
        this.setState({userProjects: body["results"]});
    }

    protected receiveUserProfile(body: {}) {
        this.setState({userProfile: body["results"][0]});
    }


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

    private getUserMenu() {
        if (this.state.userProjects !== undefined && this.state.userProjects !== null) {
            let projects: UserProjectItem[] = this.state.userProjects.map((userProject: UserProject) => {
                return { title: userProject.project.name, id: userProject.id, label: "", role: userProject.role }
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
                <Button minimal icon="cog" text="" />
                <Button minimal icon="user" text="" />
            </Navbar.Group>;
        } else {
            return <></>;
        }
    }

    /**
     * Renders the navigation bar.
     * @returns  
     */
    render() {
        return <Navbar className={"scout-navbar"}>
                <Navbar.Group align={Alignment.LEFT}>
                    <Navbar.Heading>Data Scout</Navbar.Heading>
                    <Navbar.Divider />
                    {/* <Link className="bp3-minimal" icon="home" to="/" />Home</Link>
                    <Link className="bp3-minimal" icon="document" to="/" />Data Sources</Link>
                    <Link className="bp3-minimal" icon="data-lineage" to="/about" />Flows</Link>
                    <Link className="bp3-minimal" icon="help" to="/users" />Help</Link> */}
                    {this.getMenuItems()}
                </Navbar.Group>
                {this.getUserMenu()}
            </Navbar>;
        }
}








// function onProjectChange(item: DefaultItem) {
//     console.log(item);
// }

// export function ScoutNavbarf() {
//     let currentProject = "1";
//     let projects: DefaultItem[] = [
//         { title: "Test project", id: 1, label: "" },
//         { title: "Test project 2", id: 2, label: "" }
//     ]

//     return (
//         <Navbar className={"scout-navbar"}>
//             <Navbar.Group align={Alignment.LEFT}>
//                 <Navbar.Heading>Data Scout</Navbar.Heading>
//                 <Navbar.Divider />
//                 {/* <Link className="bp3-minimal" icon="home" to="/" />Home</Link>
//                 <Link className="bp3-minimal" icon="document" to="/" />Data Sources</Link>
//                 <Link className="bp3-minimal" icon="data-lineage" to="/about" />Flows</Link>
//                 <Link className="bp3-minimal" icon="help" to="/users" />Help</Link> */}
//                 <Link to="/"><Button className="bp3-minimal" icon="home" text="Home" /></Link>
//                 <Link to="/data_sources"><Button className="bp3-minimal" icon="document" text="Data Sources" /></Link>
//                 <Link to="/recipes"><Button className="bp3-minimal" icon="data-lineage" text="Flows" /></Link>
//                 <Link to="/help"><Button className="bp3-minimal" icon="help" text="Help" /></Link>
//             </Navbar.Group>
//             <Navbar.Group align={Alignment.RIGHT}>
//                 <DefaultSelect {...defaultSelectSettings} itemRenderer={projectItemRenderer} items={projects} onItemSelect={onProjectChange}>
//                     <Button minimal icon="projects" rightIcon="caret-down" text={"(No project selected)"} />
//                 </DefaultSelect>

//                 {/* <Button className="bp3-minimal" icon="projects" text="Projects" /> */}
//                 <Navbar.Divider />
//                 <Button minimal icon="cog" text="" />
//                 <Button minimal icon="user" text="" />
//             </Navbar.Group>
//         </Navbar>
//     );
// }


