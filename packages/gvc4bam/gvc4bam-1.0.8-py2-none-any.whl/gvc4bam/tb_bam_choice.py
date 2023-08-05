import unittest
import gvc_vcf_pipeline

# NO time to Generate bam to test, so specify train1 test data


class TEST_BAM_LENGTH(unittest.TestCase):
    def test_Germline_100bp(self):
        group_infos = {'T': [
            '/disk/gvcgroup/fushun/20190227_Fq2VcfDockerTest/result/Germline/SRR1611178/T.sort.dup.bam']
        }
        self.assertEqual(100, gvc_vcf_pipeline.get_bam_lengths(group_infos))
    # Germline

    def test_Somatic_100bp(self):
        group_infos = {'T': [
            '/disk/gvcgroup/fushun/20190227_Fq2VcfDockerTest/result/Germline/SRR1611178/T.sort.dup.bam'],
            'N': ['/disk/gvcgroup/fushun/20190227_Fq2VcfDockerTest/result/Germline/SRR1611178/T.sort.dup.bam']
        }
        self.assertEqual(100, gvc_vcf_pipeline.get_bam_lengths(group_infos))

    def test_Germline_150bp(self):
        group_infos = {
            'T': ['/disk/gvcgroup/fushun/20190227_Fq2VcfDockerTest/result/Somatic/WES/Ct180554/N.sort.dup.bam']}

        self.assertEqual(150, gvc_vcf_pipeline.get_bam_lengths(group_infos))

    def test_Somatic_150bp(self):
        group_infos = {
            'N': ['/disk/gvcgroup/fushun/20190227_Fq2VcfDockerTest/result/Somatic/WES/Ct180554/N.sort.dup.bam'],
            'T': ['/disk/gvcgroup/fushun/20190227_Fq2VcfDockerTest/result/Somatic/WES/Ct180554/T.sort.dup.bam']}
        self.assertEqual(150, gvc_vcf_pipeline.get_bam_lengths(group_infos))

    def test_model_150(self):
        self.assertEqual('/disk/yinlh/docker3.0/gvc_lib//Model/PE150',
                         gvc_vcf_pipeline.get_model_path('/disk/yinlh/docker3.0/gvc_lib/', 150))

    def test_model_100(self):
        self.assertEqual('/disk/yinlh/docker3.0/gvc_lib//Model/PE100',
                         gvc_vcf_pipeline.get_model_path('/disk/yinlh/docker3.0/gvc_lib/', 100))


if __name__ == "__main__":
    unittest.main()
