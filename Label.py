# encoding=utf-8
import json
import os
import re


def error(x):
    print(x)


class nlp_pre_process(object):

    def __init__(self, datapath):
        if not (os.path.isfile(datapath)):
            print('file ' + datapath + ' not exists')
            exit(1)
        self.datapath = datapath
        self.writefile = 'new_file2.txt'

    def new_msg(self):
        pass

    def end_msg(self):
        pass

    def view_file(self):
        msgs = []
        with open(self.datapath, "r") as file, open(self.writefile, 'w') as wf:
            text_59 = []
            text_47 = []
            ca = None
            pattern_title = re.compile(r'^:[0-9a-zA-Z\_]{2,3}:*')
            pattern_47 = re.compile(r'SEE 47')
            for line in file:
                line = line.strip().upper()
                if line.endswith(r"}{4:") or line.startswith("-}{"):
                    if len(text_59) > 0:
                        t = '\n'.join(text_59)
                        print("********", file=wf)
                        print(t, file=wf)
                        output_59 = text_59
                        output_47 = []

                        sentences_47 = [x.strip() for x in '\n'.join(text_47).split("+")]
                        b_addr = list(filter(lambda x: x.startswith("BENE"), sentences_47))
                        see_47_present = pattern_47.search(t)
                        if len(b_addr) == 0 and see_47_present:
                            error(sentences_47)
                        if len(b_addr) > 0:
                            print("########", file=wf)
                            print('\n'.join(b_addr), file=wf)
                        output_47 = b_addr
                        msgs.append((output_59, output_47, see_47_present is not None))
                    text_59 = []
                    text_47 = []
                elif pattern_title.search(line):
                    if line.startswith(":59:"):
                        ca = text_59
                        ca.append(line[4:])
                    elif line.startswith(":47A:"):
                        ca = text_47
                        ca.append(line[5:])
                    else:
                        ca = None
                else:
                    if ca is not None and line != ".":
                        ca.append(line)
        return msgs


pattern_tf = re.compile(r"((T(EL)?)|PHONE|((T(EL)?\/)?(F(AX)?))):?[ 0-9\(\)\-\/\+]{8,}")
pattern_tf_num = re.compile(r"[0-9\+(][ 0-9\(\)\-\/]+[0-9]")
pattern_number = re.compile(r"[0-9]")
sep_list = {'\n', ' '}

def extract_tf(text_addr_tel):
    addr_start = -1
    addr_end = -1
    tel_start = -1
    tel_end = -1
    fax_start = - 1
    fax_end = -1
    if len(text_addr_tel) > 8:
        addr_start = 0
        mr = pattern_tf.finditer(text_addr_tel)
        min_tel_pos = len(text_addr_tel)
        for m in mr:
            start_pos = m.span(0)[0]
            min_tel_pos = min(start_pos, min_tel_pos)
            text_tel_fax = m.group(0)
            number_match = pattern_tf_num.search(text_tel_fax)

            if 'F' not in text_tel_fax:
                tel_start, tel_end = number_match.span(0)
                tel_start += start_pos
                tel_end += start_pos
            else:
                fax_start, fax_end = number_match.span(0)
                fax_start += start_pos
                fax_end += start_pos
                idx = number_match.group(0).find("/")
                if idx >= 0:
                    tel_start = fax_start
                    tel_end = idx + tel_start
                    fax_start = idx + 1 + tel_start
        addr_end = min_tel_pos
        while text_addr_tel[addr_start] in sep_list and addr_start < addr_end:
            addr_start += 1
        while text_addr_tel[addr_end - 1] in sep_list and addr_start < addr_end:
            addr_end -= 1
    return [addr_start, addr_end, tel_start, tel_end, fax_start, fax_end]


pattern_47be = re.compile(r"ADDRESS[ ]{0,3}(IS)?[ ]?:?")


def process_47be(text):
    m = pattern_47be.search(text)
    atf = None
    if m is not None:
        idx = m.span(0)[1]
        text_addr_tel_fax = text[idx:]
        atf = extract_tf(text_addr_tel_fax)
        atf = [x + idx if x >= 0 else x for x in atf]
    else:
        atf = extract_tf(text)
        atf[0] = -1
        atf[1] = -1
    return atf


def convert_atf(atf):
    r = []
    for i in range(3):
        k = i * 2
        if atf[k] >= 0 and atf[k + 1] >= 0 and atf[k] < atf[k + 1]:
            r.append((atf[k], atf[k + 1], str(i + 1)))
    return r

def rule_labeling(msg):
    t59, t47, p47 = msg
    corp_start = 0
    corp_end = len(t59[0])
    line_corp = 0 #

    text_59 = '\n'.join(t59)
    if len(t59) > 1 and pattern_number.search(t59[1]) is None:
        corp_end = corp_end + 1 + len(t59[1])
        line_corp = 1

    line_addr_tel = line_corp + 1

    line_47 = 999
    for i, s in enumerate(t59):
        if i > line_corp:
            if s.find('SEE 47') != -1:
                line_47 = i
                break
    text_addr_tel = '\n'.join(t59[line_addr_tel:line_47])
    atf = extract_tf(text_addr_tel)  #  去掉公司名称以后的子串
    r = []
    r.append([text_59, [(corp_start, corp_end, "0")] + convert_atf([x + corp_end + 1 if x >= 0 else x for x in atf])])
    for s in t47:
        r.append([s, convert_atf(process_47be(s))])
    return r

#59字段 下标 标注功能
def fn(appstr):
    c = nltk.word_tokenize(appstr[4:])
    # print(c)
    strArr = ["CO.LTD.", "CO.,LTD", "CO., LTD", "MILL C O,." "LTD  CO.", "LTD", "MILL",
              "CO LTD", "CO.,LIMITED", "CO LTD", "COMPANY", "MANUFACTURING", "LLC", "CO,. LTD",
              "CO.,LT", "CORPORATION LIMITED", "CO.,LTD", "CO.,LTD.", "CO.,LIMITED.", "CO. LTD",
              "LTD. CO.", "LTD.", "CO.", "LTD"]  # 公司标识符字符串数组

    if c[0].startswith('/'):
        companyStartLabel = 1
    else:
        companyStartLabel = 0

    placeEndLabel = len(c) - 1
    placeStartLabel = 2
    companyEndLabel = 1

    for i in range(len(c)):
        # print(c[i])
        for str in strArr:
            if c[i].find(str.strip()) != -1:
                # print(c[i])
                companyEndLabel = i
                placeStartLabel = i + 1

    for p in range(len(c)):
        if (p == companyStartLabel):
            print(c[p], "-ORGB")
        elif (p <= companyEndLabel and p > companyStartLabel):
            print(c[p], "-ORGI")

        elif (p == placeStartLabel):
            print(c[p], "-ADRB")
        elif (p <= placeEndLabel and p > placeStartLabel):
            print(c[p], "-ADRI")

    # print(companyStartLabel)
    # print(companyEndLabel)
    # print(placeStartLabel)
    # print(placeEndLabel)
    return [companyStartLabel, companyEndLabel, placeStartLabel, placeEndLabel]


##get text_addr_tel
def get_text_addr_tel(appstr):
    c = nltk.word_tokenize(appstr[4:])
    # print(c)
    strArr = ["CO.LTD.", "CO.,LTD", "CO., LTD", "MILL C O,." "LTD  CO.", "LTD", "MILL",
              "CO LTD", "CO.,LIMITED", "CO LTD", "COMPANY", "MANUFACTURING", "LLC", "CO,. LTD",
              "CO.,LT", "CORPORATION LIMITED", "CO.,LTD", "CO.,LTD.", "CO.,LIMITED.", "CO. LTD",
              "LTD. CO.", "LTD.", "CO.", "LTD"]  # 公司标识符字符串数组

    if c[0].startswith('/'):
        companyStartLabel = 1
    else:
        companyStartLabel = 0

    placeEndLabel = len(c) - 1
    placeStartLabel = 2
    companyEndLabel = 1

    for i in range(len(c)):
        # print(c[i])
        for str in strArr:
            if c[i].find(str.strip()) != -1:
                # print(c[i])
                companyEndLabel = i
                placeStartLabel = i + 1

    for p in range(len(c)):
        if (p == companyStartLabel):
            print(c[p], "-ORGB")
        elif (p <= companyEndLabel and p > companyStartLabel):
            print(c[p], "-ORGI")

        elif (p == placeStartLabel):
            print(c[p], "-ADRB")
        elif (p <= placeEndLabel and p > placeStartLabel):
            print(c[p], "-ADRI")

    # print(companyStartLabel)
    # print(companyEndLabel)
    # print(placeStartLabel)
    # print(placeEndLabel)

    text_addr_tel = '\n'.join(c[placeStartLabel:placeEndLabel])
    return text_addr_tel


def rule_labeling_new(msg):
    t59, t47, p47 = msg
    corp_start = 0
    corp_end = len(t59[0])
    line_corp = 0 #

    text_59 = '\n'.join(t59)
    if len(t59) > 1 and pattern_number.search(t59[1]) is None:
        corp_end = corp_end + 1 + len(t59[1])  # corp_end...
        line_corp = 1

    line_addr_tel = line_corp + 1

    line_47 = 999
    for i, s in enumerate(t59):
        if i > line_corp:
            if s.find('SEE 47') != -1:
                line_47 = i
                break
    text_addr_tel = '\n'.join(t59[line_addr_tel:line_47])
    atf = extract_tf(text_addr_tel)  #  去掉公司名称以后的子串

    r = []
    r.append([text_59, [(corp_start, corp_end, "0")] + convert_atf([x + corp_end + 1 if x >= 0 else x for x in atf])])
    for s in t47:
        r.append([s, convert_atf(process_47be(s))])
    return r


if __name__ == '__main__':
    a = nlp_pre_process('D:\pp3\data_all.txt')
    msgs = a.view_file()
    print(msgs)
    # c = Counter()
    # lines_59 = []
    # for t59, t47, p47 in msgs:
    #     if p47:
    #         t59 = [x for x in t59 if x.find('SEE 47') != -1][0]
    #         lines_59.append(t59)
    # c.update(lines_59)
    # print(c)
    #
    # head_47 = []
    # for t59, t47, p47 in msgs:
    #     if p47:
    #         addr_47 = [x for x in t47 if x.find('ADDR') != -1]
    #         if len(addr_47) != 1:
    #             print(addr_47)
    #         else:
    #             head_47.append(addr_47[0].split(":")[0].strip())
    # d = Counter(head_47)
    # print(d)

    '''
    e = json.JSONEncoder(ensure_ascii=False, indent=2)
    with open("a.js", "w") as f:
        print("var data=", file=f)
        print(e.encode([rule_labeling(m) for m in msgs]), file=f)
    '''
