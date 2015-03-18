# coding: utf-8


class Handler(object):
    def __init__(self, behavior, conditions):
        self.behavior = behavior
        self.conditions = conditions

    def trigger(self, item, **env):
        for condition in self.conditions:
            if not condition.evalute(item, **env):
                break
        else:
            self.behavior.execute(item, **env)
