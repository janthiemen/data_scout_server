import { IProps, IToastProps } from "@blueprintjs/core";
import { RouteComponentProps } from "react-router-dom";

export interface PageProps  extends RouteComponentProps<any>, IProps {
	addToast: (toast: IToastProps) => void;
	setLoggedIn: (loggedIn: boolean) => void;
}

