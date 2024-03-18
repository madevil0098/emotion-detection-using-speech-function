emotions=['neutral','calm','happy','sad','angry','fearful','disgust','surprised']
lables=[12,17,33,3,0,4,5,9]
import matplotlib.pyplot as plt
data=dict()
for j in range(len(emotions)):
    data[emotions[j]]=lables[j]

courses = list(data.keys())
values = list(data.values())

my_dpi=96
plt.figure(figsize=(620/my_dpi, 220/my_dpi), dpi=my_dpi)

# creating the bar plot
plt.bar(courses, values)

file = "C:\\Users\\jyoti\\OneDrive\\Desktop\\hackathon\\appdata\\finalData\\bca70898-56cb-11ee-b8b1-5cbaef20cbd2\\label0\\lbl_qqa.jpg"


plt.savefig(file)