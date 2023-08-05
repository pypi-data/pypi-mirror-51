from collections import defaultdict


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class VariantInterface(Singleton):
    VariantDict = defaultdict(type(defaultdict()))

    def set_vcf(self, variant, mutantType, vcf):
        self.VariantDict[variant][mutantType] = vcf

    def set_cnv(self, *args):
        self.VariantDict['cnv'] = list(args)

    def get_variants(self):
        return self.VariantDict


class VariantFeature(Singleton):
    VariantDict = dict()

    def set_feature(self, variant, filename):
        self.VariantDict[variant] = filename

    def get_feature(self, variant):
        return self.VariantDict[variant]
