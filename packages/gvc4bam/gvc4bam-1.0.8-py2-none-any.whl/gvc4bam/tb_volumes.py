import unittest
import pprint

import gvc_vcf_pipeline

pp = pprint.PrettyPrinter()
class TEST_VOLUMES(unittest.TestCase):
    maxDiff=None
    def test_single(self):
        volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/db/ref/')
        self.assertDictEqual(volume,{'/disk':{
            'bind':'/disk',
            "mode": "rw"
        }})

    # def test_file(self):
    #     volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/db/ref/human.fa')
    #     self.assertDictEqual(volume,{'/disk/db/ref':{
    #         'bind':'/disk/db/ref',
    #         "mode": "rw"
    #     }})

    # def  test_repeat_files(self):
    #     volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/db/ref/human.fa','/disk/db/ref/')
    #     self.assertDictEqual(volume,{'/disk/db/ref':{
    #         'bind':'/disk/db/ref',
    #         "mode": "rw"
    #     }})

    # def  test_link_files_case0(self):
    #     volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/db/ref/human.fa','/disk/db/ref/','/disk/yinlh/docker3.0/gvc_lib/Model/PE100/Depth/')
    #     re_volume = {
    #         '/disk/db/ref':{
    #             'bind':'/disk/db/ref',
    #             "mode": "rw"
    #         },
    #         '/disk/yinlh/docker3.0/gvc_lib/Model/PE100/Depth':    
    #         {
    #             'bind':'/disk/yinlh/docker3.0/gvc_lib/Model/PE100/Depth',
    #             'mode': 'rw'
    #         },
    #         '/disk/gvcgroup/zhangzb/Model/v3.0/gvc_lib/Model_idcs/PE100/Depth':
    #         {
    #             'bind':'/disk/gvcgroup/zhangzb/Model/v3.0/gvc_lib/Model_idcs/PE100/Depth',
    #             'mode':'rw'
    #         }
    #     }
    #     #pp.pprint(volume)
    #     #pp.pprint(re_volume)
    #     self.assertDictEqual(volume,re_volume)

    # def test_link_files_case1(self):
    #     volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/yinlh/db/ref/')
    #     ret_volumes = {
    #         '/disk/db/ref':{
    #             'bind':'/disk/db/ref',
    #             "mode": "rw"
    #         },
    #         '/disk/yinlh/db/ref/':{
    #             'bind':'/disk/yinlh/db/ref/',
    #             "mode": "rw"
    #         },
    #      }

    # def test_link_files_case2(self):
    #     volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/yinlh/db/ref/human.fa')
    #     ret_volumes = {
    #         '/disk/db/ref':{
    #             'bind':'/disk/db/ref',
    #             "mode": "rw"
    #         },
    #         '/disk/yinlh/db/ref/':{
    #             'bind':'/disk/yinlh/db/ref/',
    #             "mode": "rw"
    #         },
    #      }

    # def test_relate_files(self):
    #     volume = gvc_vcf_pipeline.get_dynamic_volumes('/disk/yinlh/gvc_pre/../db/ref/human.fa')
    #     ret_volumes = {
    #         '/disk/db/ref':{
    #             'bind':'/disk/db/ref',
    #             "mode": "rw"
    #         },
    #         '/disk/yinlh/db/ref/':{
    #             'bind':'/disk/yinlh/db/ref/',
    #             "mode": "rw"
    #         },
    #      }       


if __name__ == "__main__":
    unittest.main()
