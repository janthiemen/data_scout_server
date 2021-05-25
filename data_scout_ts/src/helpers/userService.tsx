import { Intent, IToastProps } from "@blueprintjs/core";
import { Project, ProjectFull } from "../components/ScoutNavbar";
import { Transformation } from "../components/Wrangler/Transformation";

/**
 * The API caller handles all API requests to the Scout backend.
 */
export class APICaller {
    public addToast: (toast: IToastProps, key?: string) => string;
    public setLoggedIn: (loggedIn: boolean) => void;

    /**
     * Construct an API caller object. It will also check if the user is logged in on creation.
     * @param addToast Method to add a toast with
     * @param setLoggedIn Method to set if the user is logged in
     */
    constructor(addToast: (toast: IToastProps, key?: string) => string, setLoggedIn: (loggedIn: boolean) => void, doCheck: boolean = false) {
        this.addToast = addToast;
        this.call = this.call.bind(this);
        this.setLoggedIn = setLoggedIn;
        if (doCheck) {
            this.checkLoggedIn();
        }
    }

    /**
     * Check if the user is logged in.
     */
    public checkLoggedIn() {
        this.call("/scout/token/check/", "GET", {}, (body: {}) => {this.setLoggedIn(true);})
    }

    /**
     * Get the headers to make an API request.
     */
    private getHeaders(): {} {
        let access_token = localStorage.getItem("jwt_access_token");
        if (access_token !== undefined) {
            return {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            }
        } else {
            return {
                'Content-Type': 'application/json',
            }
        }
    }

    /**
     * Refresh the access token and then continue calling the API.
     * @param url The URL that should be called after the refresh
     * @param body The request body
     * @param callback The callback to be called after the token is refreshed
     */
    private refreshToken(url: string, type: string, body: {}, callback: (body: {}) => void) {
        // If we're refreshing we may assume that the old token is obsolete
        localStorage.removeItem("jwt_access_token");
        let refresh_token = localStorage.getItem("jwt_refresh_token");
        fetch('/scout/token/refresh/', {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify({ "refresh": refresh_token })
        })
            .then(r => r.json().then(data => ({ status: r.status, body: data })))
            .then((result) => {
                let status = result["status"];
                let body = result["body"];
                switch (status) {
                    case 401:
                        localStorage.removeItem("jwt_refresh_token");
                        this.setLoggedIn(false);
                        break;
                    case 200:
                        console.log(body);
                        localStorage.setItem("jwt_access_token", body["access"]);
                        this.call(url, type, body, callback, true);
                        break;
                    default:
                        this.addToast({ intent: Intent.DANGER, message: "An error occured!" })
                        this.setLoggedIn(false);
                        console.error(body);        
                }
            });
    }

    protected _prepareCall(type: string, body: {}, headers: {} = {}) {
        let properties;
        if (type === "GET") {
            properties = {method: type, headers: this.getHeaders()}
        } else if (body instanceof File) {
            properties = {method: type, headers: this.getHeaders(), body: body};
            properties["headers"]["Content-Type"] = "multipart/form-data";
        } else {
            properties = {method: type, headers: this.getHeaders(), body: JSON.stringify(body)};
        }

        for (let [key, value] of Object.entries(headers)) {
            properties["headers"][key] = value;
        }
        return properties;
    }

    public call(url: string, type: string, body: {}, callback: (body: {}) => void, wasRefreshed: boolean = false, headers: {} = {}) {
        /**
         * Call an API. This method handles authentication using JWT tokens (refreshing, etc.).
         * @param url: string: The URL to call
         */
        let properties = this._prepareCall(type, body, headers);

        fetch(url, properties)
            .then(r => r.json().then(data => ({ status: r.status, body: data })).catch(data => ({ status: r.status, body: {} })))
            .then((result) => {
                let status = result["status"];
                let body = result["body"];
                switch (status) {
                    case 401:
                        if (!wasRefreshed) {
                            this.refreshToken(url, type, body, callback);
                        } else {
                            this.setLoggedIn(false);
                        }
                        break;
                    default:
                        callback(body);
                        break;
                }

            })
            .then((error) => {
                // console.log("ERROR");
                // this.addToast({ intent: Intent.DANGER, message: "An error occured!" })
                // console.log(error);
            });
    }

    public callDownloadFile(url) {
        let properties = this._prepareCall("GET", {}, {});

        fetch(url, properties)
            .then(r => {
                let fileName = r.headers.get("content-disposition").replace("attachment; filename=", "");
                r.blob().then(blob => {
                    let url = window.URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = fileName;
                    a.click();
                });
            });
    }

    public login(email: string, password: string, callbackSuccess: (body: {}) => void, callbackError: (body: {}) => void) {
		fetch("/scout/token/", {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ "username": email, "password": password })
		})
			.then(res => res.json())
			.then(
				(result) => {
					localStorage.setItem('jwt_access_token', result["access"]);
					localStorage.setItem('jwt_refresh_token', result["refresh"]);
                    this.setLoggedIn(true);
                    callbackSuccess(result);
				},
				(error) => {
                    // console.log(error);
                    this.setLoggedIn(false);
					// callbackError(error);
				}
			)
	}

}

export class UserService extends APICaller {
    public getUsers(callback: (body: {}) => void) {
        this.call("/scout/api/user/", "GET", {}, callback);
    }

    public getUserProfile(callback: (body: {}) => void) {
        this.call("/scout/api/user_profile/", "GET", {}, callback);
    }

    public setUserProfile(callback: (body: {}) => void) {
        this.call("/scout/api/user_profile/", "GET", {}, callback);
    }

    public setCurrentProject(userProfileId: number, projectId: number) {
        this.call(`/scout/api/user_profile/${userProfileId}/?partial=1`, "PATCH", {"project": projectId}, this.finishSetUserProject);
    }

    public getUserProjects(callback: (body: {}) => void) {
        this.call("/scout/api/user_project/", "GET", {}, callback);
    }

    // TODO: Move this to its own service
    public getProject(project: number, callback: (body: ProjectFull) => void) {
        this.call(`/scout/api/project/${project}`, "GET", {}, callback);
    }

    public setUserProject(projectId) {
        this.call("/scout/api/user_project/", "PUT", {"project_id": projectId}, this.finishSetUserProject);
    }

    public finishSetUserProject(body: {}) {
        // TODO: Find a better way to do this!
        window.location.reload();
    }

    public saveProject(project: Project, callback: (body: {}) => void) {
        if (project["id"] > 0) {
            this.call(`/scout/api/project/${project["id"]}/`, "PUT", project, callback);
        } else {
            this.call("/scout/api/project/", "POST", project, callback);
        }
    }

    public saveUserProject(userProject: { [key: string]: any }, callback: (body: {}) => void) {
        console.log(userProject);
        if (userProject["id"] > 0) {
            this.call(`/scout/api/user_project/${userProject["id"]}/`, "PUT", userProject, callback);
        } else {
            this.call("/scout/api/user_project/", "POST", userProject, callback);
        }
    }

    public deleteUserProject(userProject: number, callback: (body: {}) => void) {
        this.call(`/scout/api/user_project/${userProject}/`, "DELETE", {}, callback);
    }

}

export class DataSourceService extends APICaller {

    getTypes(callback: (body: {}) => void) {
        this.call("/scout/datasource_types/", "GET", {}, callback);
    }

    get(callback: (body: {}) => void) {
        this.call("/scout/api/datasource/", "GET", {}, callback);
    }

    save(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/datasource/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/datasource/", "POST", data, callback);
        }
    }

    saveFile(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/datasource_file/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/datasource_file/", "POST", data, callback);
        }
    }

    uploadFile(file: File, id, callback: (body: {}) => void) {
        this.call(`/scout/api/datasource_file/${id}/upload`, "PUT", file, callback, false, {"Content-Disposition": `attachment; filename="${file.name}"`});
    }

    downloadUserFile(id) {
        this.callDownloadFile(`/scout/api/datasource_file/${id}/?output=file`);
    }

    delete(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/datasource/${id}/`, "DELETE", {}, callback);
    }

    getFolders(callback: (body: {}) => void) {
        this.call("/scout/api/datasourcefolder/?orphans_only=1", "GET", {}, callback);
    }

    saveFolder(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/datasourcefolder/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/datasourcefolder/", "POST", data, callback);
        }
    }

    deleteFolder(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/datasourcefolder/${id}/`, "DELETE", {}, callback);
    }
}


export class RecipeService extends APICaller {

    getDataSources(callback: (body: {}) => void) {
        this.call("/scout/api/datasource/", "GET", {}, callback);
    }

    getJoins(callback: (body: {}) => void) {
        this.call("/scout/api/join/", "GET", {}, callback);
    }

    get(callback: (body: {}) => void) {
        this.call("/scout/api/recipe/", "GET", {}, callback);
    }

    save(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/recipe/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/recipe/", "POST", data, callback);
        }
    }

    delete(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/recipe/${id}/`, "DELETE", {}, callback);
    }

    getFolders(callback: (body: {}) => void) {
        this.call("/scout/api/recipefolder/?orphans_only=1", "GET", {}, callback);
    }

    saveFolder(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/recipefolder/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/recipefolder/", "POST", data, callback);
        }
    }

    deleteFolder(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/recipefolder/${id}/`, "DELETE", {}, callback);
    }
}



export class WranglerService extends APICaller {

    get(callback: (body: {}) => void) {
        this.call("/scout/api/datasource/", "GET", {}, callback);
    }

    getRecipe(recipe: number, callback: (body: {}) => void) {
        this.call(`/scout/api/recipe/${recipe}/`, "GET", {}, callback);
    }

    getData(recipe: number, callback: (body: {}) => void) {
        // this.call(`/scout/data/${recipe}/${recipe_step}`, "GET", {}, callback);
        this.call(`/scout/data/${recipe}`, "GET", {}, callback);
    }

    putTransformation(id: number, data: Transformation, callback: (body: {}) => void) {
        this.call(`/scout/api/transformation/${id}/`, "PUT", data, callback);
    }

    putTransformationOrder(id: number, data: Transformation, callback: (body: {}) => void) {
        this.call(`/scout/api/transformation/${id}/`, "PUT", data, callback);
    }

    postTransformation(data: Transformation, callback: (body: {}) => void) {
        this.call(`/scout/api/transformation/`, "POST", data, callback);
    }

    deleteTransformation(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/transformation/${id}/`, "DELETE", {}, callback);
    }

    save(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/datasource/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/datasource/", "POST", data, callback);
        }
    }

    delete(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/datasource/${id}/`, "DELETE", {}, callback);
    }

    getDefinition(recipe: number, callback: (body: {}) => void) {
        this.call(`/scout/pipeline/${recipe}`, "GET", {}, callback);
    }

    downloadCode(id) {
        this.callDownloadFile(`/scout/pipeline/${id}/?output=python`);
    }
}


export class JoinService extends APICaller {

    get(callback: (body: {}) => void) {
        this.call("/scout/api/join/", "GET", {}, callback);
    }

    getDataSources(callback: (body: {}) => void) {
        this.call("/scout/api/datasource/", "GET", {}, callback);
    }

    getRecipes(callback: (body: {}) => void) {
        this.call("/scout/api/recipe/", "GET", {}, callback);
    }

    save(data: { [key: string]: any }, callback: (body: {}) => void) {
        if (data["id"] > 0) {
            this.call(`/scout/api/join/${data["id"]}/`, "PUT", data, callback);
        } else {
            this.call("/scout/api/join/", "POST", data, callback);
        }
    }

    delete(id: number | string, callback: (body: {}) => void) {
        this.call(`/scout/api/join/${id}/`, "DELETE", {}, callback);
    }
}
