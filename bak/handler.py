# coding: utf-8


class Handler(object):
    def __init__(self, signal, behavior):
        if not isinstance(behavior, (list, tuple)):
            behavior = [behavior]
        self.behavior = behavior

        if not isinstance(signal, (list, tuple)):
            signal = [signal]
        self.signal = signal

    def trigger(self, item, **env):
        for condition in self.condition:
            if not condition.evalute(item, **env):
                break
        else:
            for behavior in self.behavior:
                behavior.execute(item, **env)
