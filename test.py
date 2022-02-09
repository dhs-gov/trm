from trm import TRM

trm = TRM()
trm.read_normalized("C:\\work\\projects\\ai-ml\\trm\\testdata\\normalized_1.xlsx")
trm.read_input("C:\\work\\projects\\ai-ml\\trm\\testdata\\input_1.xlsx")

print('*****')
trm.assess_transformer1()
print('*****')
trm.assess_spacy()
print('*****')
trm.assess_nltk()