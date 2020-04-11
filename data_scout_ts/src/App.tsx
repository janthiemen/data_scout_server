import './App.css';

// tslint:disable max-classes-per-file

import * as React from "react";

import { ScoutNavbar } from "./components/ScoutNavbar";
import { DataSources } from "./components/DataSource/DataSources";
import { Login } from "./components/User";
import { Toaster, Position, IProps, IToastProps } from "@blueprintjs/core";
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import { APICaller } from './helpers/userService';

// tslint:disable-next-line:no-var-requires
// import { DataTable } from "./components/DataTable";
// const sumo = require("./sumo.json") as any[];

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
	private apiCaller: APICaller;
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
		this.setState({isLoggedIn: isLoggedIn});
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
						<Route path="/data_sources">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<DataSources addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
							{/* <SelectExample /> */}
						</Route>
						<Route path="/login">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={false} />
							<Login addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
						<Route path="/">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
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