import * as React from "react";
import { Navbar, Button, Alignment } from "@blueprintjs/core";
import { Link } from "react-router-dom";

export function ScoutNavbar() {
    return (
        <Navbar className={"scout-navbar"}>
            <Navbar.Group align={Alignment.LEFT}>
                <Navbar.Heading>Data Scout</Navbar.Heading>
                <Navbar.Divider />
                {/* <Link className="bp3-minimal" icon="home" to="/" />Home</Link>
                <Link className="bp3-minimal" icon="document" to="/" />Data Sources</Link>
                <Link className="bp3-minimal" icon="data-lineage" to="/about" />Flows</Link>
                <Link className="bp3-minimal" icon="help" to="/users" />Help</Link> */}
                <Link to="/"><Button className="bp3-minimal" icon="home" text="Home" /></Link>
                <Link to="/data_sources"><Button className="bp3-minimal" icon="document" text="Data Sources" /></Link>
                <Link to="/flows"><Button className="bp3-minimal" icon="data-lineage" text="Flows" /></Link>
                <Link to="/help"><Button className="bp3-minimal" icon="help" text="Help" /></Link>
            </Navbar.Group>
            <Navbar.Group align={Alignment.RIGHT}>
                <Button className="bp3-minimal" icon="projects" text="Projects" />
                <Navbar.Divider />
                <Button className="bp3-minimal" icon="cog" text="" />
                <Button className="bp3-minimal" icon="user" text="" />
            </Navbar.Group>
        </Navbar>
    );
}


