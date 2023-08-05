BASE_CONFIG = {
    'log': {
        'common': {
            'name': 'common',
            'level': 'info',
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
            'handlers': [
                {
                    'type': 'std',
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'level': 'info'
                }
            ]
        }
    }
}

SAMPLE_CONFIG = {
    'log': {
        'common': {
            'name': 'common',
            'level': 'info',
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
            'handlers': [
                {
                    'type': 'std',
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'level': 'info'
                },
                {
                    'type': 'file',
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'level': 'info',
                    'log_file': 'log/common.log'
                },
                {
                    'type': 'rotate',
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'level': 'info',
                    'log_file': 'log/common1.log', 'max_bytes': 1024},
                {
                    'type': 'time_rotate',
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'level': 'info',
                    'log_file': 'log/common2.log',
                    'when': 'h'
                }
            ]
        },
        'sample': {
            'name': 'sample',
            'level': 'debug',
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
            'handlers': [
                {
                    'type': 'std',
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'level': 'debug'
                }
            ]
        }
    }
}
