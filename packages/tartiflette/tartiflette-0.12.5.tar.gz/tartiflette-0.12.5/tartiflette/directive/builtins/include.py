from tartiflette import Directive
from tartiflette.types.exceptions.tartiflette import SkipExecution


class Include:
    async def on_field_execution(
        self, directive_args, next_resolver, parent_result, args, ctx, info
    ):
        if not directive_args["if"]:
            raise SkipExecution()

        return await next_resolver(parent_result, args, ctx, info)


def bake(schema_name, _config):
    sdl = "directive @include(if: Boolean!) on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT"

    Directive(name="include", schema_name=schema_name)(Include())

    return sdl
