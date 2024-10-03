import typer

app = typer.Typer()


def is_empty_value(value: str):
    return value == "" or value.isspace()


def validate_params_callback(values: list[str]):
    # input is a list of the parameter names and their values
    # empty by default if there are no params
    if values:
        param_names = set()
        for param_name_and_value in values:
            # check for the param_name=param_value syntax
            if "=" not in param_name_and_value:
                raise typer.BadParameter(
                    "Input passed in for --param should be of the form param_name=param_value. Your input is '{}'.".format(  # noqa E501
                        param_name_and_value
                    )
                )
            [param_name, param_value] = param_name_and_value.split("=", 1)
            # check that param_name and param_value are not empty
            if is_empty_value(param_name) or is_empty_value(param_value):
                raise typer.BadParameter("param_name and param_value cannot be empty.")
            # check uniqueness of param_name
            if param_name in param_names:
                raise typer.BadParameter(
                    "Duplicated for param_name: '{}'.".format(param_name)
                )
            param_names.add(param_name)
    return values


@app.command()
def main(param: list[str] = typer.Option([], callback=validate_params_callback)):
    processed_params = {}
    for param_name_and_value in param:
        [param_name, param_value] = param_name_and_value.split("=", 1)
        processed_params[param_name] = param_value
    print(processed_params)


if __name__ == "__main__":
    app()
