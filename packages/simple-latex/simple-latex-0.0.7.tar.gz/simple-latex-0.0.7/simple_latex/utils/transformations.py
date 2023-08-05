def transform_dict_to_kv_list(options):
    """
    {"key": None, "key2": None} becomes 'key, key2'
    {"key": "\"\"", "key2": "3.5in", tocbibind: None} becomes 'key="", key2=3.5in, tocbibind'
    """
    assert isinstance(options, dict)
    return ", ".join(["{}={}".format(k,v) if v is not None else k for k,v in options.items()])
