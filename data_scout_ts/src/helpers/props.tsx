import { Intent, IProps, IToastProps } from "@blueprintjs/core";
import { RouteComponentProps } from "react-router-dom";

export interface PageProps  extends RouteComponentProps<any>, IProps {
	addToast: (toast: IToastProps, key?: string) => string;
	setLoggedIn: (loggedIn: boolean) => void;
}

export const ConfirmDeleteProps = {
	canEscapeKeyCancel: true,
    canOutsideClickCancel: true,
    cancelButtonText: "No",
    confirmButtonText: "Yes",
    intent: Intent.DANGER
}