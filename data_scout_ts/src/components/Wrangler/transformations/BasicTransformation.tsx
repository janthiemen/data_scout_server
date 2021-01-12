import { IProps } from "@blueprintjs/core";

export interface TranformationProps extends IProps {
    newTransformation: (transformationType: string, kwargs: { [key: string]: any }) => void;
}
