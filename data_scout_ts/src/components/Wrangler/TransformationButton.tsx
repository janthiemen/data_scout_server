import * as React from "react";
import autobind from 'class-autobind';
import { Button, ButtonGroup, Classes, Intent, Alert, Icon } from "@blueprintjs/core";

import { Transformation, transformationMakeTitle } from "./Transformation"

interface TransformationButtonProps {
    handleOpen: (transformation: Transformation) => void,
    deleteTransformation: (transformation: Transformation) => void,
    transformation: Transformation,
    index: number
}

interface TransformationButtonState {
    transformation: Transformation,
    index: number,
    isOpenDelete: boolean
}

export class TransformationButton extends React.PureComponent<TransformationButtonProps, TransformationButtonState> {
    private handleOpen: (transformation: Transformation) => void;
    private deleteTransformation: (transformation: Transformation) => void;
    
    constructor(props: TransformationButtonProps) {
        super(props);
        autobind(this);
        this.handleOpen = props.handleOpen;
        this.deleteTransformation = props.deleteTransformation;
        this.state = {
            transformation: props.transformation,
            index: props.index,
            isOpenDelete: false,
        }
        this.openDialog = this.openDialog.bind(this);
    }

    /**
     * Opens the transformation dialog
     */
    private openDialog() {
        this.handleOpen(this.state.transformation);
    }

    private handleDeleteAsk() {
        this.setState({ isOpenDelete: true });
    }

    private handleDeleteCancel() {
        this.setState({ isOpenDelete: false });
    }

    private handleDeleteConfirm() {
        this.deleteTransformation(this.state.transformation);
        this.setState({ isOpenDelete: false });
    }

    /**
     * Renders transformation button
     * @returns  
     */
    render() {
        let title = transformationMakeTitle(this.state.transformation);
        return <tr>
            <Alert
                canEscapeKeyCancel={true}
                canOutsideClickCancel={true}
                cancelButtonText="No"
                confirmButtonText="Yes"
                icon="trash"
                intent={Intent.DANGER}
                isOpen={this.state.isOpenDelete}
                onCancel={this.handleDeleteCancel}
                onConfirm={this.handleDeleteConfirm}
            >
                <p>Are you sure you want to delete <b>{title}</b>?</p>
            </Alert>
            <td><Icon icon="drag-handle-vertical" style={{"cursor": "grab"}}/></td>
            {/* <td>{this.state.index + 1}</td> */}
            <td>{title}</td>
            <td>
                <ButtonGroup vertical={false} fill={true} alignText="left">
                    <Button outlined intent={Intent.PRIMARY} rightIcon="edit" key={`transformation-edit-${this.state.index}`} onClick={this.openDialog} className={Classes.FIXED}></Button>
                    <Button outlined intent={Intent.DANGER} rightIcon="delete" key={`transformation-delete-${this.state.index}`} onClick={this.handleDeleteAsk} className={Classes.FIXED}></Button>
                </ButtonGroup>
            </td>
        </tr>
    }
}
