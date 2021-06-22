import './App.css';

import * as React from "react";

import { ScoutNavbar } from "./components/ScoutNavbar";
import { DataSources } from "./components/DataSource/DataSources";
import { Recipes } from "./components/Recipe/Recipes";
import { Settings } from "./components/Settings/Settings";
import { Login } from "./components/User";
import { Toaster, Position, IProps, IToastProps } from "@blueprintjs/core";
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import { Wrangler } from './components/Wrangler/Wrangler';


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
	private addToast(toast: IToastProps, key?: string): string {
		toast.timeout = 5000;
		return this.toaster.show(toast, key);
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
					<ScoutNavbar addToast={this.addToast} setLoggedIn={this.setLoggedIn} isLoggedIn={this.state.isLoggedIn}></ScoutNavbar>
					<Switch>
						<Route path="/wrangler/:recipe">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Wrangler addToast={this.addToast} setLoggedIn={this.setLoggedIn} />
						</Route>
						<Route path="/data_sources">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<DataSources addToast={this.addToast} setLoggedIn={this.setLoggedIn} isLoggedIn={this.state.isLoggedIn} />
						</Route>
						<Route path="/recipes">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Recipes addToast={this.addToast} setLoggedIn={this.setLoggedIn} isLoggedIn={this.state.isLoggedIn} />
						</Route>
						<Route path="/settings"> 
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Settings addToast={this.addToast} setLoggedIn={this.setLoggedIn} isLoggedIn={this.state.isLoggedIn} />
						</Route>
						<Route path="/login">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={false} />
							<Login addToast={this.addToast} setLoggedIn={this.setLoggedIn} isLoggedIn={this.state.isLoggedIn} />
						</Route>
						<Route path="/">
							<LoginRedirect isLoggedIn={this.state.isLoggedIn} loginRequired={true} />
							<Recipes addToast={this.addToast} setLoggedIn={this.setLoggedIn} isLoggedIn={this.state.isLoggedIn} />
						</Route>
					</Switch>
				</div>
			</Router>
		);
	}
}
