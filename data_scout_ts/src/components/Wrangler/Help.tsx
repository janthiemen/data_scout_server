import * as React from "react";

import { Drawer, Position, IProps, Button } from "@blueprintjs/core";

interface HelpState {
    autoFocus: boolean;
    canEscapeKeyClose: boolean;
    canOutsideClickClose: boolean;
    enforceFocus: boolean;
    hasBackdrop: boolean;
    isOpen: boolean;
    position?: Position;
    size?: string;
    usePortal: boolean;
    title: string;
    content: string;
}

interface HelpProps extends IProps {
    page: string;
}

export class Help extends React.PureComponent<HelpProps, HelpState> {
    public state: HelpState;

    constructor(props: HelpProps) {
        super(props);
        if (props.page === "sampling") {
            this.state = {
                autoFocus: true,
                canEscapeKeyClose: true,
                canOutsideClickClose: true,
                enforceFocus: true,
                hasBackdrop: true,
                isOpen: false,
                position: Position.RIGHT,
                size: undefined,
                usePortal: true,
                title: "Sampling",
                content: "TODO: This is a help page about the sampling methodology"
            }
        } else {
            this.state = {
                autoFocus: true,
                canEscapeKeyClose: true,
                canOutsideClickClose: true,
                enforceFocus: true,
                hasBackdrop: true,
                isOpen: false,
                position: Position.RIGHT,
                size: undefined,
                usePortal: true,
                title: this.props.page,
                content: `TODO: This is a help page about the ${this.props.page}`
            }
        }
    }

    private handleOpen = () => this.setState({ isOpen: true });
    private handleClose = () => this.setState({ isOpen: false });

    render() {
        return <span>
            <Button icon="help" onClick={this.handleOpen} minimal={true} />
            <Drawer
                icon="help"
                onClose={this.handleClose}
                {...this.state}
            >
                <div>
                    <div>
                        <p>{this.state.content}</p>
                    </div>
                </div>
            </Drawer>
        </span>
    }
}