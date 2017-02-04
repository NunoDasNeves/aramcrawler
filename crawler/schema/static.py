from crawler.schema.common import *

SCHEMA = {
        'Champions': {
            'championId' : {
                'type': 'PRIMARY KEY TINYINT UNSIGNED'
            },
            'name': {
                'type': 'KEY VARCHAR(64)'
            }
        },
        'Items': {
        }
}
