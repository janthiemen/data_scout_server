interface TransformationMeta {
    title: string
    fields: { [key: string]: { [key: string]: any } },
}

// TODO: Load the meta data from the server
export const TRANSFORMATIONS: { [key: string]: TransformationMeta } = {
    "convert": {
        "title": "Convert {field} to {to}",
        "fields": {
            "field": {
                "name": "Column", "type": "string", "help": "The field to convert", "required": true,
                "input": "column", "multiple": false, "default": ""
            },
            "to": {
                "name": "To", "type": "string", "help": "To which data type to convert", "required": true,
                "input": "select", "multiple": false, "default": "",
                "options": { "int": "Integer", "float": "Floating point number", "string": "Text" }
            }
        }
    },
    "add": {
        "title": "Sum {fields}",
        "fields": {
            "fields": {
                "name": "Columns", "type": "list<string>", "help": "The fields to add to each other",
                "required": true, "input": "column", "multiple": true, "default": []
            },
            "output": {
                "name": "Output column", "type": "string", "input": "text", "required": true,
                "help": "The name of the (newly created) column that contains the results", "default": ""
            },
        }
    },
    "min": {
        "title": "Calculate {field_a} - {field_b}",
        "fields": {
            "field_a": {
                "name": "Field 1", "type": "string", "help": "The field that should be subtracted from",
                "required": true, "input": "column", "multiple": false, "default": ""
            },
            "field_b": {
                "name": "Field 2", "type": "string", "help": "The field that should be subtracted",
                "required": true, "input": "column", "multiple": false, "default": ""
            },
            "output": {
                "name": "Output column", "type": "string", "input": "text", "required": true, "default": "",
                "help": "The name of the (newly created) column that contains the results"
            },

        }
    },
    "multiply": {
        "title": "Multiply {fields}",
        "fields": {
            "fields": {
                "name": "Columns", "type": "list<string>", "help": "The fields to add to each other",
                "required": true, "input": "column", "multiple": true, "default": []
            },
            "output": {
                "name": "Output column", "type": "string", "input": "text", "required": true,
                "help": "The name of the (newly created) column that contains the results", "default": ""
            }
        }
    },
    "divide": {
        "title": "Calculate {field_a} / {field_b}",
        "fields": {
            "field_a": {
                "name": "Numerator", "type": "string", "help": "The numerator",
                "required": true, "input": "column", "multiple": false, "default": ""
            },
            "field_b": {
                "name": "Denominator", "type": "string", "help": "The denominator",
                "required": true, "input": "column", "multiple": false, "default": ""
            },
            "output": {
                "name": "Output column", "type": "string", "input": "text", "required": true, "default": "",
                "help": "The name of the (newly created) column that contains the results"
            },

        }
    }

}

export interface Transformation {
    id: number,
    kwargs: string,
    previous: number | null,
    next?: number[],
    recipe: number,
    transformation: string,
}

export function transformationMakeTitle(transformation: Transformation): string {
    let title = transformation.transformation;
    let kwargs = JSON.parse(transformation.kwargs);
    if (title in TRANSFORMATIONS) {
        title = TRANSFORMATIONS[title]["title"].replace(/{(\w+)}/g, function (_, k) {
            return kwargs[k];
        });
    }
    return title;
}
