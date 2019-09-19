string_field = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 255
}

comment = {
    'type': 'object',
    'required': ['text'],
    'properties': {
        'text': string_field,
    },
}
