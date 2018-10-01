# -*- coding: utf-8 -*-
import json


def write_json_data(json_file_path, data, default_param=None, mode='w'):
        try:
            with open(json_file_path, mode) as f:
                f.write(
                    json.dumps(
                        data,
                        indent=4,
                        ensure_ascii=False,
                        default=default_param,
                        separators=(',', ': ')
                        )
                    )
        except IOError:
            raise Exception('Permission dinied')

