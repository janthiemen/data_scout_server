import { IProps, IToastProps } from "@blueprintjs/core";

export interface PageProps extends IProps {
	addToast: (toast: IToastProps) => void;
	setLoggedIn: (loggedIn: boolean) => void;
}

