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

    def test_hl7validator_incorrect2(self):
        """
        Tests a correct HL7v2 Message
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\nEVN|A34|wewe\nPID|||JMS17131790^^^JMS^NS|256886210^^^NIF^PT~C3709807001^^^N_BENEF|THOMPSON^ELIZABETH^GRACE||20060523000000|F|||123 OCEANVIEW DRIVE, APT 9B^^SEATTLE^WA^98101^US||^^^ELIZABETH.THOMPSON@EMAIL.COM^^^935200945||||||270858182|||||||||||N\nMRG|JMS61226892^^^JMS^NS||||||THOMPSON^ELIZABETH^GRACE"

        response = hl7validatorapi(data)
        # self.assertEqual(assess_elements(response), True)
        print(response)

        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct_with_r(self):
        """
        Tests a correct HL7v2 Message
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\rEVN|A34|wewe\rPID|||JMS17131790^^^JMS^NS|256886210^^^NIF^PT~C3709807001^^^N_BENEF|THOMPSON^ELIZABETH^GRACE||20060523000000|F|||123 OCEANVIEW DRIVE, APT 9B^^SEATTLE^WA^98101^US||^^^ELIZABETH.THOMPSON@EMAIL.COM^^^935200945||||||270858182|||||||||||N\rMRG|JMS61226892^^^JMS^NS||||||THOMPSON^ELIZABETH^GRACE"

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
        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_correct4(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.8||
EVN|A01|200708181123||
PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||S||PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|
NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN
PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct5(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&#|NIST EHR|NIST EHR Facility|NIST Test Lab APP|NIST Lab Facility|20130211184101-0500||OML^O21^OML_O21|NIST-LOI_5.0_1.1-NG|T|2.5.1|||AL|AL|||||LOI_Common_Component^LOI Base Profile^2.16.840.1.113883.9.66^ISO~LOI_NG_Component^LOI NG Profile^2.16.840.1.113883.9.79^ISO~LAB_PRU_Component^LOI PRU Profile^2.16.840.1.113883.9.82^ISO
PID|1||PATID1239^^^NIST MPI^MR||Smirnoff^Peggy^^^^^M||19750401|F||2106-3^White^HL70005|450 Bauchet Street^^LosAngeles^CA^90012^^H|||||||||||N^Not Hispanic or Latino^HL70189NK1|1||OTH^Other^HL70063||||||||||County Women's Correctional Facility^^^^^CWCF&2.16.840.1.114222.4.50.12.4&ISO^XX^^^OID724ORC|NW|ORD448811^NIST EHR|||||||20120628070100|||5742200012^Radon^Nicholas^^^^^^NPI^L^^^NPI
OBR|1|ORD448811^NIST EHR||1000^Hepatitis A  B  C Panel_WithReflex^99USL|||20120628070100|||||||||5742200012^Radon^Nicholas^^^^^^NPI^L^^^NPI
DG1|1||F11.129^Opioid abuse with intoxication,unspecified^I10C|||W|||||||||1
OBX|1|CWE|67471-3^Pregnancy^LN||UNK^Unknown^HL70353^3118003^Possible, unconfirmed^99USL^^^suspected, but unconfirmed - no test to date||||||O|||20120628|||||||||||||||SCI
SPM|1|S-2012_448811&NIST EHR||119364003^Serum specimen(specimen)^SCT^SER^Serum^L|||||||||||||20120628070100"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct6(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|MILLENNIUM|WSH|WSH_TIE|WSH_TIE|20200310095702||RDE^O01|Q105132700T129367833||2.3||||||8859/1
PID|1|1516070^^^RGR50^MRN|1516070^^^RGR50^MR~^^^NHS^NH||ZZZTEST^MEDS TEAM OAK^^^PROFESSOR^^CURRENT||19800101|2|||No Fixed Abode^^^""^ZZ99 3VZ^GBR^HOME^^""||||""|""|""|10012589^^^Encounter Num^FINNBR||||C||""|0|""|""|""||""
PD1|""|""|Practice Code not known^^8023|G1234567^Test^GP^^^^^^External Id^PRSNL^^^EXTID^""|""||""|""
PV1|1|INPATIENT|ZZZTEST LAB^Bay 1^Bed 10^WSH^^BED^Main Building|22|||C4598938^Suresh^Mohanraj^^^Dr^^^NHS Consultant Number^PRSNL^^^NONGP^""~716337131016^Suresh^Mohanraj^^^Dr^^^Doctor Nbr^PRSNL^^^ORGDR^""|G1234567^Test^GP^^^^^^External Id^PRSNL^^^EXTID^""||300|""|""|""|19|""|""||INPATIENT|10012589^^^Attendance Num^VISITID|""||""||||||||||||||""|""|""|WSH||ACTIVE|||20190308090900
PV2||1||""|||""|||0|||""||||||||""|""|^^38024||||""
ZVI|""|||||430|||""|""||""||""|20200107144700|""|""|""|""|""|""|""||""|""|""
AL1|1|DRUG|##NOMEN##,AL1,ceStruct,allergy,32239,6334447^NKA^ALLERGY
ZAL|SNAPSHOT|20190308092025|1294449|1294449|ALLEGY|CANC|||||20190308092025|^Bognar^Julia^^^^^^^PRSNL|0
ORC|CA|31320845^HNAM_ORDERID|||CA||^twice a day^^20200310180000^20200310095701^ROUTINE||20200310095641|^Reed^Matt^^^^^^^PRSNL||C4598938^Suresh^Mohanraj^^^Dr^^^NHS Consultant Number^PRSNL^^^NONGP^""~716337131016^Suresh^Mohanraj^^^Dr^^^Doctor Nbr^PRSNL^^^ORGDR^""|""||20200310095701|Course completed^Course completed
RXO|CD:14490226^Diltiazem^NHS_LEG_INT^^Diltiazem|120||mg^^^^120 mg / 1 capsule|CD:14093882^capsule (modified release)||||||0|""|0
RXR|PO^oral|||CD:10915
RXE|^twice a day^""^20200310180000^20200310095701^ROUTINE|##ITEM##,IDENTIFIER_TYPE_CD,VALUE_KEY,524232,1,CE,coding_system^##ITEM##,DESC,VALUE,524232,1^^^Diltiazem|120||mg^^^^120 mg / 1 capsule|CD:14093882^capsule (modified release)||||1|EA|||^Reed^Matt^^^^^^^PRSNL|31320845
RXR|PO^oral|||CD:10915
OBX|1|TS|REQUESTED START DATE/TIME^Requested Start Date/Time^NHS_LEG_INT||20200310180000
OBX|2|ST|IV SET SHELL ITEM ID^IV Set Shell Item Id^NHS_LEG_INT||0
OBX|3|TS|CANCEL DATE AND TIME^Cancel Date/Time^NHS_LEG_INT||20200310095600"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct8(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|SIMHOSP|SFAC|RAPP|RFAC|20200508130644||ORU^R01|7|T|2.3|||AL||44|ASCII
PID|1|1076943130^^^SIMULATOR MRN^MRN|1076943130^^^SIMULATOR MRN^MRN~2914785070^^^NHSNBR^NHSNMBR||Trivedi^Jacqueline^Pauline^^Mrs^^CURRENT||19371227000000|F|||44 Name House^Flanker Road^Westerham^^PK17 5OI^GBR^HOME||070 0130 6118^HOME|||||||||N^Black or Black British - African^^^||||||||
PV1|1|I|OtherWard^MainRoom^Bed 1^Simulated Hospital^^BED^Main Building^4|28b|||C002^Smith^Elizabeth^^^Dr^^^DRNBR^PRSNL^^^ORGDR|||SUR|||||||||4637913778641671097^^^^visitid||||||||||||||||||||||ARRIVED|||20200508130644||
ORC|RE|3529823179|2427424202||CM||||20200508130644
OBR|1|3529823179|2427424202|us-0003^UREA AND ELECTROLYTES^WinPath^^||20200508130644|20200508130644|||||||20200508130644||||||||20200508130644|||F||1
OBX|1|NM|tt-0003-02^Potassium^WinPath^^||5.10|MMOLL|3.5 - 5.3||||F|||20200508130644||
OBX|2|NM|tt-0003-03^Sodium^WinPath^^||145.01|MMOLL|133 - 146||||F|||20200508130644||
OBX|3|NM|tt-0003-04^Urea^WinPath^^||5.45|MMOLL|2.5 - 7.8||||F|||20200508130644||
NTE|0||Music dinghy poet pyramid revenge human charles dictionary hydrofoil|
OBX|4|NM|tt-0003-05^eGFR (MDRD)^WinPath^^||<15|MLMIN|[ ]||||F|||20200508130644||
NTE|0||Objective chairlift pard mug mouse sweatshirt wildlife contract mode|
OBX|5|NM|tt-0003-01^Creatinine^WinPath^^||86.25|UMOLL|49 - 92||||F|||20200508130644||
NTE|0||Pyjama leash modem dressing pocket-watch resource essay|"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct7(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|NISTEHRAPP|NISTEHRFAC|NISTIISAPP|NISTIISFAC|20150625072816.601-0500||VXU^V04^VXU_V04|NIST-IZ-AD-10.1_Send_V04_Z22|P|2.5.1|||ER|AL|||||Z22^CDCPHINVS|NISTEHRFAC|NISTIISFAC
PID|1||21142^^^NIST-MPI-1^MR||Vasquez^Manuel^Diego^^^^L||19470215|M||2106-3^White^CDCREC|227 Park Ave^^Bozeman^MT^59715^USA^P||^PRN^PH^^^406^5555815~^NET^^Manuel.Vasquez@isp.com|||||||||2135-2^Hispanic or Latino^CDCREC||N|1|||||N
PD1|||||||||||01^No reminder/recall^HL70215|N|20150625|||A|20150625|20150625ORC|RE||31165^NIST-AA-IZ-2|||||||7824^Jackson^Lily^Suzanne^^^^^NIST-PI-1^L^^^PRN|||||||NISTEHRFAC^NISTEHRFacility^HL70362
RXA|0|1|20141021||152^Pneumococcal Conjugate, unspecified formulation^CVX|999|||01^Historical Administration^NIP001|||||||||||CP|A
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct9(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|MILLENNIUM|WSH|WSH_TIE|WSH_TIE|20200310095702||RDE^O01|Q105132700T129367833||2.3||||||8859/1
PID|1|1516070^^^RGR50^MRN|1516070^^^RGR50^MR~^^^NHS^NH||ZZZTEST^MEDS TEAM OAK^^^PROFESSOR^^CURRENT||19800101|2|||No Fixed Abode^^^""^ZZ99 3VZ^GBR^HOME^^""||||""|""|""|10012589^^^Encounter Num^FINNBR||||C||""|0|""|""|""||""
PD1|""|""|Practice Code not known^^8023|G1234567^Test^GP^^^^^^External Id^PRSNL^^^EXTID^""|""||""|""
PV1|1|INPATIENT|ZZZTEST LAB^Bay 1^Bed 10^WSH^^BED^Main Building|22|||C4598938^Suresh^Mohanraj^^^Dr^^^NHS Consultant Number^PRSNL^^^NONGP^""~716337131016^Suresh^Mohanraj^^^Dr^^^Doctor Nbr^PRSNL^^^ORGDR^""|G1234567^Test^GP^^^^^^External Id^PRSNL^^^EXTID^""||300|""|""|""|19|""|""||INPATIENT|10012589^^^Attendance Num^VISITID|""||""||||||||||||||""|""|""|WSH||ACTIVE|||20190308090900
PV2||1||""|||""|||0|||""||||||||""|""|^^38024||||""
ZVI|""|||||430|||""|""||""||""|20200107144700|""|""|""|""|""|""|""||""|""|""
AL1|1|DRUG|##NOMEN##,AL1,ceStruct,allergy,32239,6334447^NKA^ALLERGY
ZAL|SNAPSHOT|20190308092025|1294449|1294449|ALLEGY|CANC|||||20190308092025|^Bognar^Julia^^^^^^^PRSNL|0
ORC|CA|31320845^HNAM_ORDERID|||CA||^twice a day^^20200310180000^20200310095701^ROUTINE||20200310095641|^Reed^Matt^^^^^^^PRSNL||C4598938^Suresh^Mohanraj^^^Dr^^^NHS Consultant Number^PRSNL^^^NONGP^""~716337131016^Suresh^Mohanraj^^^Dr^^^Doctor Nbr^PRSNL^^^ORGDR^""|""||20200310095701|Course completed^Course completed
RXO|CD:14490226^Diltiazem^NHS_LEG_INT^^Diltiazem|120||mg^^^^120 mg / 1 capsule|CD:14093882^capsule (modified release)||||||0|""|0
RXR|PO^oral|||CD:10915
RXE|^twice a day^""^20200310180000^20200310095701^ROUTINE|##ITEM##,IDENTIFIER_TYPE_CD,VALUE_KEY,524232,1,CE,coding_system^##ITEM##,DESC,VALUE,524232,1^^^Diltiazem|120||mg^^^^120 mg / 1 capsule|CD:14093882^capsule (modified release)||||1|EA|||^Reed^Matt^^^^^^^PRSNL|31320845
RXR|PO^oral|||CD:10915
OBX|1|TS|REQUESTED START DATE/TIME^Requested Start Date/Time^NHS_LEG_INT||20200310180000
OBX|2|ST|IV SET SHELL ITEM ID^IV Set Shell Item Id^NHS_LEG_INT||0
OBX|3|TS|CANCEL DATE AND TIME^Cancel Date/Time^NHS_LEG_INT||20200310095600
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct10(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|NISTEHRAPP|NISTEHRFAC|NISTIISAPP|NISTIISFAC|20150624084727.655-0500||VXU^V04^VXU_V04|NIST-IZ-AD-2.1_Send_V04_Z22|P|2.5.1|||ER|AL|||||Z22^CDCPHINVS|NISTEHRFAC|NISTIISFAC
PID|1||90012^^^NIST-MPI-1^MR||Wong^Elise^^^^^L||19830615|F||2028-9^Asian^CDCREC|9200 Wellington Trail^^Bozeman^MT^59715^USA^P||^PRN^PH^^^406^5557896~^NET^^Elise.Wong@isp.com|||||||||2186-5^Not Hispanic or   Latino^CDCREC||N|1|||||N
PD1|||||||||||02^Reminder/recall -  any method^HL70215|N|20150624|||A|19830615|20150624
ORC|RE|4422^NIST-AA-IZ-2|13696^NIST-AA-IZ-2|||||||7824^Jackson^Lily^Suzanne^^^^^NIST-PI-1^L^^^PRN||654^Thomas^Wilma^Elizabeth^^^^^NIST-PI-1^L^^^MD|||||NISTEHRFAC^NISTEHRFacility^HL70362|
RXA|0|1|20150624||49281-0215-88^TENIVAC^NDC|0.5|mL^mL^UCUM||00^New Record^NIP001|7824^Jackson^Lily^Suzanne^^^^^NIST-PI-1^L^^^PRN|^^^NIST-Clinic-1||||315841|20151216|PMC^Sanofi Pasteur^MVX|||CP|A
RXR|C28161^Intramuscular^NCIT|RD^Right Deltoid^HL70163
OBX|1|CE|30963-3^Vaccine Funding Source^LN|1|PHC70^Private^CDCPHINVS||||||F|||20150624
OBX|2|CE|64994-7^Vaccine Funding Program Eligibility^LN|2|V01^Not VFC Eligible^HL70064||||||F|||20150624|||VXC40^per immunization^CDCPHINVS
OBX|3|CE|69764-9^Document Type^LN|3|253088698300028811170411^Tetanus/Diphtheria (Td) Vaccine VIS^cdcgs1vis||||||F|||20150624
OBX|4|DT|29769-7^Date Vis Presented^LN|3|20150624||||||F|||20150624
ORC|RE||38760^NIST-AA-IZ-2|||||||7824^Jackson^Lily^Suzanne^^^^^NIST-PI-1^L^^^PRN|||||||NISTEHRFAC^NISTEHRFacility^HL70362
RXA|0|1|20141012||88^influenza, unspecified formulation^CVX|999|||01^Historical Administration^NIP001|||||||||||CP|A
ORC|RE||35508^NIST-AA-IZ-2|||||||7824^Jackson^Lily^Suzanne^^^^^NIST-PI-1^L^^^PRN|||||||NISTEHRFAC^NISTEHRFacility^HL70362
RXA|0|1|20131112||88^influenza, unspecified formulation^CVX|999|||01^Historical Administration^NIP001|||||||||||CP|A
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct11(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """FHS|^~\&|WIR11.3.2^^^|WIR^^^|||20200514||1218918.update|||
BHS|^~\&|WIR11.3.2^^^|WIR^^^|||20200514|||||
MSH|^~\&|WIR11.3.2^^^|WIR^^^||WIRPH^^^|20200514||VXU^V04|2020051409183900|P^|2.3.1^^|||ER
PID|||3019190^^^^^||NEW^BORNBOY^^^^^^||20180711|U||B^^^^^|185 4TH AVE^^EAU CLAIRE^WI^54703^^^^WI035^^||(608)696-9696^PRN^PH^^^608^6969696^^|||||||||H^^^^^|||||||
PD1|||||||||||02^^^^^|Y||A
NK1|1|NEW^BORNBOY^^^^^^|18^SELF^HL70063^^^|185 4TH AVE^^EAU CLAIRE^WI^54703^^^^^^|(608)696-9696^PRN^PH^^^608^6969696^^
RXA|0|999|20180911|20180911|48^Hib-PRP-T^CVX^90648^Hib-PRP-T^CPT|1.0|||01^^^^^~38178326^WIR immunization id^IMM_ID^^^||||||||
BTS|1|
FTS|1|
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct12(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|Healthmatics|Healthmatics EHR|Ntierprise|Ntierprise Clinic|20190416084748||DFT^P03|1477-3|P|2.3|||NE|NE
EVN|P03|20190416084748||01
PID|1|A4EMR640|640|67359|Test^Patient1^D||19700101|F||3|1212 Dillard Drive^^Cary^NC^27511|||(222)222-2222^^^^^222^2222222||S
PV1|1|R|MainOffi||||Manning^Manning^Terry^^^^^^&7654321&UPIN|||||||||||||||||||||||||||||||||||||20190416110000||||||1203
FT1|1|E8866||20190416110000|20190416110000|CG||||1||||||^^^MainOffi|||J11.1^INFLUENZA WITH OTHER RESPIRATORY MANIFESTATIONS^I10~487.1^INFLUENZA WITH OTHER RESPIRATORY MANIFESTATIONS^I9~J03.90^INFLUENZA WITH OTHER RESPIRATORY MANIFESTATIONS^I10~J40^BRONCHITIS, NOT SPECIFIED AS ACUTE OR CHRONIC^I10~490^BRONCHITIS, NOT SPECIFIED AS ACUTE OR CHRONIC^I9|TM^Manning^Terry^^^^^^&7654321&UPIN|Manning^Manning^Terry^^^^^^&7654321&UPIN||||99214^OFFICE OUTPATIENT VISIT 25 MINUTES
PR1|1||99214^OFFICE OUTPATIENT VISIT 25 MINUTES||20190416110000|D|||||||||J11.1^^I10
DG1|1|I|J11.1^INFLUENZA WITH OTHER RESPIRATORY MANIFESTATIONS^I10|||F
DG1|2|I|487.1^INFLUENZA WITH OTHER RESPIRATORY MANIFESTATIONS^I9|||F
DG1|3|I|J03.90^INFLUENZA WITH OTHER RESPIRATORY MANIFESTATIONS^I10|||F
DG1|4|I|J40^BRONCHITIS, NOT SPECIFIED AS ACUTE OR CHRONIC^I10|||F
DG1|5|I|490^BRONCHITIS, NOT SPECIFIED AS ACUTE OR CHRONIC^I9|||F
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct13(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|Ntierprise|Ntierprise Clinic|Healthmatics EHR|Healthmatics Clinic|20190423114154||SIU^S12|8907-45|P|2.3|||NE|NE
SCH|1209|13030|||1209|OV15^OFFICE VISIT-15^CSI^N|OFFICE VISIT-15^OFFICE VISIT-15 -|OV15|15|m|^^15^20190423140000^20190423141500|||||mdrxmbyr^Byrne^Misty||||mdrxmbyr^Byrne^Misty|||||Scheduled^^CSI
PID|1||150||Bond^James^^007||19770920|M|||007 Soho Lane^^Cary^NC^27511||(919)007-0007^^^^^919^0070007~(777)707-0707^^CP^^^777^7070707~^NET^X.400^007@BritishSecretService.com|(919)851-6177 X007^^^^^919^8516177^007||M||150|007-00-0007|||||||||||N
PV1|1|R|||||MRYAN^Ryan^Mark^S^phd^^^^&MR1127&UPIN||WEEDER^Weeder, M.D.^Dana^N^^^^^&W22630&UPIN|||||||N||||M
RGS|1|A
AIG|1||PULLEN^Pullen, Jeri|P^^CSI
AIL|1||MainOffi^^^MainOffi^^^^^Healthmatics Clinic|^Healthmatics Clinic^CSI
AIP|1||JPULLEN1^Pullen^Jeri^^^^^^&F12456&UPIN|D^Pullen, Jeri||20190423140000|||15|m^Minutes
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_correct14(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|Ntierprise|Ntierprise Clinic|Healthmatics EHR|Healthmatics Clinic|20190423114643||MFN^M02|8915-51|P|2.3|||NE|NE
MFI|REF||UPD|||NE
MFE|MAD|||testy
STF|testy|testy|Aaron^RefTest^R|R|M|19871011|A|||(333)222-1111^^PH^RefTest@Allscripts.com^^333^2221111|Address1^^Raleigh^NC^27609
PRA|testy|||||984567UPIN^UPIN
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct15(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|SendFac|SendApp|EXTERNAL APP|EXTERNAL FAC|201902021310|319|MDM^T02|42|P|2.3.1||
EVN|T02|201902021310|||543453^WILLIAMS^LINDSAY^^^^^^NPI^L^^^NPI
PID|1||117513^^^West^MR||Patrick^Michelle^ANNE^^^||19810518|F|||120 WOODSY ANIMAL LANE^^MIDDLETON^WI^53700^USA||(608)222-2222|(608)777-7777
PV1|1|O|||||543453^WILLIAMS^LINDSAY^^^^^^NPI^L^^^NPI ||||||||||||17872
TXA|1|OV^Outpatient Visit Note|TX|201902021000|543453^WILLIAMS^LINDSAY^^^^^^NPI^L^^^NPI|201902021315|||543453^WILLIAMS^LINDSAY^^^^^^NPI^L^^^NPI|||OV17872|||||AU||AV|||543453^WILLIAMS^LINDSAY ^^^^^^PRN^^^^^^201902021420|
OBX|1|TX|1006^History: Family|6|Family History~~ Problem Relation Age of Onset~ Asthma Grandchild 13~ Comments: Comments~ Colon Cancer Mother 57~ Arthritis Brother~ Arthritis Sister~ Cancer Sister~ Cancer Maternal Grandfather~ Allergies Paternal Grandmother~ Alcohol/Drug Mother~ Gestational Diabetes Brother~~Family Status - Relation Status Age at Death~ Mother Alive~ Father Deceased~ Sister Alive~ Maternal Grandmother Deceased 68~ Maternal Grandfather Deceased 65~||||||F

"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct16(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|Ntierprise|Ntierprise Clinic|Healthmatics EHR|Healthmatics Clinic|20190423150137||ADT^A34|8919-40|P|2.3|||NE|NE
EVN|A34|20190423150137||01
PID|1||5027440||Tester^BabyGirl^A||20180205|F|||123 Any Street^^Raleigh^NC^27615||(111)111-1111^^^^^111^1111111|||||5027440
MRG|5027450
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_correct17(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|P0241|HOMERTON|HOMERTON_TIE|HOMERTON|20150209170901||ADT^A31|Q111111119T4083493511111111||2.3
EVN|A31|20150209170901|||101111^Smith^Geoff^^^^^^PERSONNEL PRIMARY IDENTIFIER^Personnel^^^Personnel Primary Identifier^""
PID|1|999999^^^Homerton Case Note Number^MRN^""|999998^^^Homerton Case Note Number^CNN~111111^^^Person ID^Person ID||MIAH^Jane^^^Miss^^Current~~^MIAH^^^^^Alternate||19781030000000|Female|^MIAH^^^^^Alternate~Miah^Janet^^^Miss^^Preferred~JONES^Jane^^^Miss^^Previous|""|Flat 1^15 Main Street^^London^N1 1AA^""^home^^""~MAJOR HOUSE^CHURCH ROAD^^""^^""^Previous^LONDON^""||^Home^Tel~07777111111^Mobile Number^Tel|^Business|Turkish|""|Not Known|999999^^^Homerton FIN^Encounter No.^""|9999999999|||Eastern European|||0|""|""|""||No||Trace in Progress
PD1|""|""||G88888888^RICHARDSON^JANET^^020711111111^F84040^MAIN ROAD MEDICAL CENTRE^100 MAIN ROAD^&LONDON&N1 1AA^^^^^Q06|""||""|""
NK1|1|MIAH^Richard^^^^^Current|""|Flat 1^15 Main Road^^""^N1 1AA^""^^^""|077777222333||Next of Kin|||||||||||||""
PV1|1|Inpatient|HUH AE OMU^OMU B^Bed 03^HOMERTON UNIVER^^Bed(s)^Homerton UH|Emergency-A\T\E/Dental||HUH AE Adults^""^""^HOMERTON UNIVER^^^Homerton UH|1122334^Alaz^Mohammed^^^^^^PERSONNEL PRIMARY IDENTIFIER^Personnel^^^Personnel Primary Identifier^""~ALAZ^Alaz^Mohammed^^^^^^Homerton Sysmed Prsnl Pool^Personnel^^^OTHER^""~C10001000^Alaz^Mohammed^^^^^^""^Personnel^^^COMMUNITY DR NBR^""~C20002000^Alaz^Mohammed^^^^^^NHS PRSNL ID^Personnel^^^PRSNLID^""|3333444^Kumar^Alesh^^^^^^PERSONNEL PRIMARY IDENTIFIER^Personnel^^^Personnel Primary Identifier^""~KUMAR^Kumar^Alesh^^^^^^Homerton Sysmed Prsnl Pool^Personnel^^^OTHER^""~C30010002^Kumar^Alesh^^^^^^""^Personnel^^^COMMUNITY DR NBR^""||Accident and Emergency|""|""|New Problem/First Attendance|NHS Provider-General (inc.A\T\E-this Hosp)|""|""||Inpatient|5000000^0^""^^Attendance No.|""||""||||||||||||||Admitted as Inpatient|""|""|HOMERTON UNIVER||Active|||20150208113419
PV2||NHS|^4 UNWELL|Transfer from ED|||""|||0|||""||||||||""|""|^^1
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct18(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|MS4_AZ|UNV|PREMISE|UNV|20180301010000||ADT^A04|IHS-20180301010000.00120|P|2.1
EVN|A04|20180301010000
PID|1||19050114293307.1082||BUNNY^BUGS^RABBIT^^^MS||19830215|M|||1234 LOONEY RD^APT A^CRAIGMONT^ID^83523^USA|||||||111-11-1111|111-11-1111
PV1|1|E|ED^^^UNV|C|||999-99-9999^MUNCHER^CHANDRA^ANDRIA^MD^DR|888-88-8888^SMETHERS^ANNETTA^JONI^MD^DR||||||7||||REF||||||||||||||||||||||||||20180301010000
"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct19(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|P0241|HOMERTON|HOMERTON_TIE|HOMERTON|20150209170901||ADT^A31|Q111111119T4083493511111111||2.3
EVN|A31|20150209170901|||101111^Smith^Geoff^^^^^^PERSONNEL PRIMARY IDENTIFIER^Personnel^^^Personnel Primary Identifier^""
PID|1|999999^^^Homerton Case Note Number^MRN^""|999998^^^Homerton Case Note Number^CNN~111111^^^Person ID^Person ID||MIAH^Jane^^^Miss^^Current~~^MIAH^^^^^Alternate||19781030000000|Female|^MIAH^^^^^Alternate~Miah^Janet^^^Miss^^Preferred~JONES^Jane^^^Miss^^Previous|""|Flat 1^15 Main Street^^London^N1 1AA^""^home^^""~MAJOR HOUSE^CHURCH ROAD^^""^^""^Previous^LONDON^""||^Home^Tel~07777111111^Mobile Number^Tel|^Business|Turkish|""|Not Known|999999^^^Homerton FIN^Encounter No.^""|9999999999|||Eastern European|||0|""|""|""||No||Trace in Progress
PD1|""|""||G88888888^RICHARDSON^JANET^^020711111111^F84040^MAIN ROAD MEDICAL CENTRE^100 MAIN ROAD^&LONDON&N1 1AA^^^^^Q06|""||""|""
NK1|1|MIAH^Richard^^^^^Current|""|Flat 1^15 Main Road^^""^N1 1AA^""^^^""|077777222333||Next of Kin|||||||||||||""
PV1|1|Inpatient|HUH AE OMU^OMU B^Bed 03^HOMERTON UNIVER^^Bed(s)^Homerton UH|Emergency-A\T\E/Dental||HUH AE Adults^""^""^HOMERTON UNIVER^^^Homerton UH|1122334^Alaz^Mohammed^^^^^^PERSONNEL PRIMARY IDENTIFIER^Personnel^^^Personnel Primary Identifier^""~ALAZ^Alaz^Mohammed^^^^^^Homerton Sysmed Prsnl Pool^Personnel^^^OTHER^""~C10001000^Alaz^Mohammed^^^^^^""^Personnel^^^COMMUNITY DR NBR^""~C20002000^Alaz^Mohammed^^^^^^NHS PRSNL ID^Personnel^^^PRSNLID^""|3333444^Kumar^Alesh^^^^^^PERSONNEL PRIMARY IDENTIFIER^Personnel^^^Personnel Primary Identifier^""~KUMAR^Kumar^Alesh^^^^^^Homerton Sysmed Prsnl Pool^Personnel^^^OTHER^""~C30010002^Kumar^Alesh^^^^^^""^Personnel^^^COMMUNITY DR NBR^""||Accident and Emergency|""|""|New Problem/First Attendance|NHS Provider-General (inc.A\T\E-this Hosp)|""|""||Inpatient|5000000^0^""^^Attendance No.|""||""||||||||||||||Admitted as Inpatient|""|""|HOMERTON UNIVER||Active|||20150208113419
PV2||NHS|^4 UNWELL|Transfer from ED|||""|||0|||""||||||||""|""|^^1"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct21(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|PAS|RCB|ROUTE|ROUTE|201001021215||ADT^A28^ADT_A05|13403891320453338075|P|2.4|0|20100102121557|||GBR|UNICODE|EN||iTKv1.0
EVN||201001021213|||111111111^Cortana^Emily^^Miss^^RCB55|201001021213
PID|1||3333333333^^^NHS||SMITH^FREDRICA^J^^MRS^^L|SCHMIDT^HELGAR^Y|196511121515|2|||29 WEST AVENUE^BURYTHORPE^MALTON^NORTH YORKSHIRE^YO32 5TT^GBR^H||+441234567890||EN|M|C22|||||A|Berlin|N||GBR||DEU||||ED
PD1|||MALTON GP PRACTICE^^Y06601|G5612908^Townley^Gregory^^^Dr^^^GMC
NK1|2|SMITH^FRANCESCA^^^MRS^^L|16|29 WEST AVENUE^BURYTHORPE^MALTON^NORTH YORKSHIRE^YO32 5TT^GBR^H|+441234567890||||||||||1|196311111513||||EN
PV1||N|
AL1|1|DA|Z88.5|5||199807011755"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_correct22(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|Ntierprise|Ntierprise Clinic|Healthmatics EHR|Healthmatics Clinic|20190423113910||ADT^A08|8899-39|P|2.3|||NE|NE
EVN|A08|20190423113910||01
PID|1||151||Bond^Tiny||19990723|M|||8388 Secret Agent Way^^Raleigh^NC^27677|||||||151||||||||||||N
NK1|1|Bond^Lady^T|Spouse^Spouse|007 Soho Lane^^Cary^NC^27511|(919)007-0007^^PH^^^919^0070007
PV1|1|R|||||Manning^Manning^Terry^^^^^^&7654321&UPIN|||||||||N||A
GT1|1|150|Bond^James^^007||007 Soho Lane^^Cary^NC^27511|(919)007-0007^^PH^^^919^0070007~(777)707-0707^^CP^^^777^7070707~^NET^X.400^007@BritishSecretService.com|(919)851-6177 X007^^^^^919^8516177^007|19770920|M|||007-00-0007|||||2988 England Drive^^London^DC|||F||||||||||M|||||||||||||||||||||British Secret Service"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct23(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|SIMHOSP|SFAC|RAPP|RFAC|20200502220643||ORU^R01|2|T|2.3|||AL||44|ASCII
PID|1|2590157853^^^SIMULATOR MRN^MRN|2590157853^^^SIMULATOR MRN^MRN~2478684691^^^NHSNBR^NHSNMBR||Esterkin^AKI Scenario 6^^^Miss^^CURRENT||19890118000000|F|||170 Juice Place^^London^^RW21 6KC^GBR^HOME||020 5368 1665^HOME|||||||||R^Other - Chinese^^^||||||||
PV1|1|O|ED^^^Simulated Hospital^^ED^^|28b|||C006^Wolf^Kathy^^^Dr^^^DRNBR^PRSNL^^^ORGDR|||MED||||||||||||||||||||||||||||||||||20200501140643||
ORC|RE|3259758581|3281433988||CM||||20200502220643
OBR|1|3259758581|3281433988|us-0003^UREA AND ELECTROLYTES^WinPath^^||20200502220643|20200502220643|||||||20200502220643||||||||20200502220643|||F||1
OBX|1|NM|tt-0003-01^Creatinine^WinPath^^||83.00|UMOLL|49 - 92||||F|||20200502220643|"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct24(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&#|NIST EHR^2.16.840.1.113883.3.72.5.22^ISO|NIST EHR Facility^2.16.840.1.113883.3.72.5.23^ISO|NIST Test Lab APP^2.16.840.1.113883.3.72.5.20^ISO|NIST Lab Facility^2.16.840.1.113883.3.72.5.21^ISO|20130211184101-0500||OML^O21^OML_O21|NIST-LOI_9.0_1.1-GU_PRU|T|2.5.1|||AL|AL|||||LOI_Common_Component^LOI BaseProfile^2.16.840.1.113883.9.66^ISO~LOI_GU_Component^LOI GU Profile^2.16.840.1.113883.9.78^ISO~LAB_PRU_Component^LOI PRU Profile^2.16.840.1.113883.9.82^ISO
PID|1||PATID14567^^^NIST MPI&2.16.840.1.113883.3.72.5.30.2&ISO^MR||Hernandez^Maria^^^^^L||19880906|F||2054-5^Black or   African American^HL70005|3248 E  FlorenceAve^^Huntington Park^CA^90255^^H||^^PH^^^323^5825421|||||||||H^Hispanic or Latino^HL70189
ORC|NW|ORD231-1^NIST EHR^2.16.840.1.113883.3.72.5.24^ISO|||||||20130116090021-0800|||134569827^Feller^Hans^^^^^^NPI&2.16.840.1.113883.4.6&ISO^L^^^NPI
OBR|1|ORD231-1^NIST EHR^2.16.840.1.113883.3.72.5.24^ISO||34555-3^Creatinine 24H renal clearance panel^LN^^^^^^CreatinineClearance|||201301151130-0800|201301160912-0800||||||||134569827^Feller^Hans^^^^^^NPI&2.16.840.1.113883.4.6&ISO^L^^^NPI
DG1|1||I10^Essential (primary) hypertension^I10C^^^^^^Hypertension, NOS|||F|||||||||2
DG1|2||O10.93^Unspecified pre-existing hypertension complicating the puerperium^I10C^^^^^^Pregnancy with chronic hypertension|||W|||||||||1
OBX|1|CWE|67471-3^Pregnancy status^LN^1903^Pregnancy status^99USL^2.44^^Isthe patient pregnant?||Y^Yes^HL70136^1^Yes, confirmed less than 12 weeks^99USL^2.5.1^^early pregnancy (pre 12 weeks)||||||O|||20130115|||||||||||||||SCI
OBX|2|NM|3167-4^Volume of   24   hour Urine^LN^1904^Urine Volume of 24 hour collection^99USL^2.44^^Urine Volume 24hour collection||1250|mL^milliliter^UCUM^ml^mililiter^L^1.7^^ml|||||O|||20130116|||||||||||||||SCI
OBX|3|NM|3141-9^Body weight Measured^LN^BWm^Body weight Measured^99USL^2.44^^patient weight measured in kg||59.5|kg^kilogram^UCUM|||||O|||20130116|||||||||||||||SCI
SPM|1|S-2312987-1&NIST EHR&2.16.840.1.113883.3.72.5.24&ISO||276833005^24 hour urine sample (specimen)^SCT^UR24H^24hr Urine^99USL^^^24 hour urine|||||||||||||201301151130-0800^201301160912-0800
SPM|2|S-2312987-2&NIST EHR&2.16.840.1.113883.3.72.5.24&ISO||119297000^Blood Specimen^SCT|||||||||||||201301160912-0800ORC|NW|ORD231-2^NIST EHR^2.16.840.1.113883.3.72.5.24^ISO|||||||20130115102146-0800|||134569827^Feller^Hans^^^^^^NPI&2.16.840.1.113883.4.6&ISO^L^^^NPI
OBR|2|ORD231-2^NIST EHR^2.16.840.1.113883.3.72.5.24^ISO||21482-5^Protein [Mass/volume] in 24 hour Urine^LN^^^^^^24 hour Urine Protein|||201301151130-0800|201301160912-0800||||||||134569827^Feller^Hans^^^^^^NPI&2.16.840.1.113883.4.6&ISO^L^^^NPI
DG1|1||I10^Essential (primary) hypertension^I10C^^^^^^Hypertension, NOS|||F|||||||||2"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct25(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&#|SndApp^1.2.3.4.5^ISO|SndFac^1.2.3.4.5^ISO|RcvApp^1.2.3.4.5^ISO|RcvFac^1.2.3.4.5^ISO|20150601160901.12+0100|20150601160810+0500|ORM^O01^ORM_O01|5381904|P|2.3.1|||AL|AL|USA|ASCII|en-US^^ISO639|
PID|1||1032702^^^SndFac&1.2.3.4.5&ISO^MR^ AssignFac&1.2.3.4.5.7&ISO^20190101^20290101||Everywoman^Eve^L^Jr^Dr^^L^^^^G^20000909^20301231^PhD~ Original^Eve^L^Jr^^^M^^^19700601&20000908^G||197006010912|F||1002-5^American Indian or Alaska Native^HL70005~2106-3^White^HL70005|1000 House Lane^Appt 123^Ann Arbor ^MI^99999^USA^H^^WA||^PRN^PH^^1^555^555-8473~^NET^Internet^eve@test.test|^WPN^PH^^1^555^555-1126^12|en-US^^ISO639|M^Married^HL70002|CHR^Christian^HL70006|12345^^^ SndFact&1.2.3.4.5&ISO^AN||12345^MI^20180219||N^Not Hispanic or Latino&HL70189|1025 House Lane^^Ann Arbor ^MI^99999^USA^H^^WA|Y|2|NL^Netherlands^ISO3166||||N|
PV1|1|E^EMERGENCY^HL70004|EMERG^101^01^^^^^^^^DEPID|E^Emergency^HL70007|| | |||857432^Jones^Emily^^^MD^^ AssignAuth&1.2.3.4.5.6&ISO^L^9^1000^DN^ AssignFac&1.2.3.4.5.7&ISO^^G^20100101000000^20330101000000^doctor|||||| |||81456267^^^AssignAuth&1.2.3.4.5.6&ISO^VN|T^Third Party Bill^HL70064||||||||||||||||||||||||20150601135800|
PV2|||^Not feeling well|||||201506011609|||||23432^Smith^Gordon^Denny^Jr^MD^^AssignAuth&1.2.3.4.5.6&ISO^L^9^1000^DN^AssignFac&1.2.3.4.5.7&ISO^^G^20100101000000^20330101000000^doctor||||||||F|N|||2^Urgent^HL72017|
IN1|1|200101^Medicare A and B|2001|Medicare|[Get CMS address]|||123450-1||[check on workman�s comp]|20150101|20151231||Medicare|Everywoman^Eve^L^Jr^Dr^^L^^^^G^20000909^20301231^PhD~Original^Eve^L^Jr^^^M^^^19700601&20000908^G|SEL^Self^HL70063|197006010912|1000 House Lane^Appt 123^Ann Arbor^MI^99999^USA^H^^WA|||||||||||||||||54321-01|
AL1|1|LA^Pollen Allergy^HL70127|^Timothy Grass|MO^Moderate^HL70128|Sneeze|201406|
ORC|NW|ORD777889^SndFac^1.2.3.4.5^ISO||GORD874245^SndFac^1.2.3.4.5^ISO|||1^^^20150601^^R||201506011610|1234567890^PhysicianAssistant^Will^John^III^Mr.^PA^&372526&L^L^^^NPI^^^^G^20140129^^FHL7|5742200012^Radon^Nicholas^^^^^^&372526&L^L^^^NPI|5742200012^Radon^Nicholas^^^^^^&372526&L^L^^^NPI|||||^^^^^^^^Emergency Department|||2^Patient has been informed of responsibility, and agrees to pay for service^HL70339|SndFac^1.2.3.4.5^ISO|Emergency Lane&&911^First Floor^Ann Arbor^MI^99999^USA^S&Service Location&HL70190^^WA^9876^^20100612^^^^^^^Attn: ED Doc in Charge|555-555-9110|Emergency Lane&&912^Medical Building I^Ann Arbor^MI^99999^USA^S&Service Location&HL70190^^WA^9876^^20100813^^^^^^^Attn: Office Manager
OBR|1|ORD777888^SndFac^1.2.3.4.5^ISO||51523-9^Grass Pollen Mix^LN|R|201506011608|201506011608||||||||SER&Serum&HL0070|5742200012^Radon^Nicholas^^^^^^&372526&L^L^^^NPI|^WPN^PH^^1^555^5559908^34||||||||||1^^^20150601^^R|10092000194^Hamlin^Pafford^^^^^^&372526&L^L^^^NPI
NTE|1||Bluegrass is in bloom at the moment|RE|"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Failed")

    def test_hl7validator_correct26(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|||||20040629164652|1|PPR^PC1|331|P|2.3.1|| 
PID|||10290^^^WEST^MR||KARLS^TOM^ANDREW^^MR.^||20040530|M|||||||||||398-44-5555|||||||||||N 
PRB|AD|2004062916460000|596.5^BLADDER DYSFUNCTION^I9|26744|||20040629||||||ACTIVE|||20040629 """
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Success")

    def test_hl7validator_correct27(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|PAS|RCB|ROUTE|ROUTE|201001021215||ADT^A28^ADT_A05|13403891320453338075|P|2.4|0|20100102121557|||GBR|UNICODE|EN||iTKv1.0
EVN||201001021213|||111111111^Cortana^Emily^^Miss^^RCB55|201001021213
PID|1||3333333333^^^NHS||SMITH^FREDRICA^J^^MRS^^L|SCHMIDT^HELGAR^Y|196511121515|2|||29 WEST AVENUE^BURYTHORPE^MALTON^NORTH YORKSHIRE^YO32 5TT^GBR^H||+441234567890||EN|M|C22|||||A|Berlin|N||GBR||DEU||||ED
PD1|||MALTON GP PRACTICE^^Y06601|G5612908^Townley^Gregory^^^Dr^^^GMC
NK1|2|SMITH^FRANCESCA^^^MRS^^L|16|29 WEST AVENUE^BURYTHORPE^MALTON^NORTH YORKSHIRE^YO32 5TT^GBR^H|+441234567890||||||||||1|196311111513||||EN
PV1||N|
AL1|1|DA|Z88.5|5||199807011755"""
        response = hl7validatorapi(data)
        #   self.assertEqual(assess_elements(response), True)
        self.assertEqual(response["statusCode"], "Success")


if __name__ == "__main__":
    unittest.main()
