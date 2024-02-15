import unittest
from hl7validator.api import hl7validatorapi


class TestHL7Validator(unittest.TestCase):
    def test_hl7validator_incorrect(self):
        """
        Tests a incorrect HL7v2 Message
        :return:
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\nEVN|A34\nPID|||JMS17131790^^^JMS^NS|*********^^^***^**~***********^^^*******|*******^*******^***********||**************|*|||****************************^^******^^********^*||^^^****************************^^^*********||||||*********|||||||||||N\nMRG|JMS61226892^^^JMS^NS||||||********^***********^********* **** ****"
        response = hl7validatorapi(data)
        print(response)
        # self.assertEqual(assess_elements(response), True)

        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct(self):
        """
        Tests a correct HL7v2 Message
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\nEVN|A34|wewe\nPID|||JMS17131790^^^JMS^NS|256886210^^^NIF^PT~C3709807001^^^N_BENEF|ALMEIDA^BEATRIZ^DELMAR NETO||20060523000000|F|||ESTRADA DA CAPELEIRA, No 9 B^^OBIDOS^^2510-018^1||^^^SONIAMMNALMEIDA@HOTMAIL.COM^^^935200945||||||270858182|||||||||||N\nMRG|JMS61226892^^^JMS^NS||||||ALMEIDA^BEATRIZ^DELMAR NETO DE"

        response = hl7validatorapi(data)
        # self.assertEqual(assess_elements(response), True)
        print(response)

        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_correct_with_r(self):
        """
        Tests a correct HL7v2 Message
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\rEVN|A34|wewe\rPID|||JMS17131790^^^JMS^NS|256886210^^^NIF^PT~C3709807001^^^N_BENEF|ALMEIDA^BEATRIZ^DELMAR NETO||20060523000000|F|||ESTRADA DA CAPELEIRA, No 9 B^^OBIDOS^^2510-018^1||^^^SONIAMMNALMEIDA@HOTMAIL.COM^^^935200945||||||270858182|||||||||||N\rMRG|JMS61226892^^^JMS^NS||||||ALMEIDA^BEATRIZ^DELMAR NETO DE"

        response = hl7validatorapi(data)
        # self.assertEqual(assess_elements(response), True)
        print(response)

        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_incorrect2(self):
        """
        Tests a correct HL7v2 Message
        """
        data = (
            """MSH|^~\&|KEANE|Sacred Heart|||20090601103638||ADT^A08|JPANUCCI-0091|T|2.2|5109
EVN|A08|20090601103638|||ad.kfuj
PID|1|540091|540091||Panucci^John^||19490314|M||2106-3|33 10th Ave.^^Costa Mesa^CA^92330^US^B||(714) 555-0091^^HOME SO~||ENG|M|CAT|540091|677-47-2055||
NK1|1|CEHOLJIMCADC^BIMA|HU|7056 QEXNON ILY^""^FICIHXEV^DI^24062|(234)211-4615|""
NK1|2|""^""|""|""^""^""^""^""|""|""
PV1||O|Z27|U|||16^VAN HOUTEN^KIRK^|11^FLANDERS^NED^|14^VAN HOUTEN^MILLHOUSE^|SUR||||1|| |005213^KURZWEIL^PETER^R|O||MA||||||||||||||||""|||SIMPSON CLINIC|||||200906011027
PV2||""|""^MENISCUS TEAR RIGHT KNEE|||||""||||EKG/LAB|||||||||""
GT1|1||CEHOLJIMCADC^ROZOCZ^M||7056 QEXNON ILY^""^FICIHXEV^DI^24062|(234)211-4615|||||SEL|677-47-2055||||DISABLED
IN1|1|MB|0011|MEDICARE    OP ONLY MCR M|||||""
IN1|2|MSCP|0I38|MEM SENIOR  COMPPLN IND I|||||"""
            ""
        )
        response = hl7validatorapi(data)
        print(response)

        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct2(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|EPIC|LAMH|KEANE|KEANE|20090601115851|I000007|ADT^A60|AWONG-0025|P|2.4|||
EVN|A60|200906011158|||I000007^INTERFACE^ADT^^^^^^M^^^^^LAMH
PID||111987|111987||Wong^Amy^||19810902|F||2028-9|999 NINE AVE^^LONG BEACH^CA^90745^US^H||(562)555-0025^^M||ENG|M|BUD|LBACT0025|730-85-8464|||||||||||N
PV1||O|ZBC||||7^SIMPSON^MARGE^|18^WIGGUM^RALPH^|2^MOUSE^M^|MED|||||||000819^LEE VOGT^JUDY^K|O|824477665||||||||||||||||||||SIMPSON CLINIC||N|||||||||210010404670
PV2|||^ANNUAL SCREENING MAMMOGRAM|||||20090602||||||||||||||N
IAM|1|FA^PEANUTS^ELG|FA^PEANUTS|||A|123|||||||||||I000007^INTERFACE^ADT
"""
        response = hl7validatorapi(data)
        # self.assertEqual(assess_elements(response), True)
        print(response)

        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_incorrect3(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|TESTLAB1|INDEPENDENT LAB SERVICES^LABCLIANUM^CLIA|||200404281339||ORU^R01|2004042813390045|P|2.3.1|||||||||2.0
PID|1||123456789^^^^SS|000039^^^^LR|McMuffin^Candy^^^Ms.||19570706|F||2106-3|495 East Overshoot Drive^^Delmar^NY^12054||^^^^^518^5559999|||M|||4442331235
ORC|RE||||||||||||||||||||General Hospital^^123456^^^AHA|857 Facility Lane^^Albany^NY^12205|^^^^^518^3334444|100 Provider St^^Albany^NY^12205
OBR|1||S91-1700|22049-1^cancer identification battery^LN|||20040720||||||||^left breast mass|1234567^Myeolmus^John^^MD|(518)424-4243||||||||F|||||||99999&Glance&Justin&A&MD
OBX|1|TX|22636-5^clinical history^LN||47-year old white female with (L) UOQ breast mass||||||F|||20040720
OBX|2|ST|22633-2^nature of specimen^LN|1|left breast biopsy||||||F|||20040720
OBX|3|ST|22633-2^nature of specimen^LN|2|apical axillary tissue||||||F|||20040720
OBX|4|ST|22633-2^nature of specimen^LN|3|contents of left radical mastectomy||||||F|||20040720
OBX|5|TX|22634-0^gross pathology^LN|1|Part #1 is labeled "left breast biopsy" and is received fresh after frozen section preparation. It consists of a single firm nodule measuring 3cm in circular diameter and 1.5cm in thickness surrounded by adherent fibrofatty tissue. On section a pale gray, slightly mottled appearance is revealed. Numerous sections are submitted for permanent processing.||||||F|||20040720
OBX|6|TX|22634-0^gross pathology^LN|2|Part #2 is labeled "apical left axillary tissue" and is received fresh. It consists of two amorphous fibrofatty tissue masses without grossly discernible lymph nodes therein. Both pieces are rendered into numerous sections and submitted in their entirety for history.||||||F|||20040720
OBX|7|TX|22634-0^gross pathology^LN|3|Part #3 is labeled "contents of left radical mastectomy" and is received flesh. It consists of a large ellipse of skin overlying breast tissue, the ellipse measuring 20cm in length and 14 cm in height. A freshly sutured incision extends 3cm directly lateral from the areola, corresponding to the closure for removal of part #1. Abundant amounts of fibrofatty connective tissue surround the entire beast and the deep aspect includes and 8cm length of pectoralis minor and a generous mass of overlying pectoralis major muscle. Incision from the deepest aspect of the specimen beneath the tumor mass reveals tumor extension gross to within 0.5cm of muscle. Sections are submitted according to the following code: DE- deep surgical resection margins; SU, LA, INF, ME -- full thickness radila samplings from the center of the tumor superiorly,  laterally, inferiorly and medially, respectively: NI- nipple and subjacent tissue. Lymph nodes dissected free from axillary fibrofatty tissue from levels I, II, and III will be labeled accordingly.||||||F|||20040720
OBX|8|TX|22635-7^microscopic pathology^LN|1|Sections of part #1 confirm frozen section diagnosis of infiltrating duct carcinoma. It is to be noted that the tumor cells show considerable pleomorphism, and mitotic figures are frequent (as many as 4 per high power field). Many foci of calcification are present within the tumor. ||||||F|||20040720
OBX|9|TX|22635-7^microscopic pathology^LN|2|Part #2 consists of fibrofatty tissue and single tiny lymph node free of disease. ||||||F|||20040720
OBX|10|TX|22635-7^microscopic pathology^LN|3|Part #3 includes 18 lymph nodes, three from Level III, two from Level II and thirteen from Level I. All lymph nodes are free of disease with the exception of one Level I lymph node, which contains several masses of metastatic carcinoma. All sections taken radially from the superficial center of the resection site fail to include tumor, indicating the tumor to have originated deep within the breast parenchyma. Similarly, there is no malignancy in the nipple region, or in the lactiferous sinuses. Sections of deep surgical margin demonstrate diffuse tumor nfiltration of deep fatty tissues, however, there is no invasion of muscle. Total size of primary tumor is estimated to be 4cm in greatest dimension.||||||F|||20040720
OBX|11|TX|22637-3^final diagnosis^LN|1|1. Infiltrating duct carcinoma, left breast. ||||||F|||20040720
OBX|12|TX|22637-3^final diagnosis^LN|2|2. Lymph node, no pathologic diagnosis, left axilla.||||||F|||20040720
OBX|13|TX|22637-3^final diagnosis^LN|3|3. Ext. of tumor into deep fatty tissue. Metastatic carcinoma, left axillary lymph node (1) Level I. Free of disease 17 of 18 lymph nodes - Level I (12), Level II (2) and Level III (3). ||||||F|||20040720
OBX|14|TX|22638-1^comments^LN||Clinical diagnosis: carcinoma of breast. Postoperative diagnosis: same.||||||F|||20040720"""
        response = hl7validatorapi(data)
        print(response)
        #  self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct3(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|KIS||CommServer||200811111017||QRY^A19|ertyusdfg|P|2.2|
QRD|200811111016|R|I|Q1004|||1^RD|10000437363|DEM|18rg||"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")


if __name__ == "__main__":
    unittest.main()
