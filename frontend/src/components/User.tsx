import * as React from "react";
import autobind from 'class-autobind';

import { FormGroup, InputGroup, ButtonGroup, Button, Intent, IToastProps } from "@blueprintjs/core";
import { Grid, Row, Col } from "react-flexbox-grid";
import { Formik } from 'formik';
import { APICaller } from "../helpers/userService";
import { PageProps } from "../helpers/props";
import { withRouter } from "react-router-dom";


export class LoginComponent extends React.PureComponent<PageProps> {
	private addToast: (toast: IToastProps, key?: string) => string;
	private apiCaller: APICaller;

	constructor(props: PageProps) {
		super(props);
        autobind(this);
		this.apiCaller = new APICaller(props.addToast, props.setLoggedIn);
		this.addToast = props.addToast;
	}

	protected doLogin(email: string, password: string) {
		this.apiCaller.login(email, password, (body) => {this.addToast({
			intent: Intent.SUCCESS,
			message: "You've been logged in.",
		})}, (body) => {this.addToast({
			intent: Intent.WARNING,
			message: "Please check your e-mail address and password.",
		})})
	}

	public render() {
		return <Grid fluid>
			<Row center="xs">
				<Col md={4}>
					<Formik
						initialValues={{ email: '', password: '' }}
						onSubmit={(values, { setSubmitting }) => {
							this.doLogin(values.email, values.password);
							setSubmitting(false);
						}}
					>
						{({ values, handleChange, handleBlur, handleSubmit, isSubmitting }) => (
								<form onSubmit={handleSubmit}>
									<FormGroup label="E-mail address" labelFor="email">
										<InputGroup type="text" id="email"
											onChange={handleChange}
											onBlur={handleBlur}
											value={values.email}
											placeholder="john.doe@example.com" />
									</FormGroup>
									<FormGroup label="Password" labelFor="password">
										<InputGroup type="password" id="password"
											onChange={handleChange}
											onBlur={handleBlur}
											value={values.password} />
									</FormGroup>
									<ButtonGroup minimal={true}>
										<Button text="Register" intent="primary" />
										<Button text="Login" intent="success" type="submit" disabled={isSubmitting} />
										<Button text="Forgot password" intent="warning" />
									</ButtonGroup>

								</form>
							)}
					</Formik>
				</Col>
			</Row>
		</Grid>;
	}
}

export const Login = withRouter(LoginComponent);