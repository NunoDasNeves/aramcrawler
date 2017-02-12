from crawler.schema.common import *

SCHEMA = {
        'Champions': {
            'championId' : {
                'type': 'TINYINT UNSIGNED PRIMARY KEY'
            },
            'name': {
                'type': 'VARCHAR(64)'
            }
        },
        'Items': {
            'itemId' : {
                'type': 'INT UNSIGNED PRIMARY KEY'
            },
            'name' : {
                'type': 'VARCHAR(128)'
            }
        }
}
