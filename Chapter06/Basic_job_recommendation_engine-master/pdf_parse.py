from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import string
import re
import os
import pickle
import dill


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


num_company = 7
train1_size = 150
train2_size = 50
test_size = 50

parse_fields = ['WORK EXPERIENCE', 'EDUCATION', 'SKILLS', 'AWARDS', 'CERTIFICATIONS', 'ADDITIONAL INFORMATION']

companies = ['amazon', 'apple', 'facebook', 'ibm', 'microsoft', 'oracle', 'twitter']


class Experience:
    company = ''
    title = ''
    descripton = ''

    def __init__(self, doc):
        self.title = re.findall(r'^.*', doc)[0].strip()
        self.company = re.split(r'[\n-]', doc)[1].strip()
        self.description = doc[len(re.findall(r'.*\n.*\s-\s.*', doc)[0]):].strip()


def get_fields(doc):
    fields = [''] * (len(parse_fields) + 1)
    last_index = len(doc)
    for i in range(len(fields)):
        field_index = len(fields) - 2 - i
        if field_index == -1:
            fields[0] = doc[0:last_index].strip()
            break
        doc_pos = string.find(doc, '\n' + parse_fields[field_index] + '\n')
        if doc_pos != -1:
            fields[field_index + 1] = doc[doc_pos + len(parse_fields[field_index]) + 2:last_index].strip()
            last_index = doc_pos
    return fields


class Resume:
    fields = [''] * (len(parse_fields) + 1)
    work_experience = []

    def __init__(self, doc):
        last_index = len(doc)
        for i in range(len(self.fields)):
            field_index = len(self.fields) - 2 - i
            if field_index == -1:
                self.fields[0] = doc[0:last_index].strip()
                break
            doc_pos = string.find(doc, '\n' + parse_fields[field_index] + '\n')
            if doc_pos != -1:
                self.fields[field_index + 1] = doc[doc_pos + len(parse_fields[field_index]) + 2:last_index].strip()
                last_index = doc_pos

        work_doc = self.fields[1]

        l = re.findall(r'.+\n.+\s-\s.+', work_doc)
        for i in range(len(l)):
            l[i] = l[i].strip()

        l[:] = (value for value in l if value != '')

        last_index = len(work_doc)
        for i in range(len(l)):
            pos = string.find(work_doc, l[len(l) - i - 1])
            l[len(l) - i - 1] = work_doc[pos:last_index].strip()
            last_index = pos

        for i in range(len(l)):
            e = Experience(l[i])
            self.work_experience.append(e)


rootdir = './resume_scrap/'

list_resumes = []

for i in range(num_company):
    resumes = []
    for filenames in os.walk(rootdir + companies[i] + '/'):
        for filename in filenames[2]:
            if string.find(filename, 'pdf') != -1:
                doc = convert(rootdir + companies[i] + '/' + filename)
                try:
                    r = get_fields(doc)
                    resumes.append(r)
                    print companies[i] + '-' + filename
                except:
                    r = None
    list_resumes.append(resumes)

with open('resume_data.pkl', 'wb') as output:
    dill.dump(list_resumes, output, pickle.HIGHEST_PROTOCOL)








