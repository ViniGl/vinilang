import re

class Pre_process:

    @staticmethod
    def filter(code):
        return re.sub('\/\*(\*(?!\/)|[^*])*\*\/', '', code)


