import './App.css';

import * as React from "react";

import { ScoutNavbar } from "./components/ScoutNavbar";
import { DataSources } from "./components/DataSource/DataSources";
import { Recipes } from "./components/Recipe/Recipes";
import { Login } from "./components/User";
import { Toaster, Position, IProps, IToastProps, HTMLTable } from "@blueprintjs/core";
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import { Wrangler } from './components/Wrangler/Wrangler';

import { ReactSortable } from "react-sortablejs";

interface BasicClassState {
	list: { id: string; name: string }[];
}

export class BasicClass extends React.Component<{}, BasicClassState> {
	state: BasicClassState = {
		list: [{ id: "1", name: "shrek" }, { id: "2", name: "fiona" }]
	};
	render() {
		return (
			<HTMLTable striped={true}>
				<tbody>
					<ReactSortable
						list={this.state.list}
						setList={newState => this.setState({ list: newState })}
					>
						{this.state.list.map(item => (
							<tr><td>{item.id}</td><td>{item.name}</td><td>{item.name}</td></tr>
						))}
					</ReactSortable>
				</tbody>
			</HTMLTable>
		);
	}
}

interface LoginRedirectProps extends IProps {
	isLoggedIn: boolean;
	loginRequired: boolean;
}

function LoginRedirect(props: LoginRedirectProps) {
	if (!props.isLoggedIn && props.loginRequired) {
		return <Redirect to='/login' />;
	}
	if (props.isLoggedIn && !props.loginRequired) {
		return <Redirect to='/' />;
	}
	return <span></span>;
}

export default class App extends React.Component<IProps> {
	private toaster: Toaster;
	private refHandlers = {
		toaster: (ref: Toaster) => (this.toaster = ref),
	};
	public state = {
		isLoggedIn: true
	}

	constructor(props: IProps) {
		super(props);
		this.addToast = this.addToast.bind(this);
		this.setLoggedIn = this.setLoggedIn.bind(this);
	}

	/**
	 * Add a toast.
	 * @param toast The Blueprint.js toast properties
	 */
	private addToast(toast: IToastProps) {
		toast.timeout = 5000;
		this.toaster.show(toast);
	}

	/**
	 * Set the logged in status of the user.
	 * @param isLoggedIn Is the user logged in or not?
	 */
	private setLoggedIn(isLoggedIn: boolean) {
		this.setState({ isLoggedIn: isLoggedIn });
	}

	render() {
		return (
			<Router>
				<div>
					<Toaster autoFocus={false} canEscapeKeyClear={true} position={Position.TOP} ref={this.refHandlers.toaster} />
					<ScoutNavbar></ScoutNavbar>
					<Switch>
						<Route path="/about">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<About />
						</Route>
						<Route path="/wrangler/:recipe">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Wrangler addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
						<Route path="/data_sources">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<DataSources addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
						<Route path="/recipes">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Recipes addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
						<Route path="/login">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={false} />
							<Login addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
						<Route path="/">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Recipes addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
					</Switch>
				</div>
			</Router>
		);
	}
}

function About() {
	return <h2>About</h2>;
}