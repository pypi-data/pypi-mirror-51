import functools
import json

import click
import yaml
from click.exceptions import Exit
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup
from gradient.cli import cli_types

OPTIONS_FILE_PARAMETER_NAME = "options_file"


api_key_option = click.option(
    "--apiKey",
    "api_key",
    help="API key to use this time only",
)


def del_if_value_is_none(dict_, del_all_falsy=False):
    """Remove all elements with value == None"""
    for key, val in list(dict_.items()):
        if val is None or (del_all_falsy and not val):
            del dict_[key]


def jsonify_dicts(dict_):
    json_fields = [
        "envVars",
        "nodeAttrs"
    ]
    for field in json_fields:
        if field in dict_:
            dict_[field] = json.dumps(dict_[field])


class ClickGroup(DYMMixin, HelpColorsGroup):
    pass


def deprecated(msg):
    deprecated_invoke_notice = msg + """\nFor more information, please see:

https://docs.paperspace.com
If you depend on functionality not listed there, please file an issue."""

    def new_invoke(self, ctx):
        click.echo(click.style(deprecated_invoke_notice, fg='red'), err=True)
        super(type(self), self).invoke(ctx)

    def decorator(f):
        f.invoke = functools.partial(new_invoke, f)

    return decorator


def get_option_name(options_strings):
    for opt in options_strings:
        if not opt.startswith("-"):
            return opt

        if opt.startswith("--"):
            return opt[2:]


class ReadValueFromConfigFile(click.Parameter):
    def handle_parse_result(self, ctx, opts, args):
        config_file = ctx.params.get(OPTIONS_FILE_PARAMETER_NAME)
        if config_file:
            with open(config_file) as f:
                config_data = yaml.load(f, Loader=yaml.FullLoader)
                option_name = get_option_name(self.opts)
                value = config_data.get(option_name)
                if value is not None:
                    if isinstance(value, dict):
                        value = json.dumps(value)

                    opts[self.name] = value

        return super(ReadValueFromConfigFile, self).handle_parse_result(
            ctx, opts, args)


class ArgumentReadValueFromConfigFile(ReadValueFromConfigFile, click.Argument):
    pass


class OptionReadValueFromConfigFile(ReadValueFromConfigFile, click.Option):
    pass


def generate_options_template(ctx, param, value):
    if not value:
        return value

    params = {}
    for param in ctx.command.params:
        option_name = get_option_name(param.opts)
        option_value = ctx.params.get(param.name) or param.default

        if isinstance(param.type, cli_types.ChoiceType):
            for key, val in param.type.type_map.items():
                if val == option_value:
                    option_value = key

        params[option_name] = option_value

    with open(value, "w") as f:
        yaml.safe_dump(params, f, default_flow_style=False)

    raise Exit  # to stop execution without executing the command


def options_file(f):
    options = [
        click.option(
            "--optionsFile",
            OPTIONS_FILE_PARAMETER_NAME,
            help="Path to YAML file with predefined options",
        ),
        click.option(
            "--optionsFileTemplate",
            callback=generate_options_template,
            expose_value=False,
            help="Generate template options file"
        )
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)
