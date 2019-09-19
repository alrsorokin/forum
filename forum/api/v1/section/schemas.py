string_field = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 255
}

section = {
    'type': 'object',
    'required': ['theme', 'description'],
    'properties': {
        'theme': string_field,
        'description': string_field,
    },
}
