from openomics.database.annotation import Annotatable
from openomics.transcriptomics import ExpressionData


class SomaticMutation(ExpressionData, Annotatable):
    def __init__(self, cohort_name, index, file_path, columns="GeneSymbol|TCGA", genes_col_name="GeneSymbol",
                 transposed=True, log2_transform=False):
        super(SomaticMutation, self).__init__(cohort_name, index, file_path, columns=columns,
                                              genes_col_name=genes_col_name,
                                              transposed=transposed, log2_transform=log2_transform)
    @classmethod
    def name(cls):
        return cls.__name__


class DNAMethylation(ExpressionData):
    def __init__(self, cohort_name, index, file_path, columns="GeneSymbol|TCGA", genes_col_name="GeneSymbol",
                 transposed=True, log2_transform=False):
        super(DNAMethylation, self).__init__(cohort_name, index, file_path, columns=columns,
                                             genes_col_name=genes_col_name,
                                             transposed=transposed, log2_transform=log2_transform)

    @classmethod
    def name(cls):
        return cls.__name__


class CopyNumberVariation(ExpressionData, Annotatable):
    def __init__(self, cohort_name, index, file_path, columns="GeneSymbol|TCGA", genes_col_name="GeneSymbol",
                 transposed=True, log2_transform=False):
        super(CopyNumberVariation, self).__init__(cohort_name, index, file_path, columns=columns,
                                                  genes_col_name=genes_col_name,
                                                  transposed=transposed, log2_transform=log2_transform)

    @classmethod
    def name(cls):
        return cls.__name__
