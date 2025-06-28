import sqlite3
import matplotlib.pyplot as plt
import numpy as np

con = sqlite3.connect('socialmedia.sqlt.db')
cur = con.cursor()

'''3. პრინტავს თითოეულ ჩანაწერს ბაზიდან, სადაც ქვეყანა=საქართველოა '''
cur.execute("SELECT * FROM Students WHERE Country='Georgia'")
result = cur.fetchall()
for row in result:
    print(row)




'''5. მონაცემების შეცვლა'''
student_id = input("შეიყვანე Student_ID, რომლის მონაცემების განახლება გინდა: ")
print("განაახლეთ მონაცემები ამ სტუდენტზე.")
age = input("age: ")
gender = input("gender: ")
level = input("academic level: ")
country = input("country: ")
usage = input("average daily usage in hours: ")
platform = input("most used platformა: ")
impact = input("affects academic performance? (Y/N): ")
sleep = input("sleep hours: ")
mental = input("mental health score: ")
relationship = input("relationship status: ")
conflict = input("conflicts over social media (numbers): ")
addiction = input("Adddicted Score: ")

cur.execute("""
    UPDATE Students
    SET Age = ?, Gender = ?, Academic_Level = ?, Country = ?, Avg_Daily_Usage_Hours = ?,
        Most_Used_Platform = ?, Affects_Academic_Performance = ?, Sleep_Hours_Per_Night = ?, Mental_Health_Score = ?,
        Relationship_Status = ?, Conflicts_Over_Social_Media = ?, Addicted_Score = ?
    WHERE Student_ID = ?
""", (age, gender, level, country, usage, platform, impact, sleep, mental,
      relationship, conflict, addiction, student_id))

con.commit()

print(f"Student_ID {student_id}-ის მონაცემები განახლდა.")



'''6.სტუდენტის მონაცემების ამოშლა ID-ის მიხედვით'''
# მომხმარებელს ვთხოვთ მიუთითოს წაშლის კრიტერიუმი – Student_ID
student_id = input("შეიყვანეთ Student_ID, რომლის ჩანაწერის წაშლა გსურთ: ")

# ვასრულებთ წაშლის ბრძანებას კონკრეტული Student_ID-ის მიხედვით
cur.execute("DELETE FROM Students WHERE Student_ID = ?", (student_id,))

# ვამყარებთ ცვლილებებს ბაზაში
con.commit()

print(f"Student_ID {student_id}-ის ჩანაწერი წაიშალა წარმატებით.")




'''სტუდენტების რაოდენობა'''
def gender_count(gender):
    return cur.execute('SELECT count(*) FROM Students WHERE Gender=:a',{'a':gender}).fetchone()[0]

male_count = gender_count('Male')
female_count = gender_count('Female')
students_count = male_count + female_count
# print(male_count)
# print(female_count)
#
'''
ხელს უშლის თუ არა სოციალური მედია სტუდენტი აკადემიურ მოსწრებას
'''
def affects_academic(gender):
    return cur.execute('SELECT count(*) FROM Students WHERE Gender=:a and Affects_Academic_Performance=:b',{'a':gender,"b":"Yes"}).fetchone()[0]
def doesnt_Affects_Academic(gender):
    return cur.execute("SELECT count(*) FROM Students WHERE Gender=:a AND Affects_Academic_Performance=:b",{'a':gender,"b":"No"}).fetchone()[0]

female_yes = affects_academic('Female')
male_yes = affects_academic('Male')
female_no = doesnt_Affects_Academic('Female')
male_no = doesnt_Affects_Academic('Male')
affects = female_yes + male_yes
not_affects = male_no + female_no
print(affects)
print(not_affects)

#3matplotlib-ის გამოყენება
labels = ['Yes', "No" ]
sizes = [affects, not_affects]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')

ax.legend(loc='best',)
ax.set_title("Does Social Media Affect Academic Studies\n of students?")
plt.show()


'''
4.ცხრილში ახალი მონაცემების შეტანა input-ით
'''
def insert_input():
    student_id = students_count + 1
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    academic_level = input("Enter Academic Level: ")
    country = input("Enter Country: ")
    avg_hours = float(input("Enter Avg_Daily_Usage_Hours: "))
    used_platform = input("Enter Your Most Used Platform: ")
    affects_studies = input("Does Social Media Affect Your Academic Performance (Yes/No): ")
    sleep_hours = float(input("Enter How Many Hours Of Sleep You Get: "))
    mental_score = int(input("Enter Mental Health Score: "))
    relationship = input("Enter Relationship Status: ")
    conflicts = int(input("Enter Number of Conflicts Over Social Media: "))
    addiction = int(input("Enter Addiction Score: "))

    cur.execute("INSERT INTO Students (Student_ID, Age, Gender, Academic_Level, Country,"
                "Avg_Daily_Usage_Hours, Most_Used_Platform,Affects_Academic_Performance, Sleep_Hours_Per_Night, Mental_Health_Score, Relationship_Status,"
                "Conflicts_Over_Social_Media, Addicted_Score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(student_id,age,gender,academic_level, country,avg_hours,
                used_platform,affects_studies, sleep_hours,mental_score,relationship,conflicts,addiction))

    con.commit()

insert_input()


'''
ბაზაში არსებული პლატფორმები
'''
cur.execute("SELECT DISTINCT Most_Used_Platform FROM students")
platforms = [row[0] for row in cur.fetchall()]

'''რამდენს უწერია თითოეული პლატფორმა'''
platforms_values = {}
for each in platforms:
    cur.execute("SELECT COUNT(*) FROM students WHERE Most_Used_Platform = ?", (each,))
    count = cur.fetchone()[0]
    platforms_values[each] = count
print(platforms_values)
count = 0

# პლათფორმა და რაოდენობა
platforms = list(platforms_values.keys())
counts = list(platforms_values.values())

''' ბარის დიაგრამა
 სტუდენტების მიერ ყველაზე ხშირად გამოყენებული სოციალური პლატფორმის მიხედვით '''
plt.figure(figsize=(10, 6))
plt.bar(platforms, counts, color='skyblue')

plt.title('Most Used Social Media Platforms', fontsize=14)
plt.xlabel('Platform', fontsize=12)
plt.ylabel('Number of Users', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()


plt.show()



'''ხაზოვანი დიაგრამა სოციალურ მედიაზე დამოკიდებულება ასაკის მიხედვით'''
cur.execute("SELECT Age, Addicted_Score FROM Students ORDER BY Age")
data = cur.fetchall()

print(data)
#აქ თითოეულ ასაკზე გამოვთვლი სოციალურ მედიაზე დამოკიდებულების საშუალოს
avg18, avg19, avg20, avg21, avg22, avg23, avg24 = 0, 0, 0, 0, 0, 0, 0
count18, count19, count20, count21, count22, count23, count24 = 0, 0, 0, 0, 0, 0, 0
for each in data:
    if each[0] == 18:
        count18 += 1
        avg18 += each[1]
    elif each[0] == 19:
        count19 += 1
        avg19 += each[1]
    elif each[0] == 20:
        count20 += 1
        avg20 += each[1]
    elif each[0] == 21:
        count21 += 1
        avg21 += each[1]
    elif each[0] == 22:
        count22 += 1
        avg22 += each[1]
    elif each[0] == 23:
        count23 += 1
        avg23 += each[1]
    elif each[0] == 24:
        count24 += 1
        avg24 += each[1]
avg18 /= count18
avg19 /= count19
avg20 /= count20
avg21 /= count21
avg22 /= count22
avg23 /= count23
avg24 /= count24
print(avg18, avg19, avg20, avg21, avg22, avg23, avg24)

#xazovani diagrama
t = np.arange(18,25)
s = avg18, avg19, avg20, avg21, avg22, avg23, avg24

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='age', ylabel='addiction score',
       title='average addiction score on social media')
ax.grid()

fig.savefig("test.png")
plt.show()




con.commit()
con.close()