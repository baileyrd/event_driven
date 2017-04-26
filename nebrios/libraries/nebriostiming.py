

def prefixed_name(prefix, operation):
    if prefix == "":
        return operation
    else:
        return "%s_%s" % (prefix, operation)


def mark_start(bag, prefix="", instant=None):
    if instant is None or not isinstance(instant, datetime):
        instant = datetime.now()
    if isinstance(prefix, list):
        for p in prefix:
            mark_start(bag, prefix=p, instant=instant)
    elif isinstance(prefix, basestring):
        start_name = prefixed_name(prefix, "start")
        try:
            bag.__setitem__(start_name, instant)
        except Exception as e:
            raise Exception("Bag %s threw an exception during mark_start: %s" % (bag, e))
    else:
        raise Exception("Invalid prefix type %s for %s. Only strings or lists of strings allowed." % (type(prefix),
                        prefix))


def mark_end(bag, prefix="", instant=None):
    if instant is None or not isinstance(instant, datetime):
        instant = datetime.now()
    if isinstance(prefix, list):
        for p in prefix:
            mark_start(bag, prefix=p, instant=instant)
    elif isinstance(prefix, basestring):
        start_name = prefixed_name(prefix, "start")
        stop_name = prefixed_name(prefix, "stop")
        elapsed_name = prefixed_name(prefix, "elapsed")
        try:
            previous = bag.__getitem__(start_name)
            if previous is None:
                raise KeyError(start_name)
            bag.__setitem__(stop_name, instant)
            elapsed_delta = instant - previous
            bag.__setitem__(elapsed_name, elapsed_delta.total_seconds())
        except Exception as e:
            raise Exception("Bag %s threw an exception during mark_end: %s" % (bag, e))
    else:
        raise Exception("Invalid prefix type %s for %s. Only strings or lists of strings allowed." % (type(prefix),
                        prefix))
