#
class RadialFuncUnit:
    def name(self):
        return "1"

    def need_rb_corr(self):
        return True

    def second_order_moment_name(self):
        return "r^2"