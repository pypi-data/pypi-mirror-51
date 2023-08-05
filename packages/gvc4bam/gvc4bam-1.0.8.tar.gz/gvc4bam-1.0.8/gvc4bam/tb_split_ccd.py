
import unittest


import gvc_pipeline


class TestSplitMethod(unittest.TestCase):

    def test_split_method(self):
        input_regions = [['1',400,500],
                        ['2',5000,6000],
                        ['2',6010,7000]
                        ]
        self.assertListEqual(input_regions,
            gvc_pipeline.split_ccd(input_regions,500))
        input_regions = [['1',400,500],
                        ['2',5000,5020],
                        ['2',5030,5035],
                        ['3',5030,5035]
                        ]
        output_regions = [['1',400,500],
                        ['2',5000,5035],
                        ['3',5030,5035]
                        ]
        self.assertListEqual(output_regions,
            gvc_pipeline.split_ccd(input_regions,500))

    def test_split_method_WGS(self):
        refernces = ['1']
        lens = [23]
        output = [['1',1,5],['1',6,10],['1',11,15],['1',16,20],['1',21,23
        ]]
        self.assertListEqual(output,gvc_pipeline.split_reference(refernces,lens,5))
        refernces = ['1','2']
        lens = [500,600]
        output = [['1',1,500],['2',1,500],['2',501,600]]
        self.assertListEqual(output,gvc_pipeline.split_reference(refernces,lens,500))

    def test_filter_bed(self):
        input_regions = [['1',400,500],
                        ['fake_name_too_long',5000,5020],
                        ['2',5030,5035],
                        ['fake_name_too_long',5030,5035]
                        ]
        output = [['1',400,500],['2',5030,5035]]
        self.assertListEqual(output,gvc_pipeline.filter_bed(input_regions,10))
        int_ref = ['fake_name_too_long','1','fake_name_too_long','2']
        int_lens =[0,1,3,4]
        out_ref ,out_lens = gvc_pipeline.filter_references(int_ref,int_lens,10)
        self.assertListEqual(out_ref,['1','2'])
        self.assertListEqual(out_lens,[1,4])

if __name__ == "__main__":
    unittest.main()