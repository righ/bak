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
        for signal in self.signal:
            if not signal.evalute(item, **env):
                break
        else:
            for behavior in self.behavior:
                behavior.execute(item, **env)
