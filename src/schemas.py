from src.deps.ma import ma

paginated_schema_cache: dict = {}


class EmptySchema(ma.Schema):
    pass


class HTTPRequestSchema(ma.Schema):
    """
    Schema for http request response

    Details:
        code = Status Code
        message = Status Message
        description = API Response Description
    """

    code = ma.Int()
    message = ma.Str()
    description = ma.Str()
