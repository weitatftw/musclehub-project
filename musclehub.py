from codecademySQL import sql_query


# Examine visits here
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')

# Examine fitness_tests here
sql_query('''
SELECT *
FROM fitness_tests
LIMIT 5
''')

# Examine applications here
sql_query('''
SELECT *
FROM applications
LIMIT 5
''')

# Examine purchases here
sql_query('''
SELECT *
FROM purchases
LIMIT 5
''')

df = sql_query('''
SELECT visits.first_name, visits.last_name, visits.gender, visits.email, visits.visit_date, fitness_tests.fitness_test_date, applications.application_date, purchases.purchase_date 
FROM visits
LEFT JOIN fitness_tests
ON visits.first_name = fitness_tests.first_name AND visits.last_name = fitness_tests.last_name AND visits.email = fitness_tests.email
LEFT JOIN applications
ON visits.first_name = applications.first_name AND visits.last_name = applications.last_name AND visits.email = applications.email
LEFT JOIN purchases
ON visits.first_name = purchases.first_name AND visits.last_name = purchases.last_name AND visits.email = purchases.email
WHERE visits.visit_date >= '7-1-17'
''')

import pandas as pd
from matplotlib import pyplot as plt


aorb = lambda x: 'A' if pd.notnull(x) else 'B' 
df['ab_test_group'] = df.fitness_test_date.apply(aorb)
ab_counts = df.groupby(df.ab_test_group).first_name.count().reset_index()
print(ab_counts)

labels=['A', 'B']
plt.pie(ab_counts.first_name, labels=labels, autopct='%.0f%%')
plt.axis('equal')
plt.savefig('ab_test_pie_chart.png')

applied = lambda x: 'Application' if pd.notnull(x) else 'No Application'
df['is_application'] = df.application_date.apply(applied)
app_counts = df.groupby([df.is_application, df.ab_test_group]).first_name.count().reset_index()
print(app_counts)
app_pivot = app_counts.pivot(index='ab_test_group', columns='is_application', values='first_name').reset_index()
print(app_pivot)
app_pivot['Total'] = app_pivot['Application'] + app_pivot['No Application']
print(app_pivot)
app_pivot['Percent with Application'] = app_pivot.Application / app_pivot.Total
print(app_pivot)

from scipy.stats import chi2_contingency


contingency = [[250, 2254], [325, 2175]]
chi2, pval, froq, dof = chi2_contingency(contingency)
print(pval)

member = lambda x: 'Member' if pd.notnull(x) else 'Not Member'
df['is_member'] = df.purchase_date.apply(member)

just_apps = df[df['is_application'] == 'Application']
print(just_apps)
just_appscounts = just_apps.groupby(['is_member', 'ab_test_group']).first_name.count().reset_index()
member_pivot = just_appscounts.pivot(index='ab_test_group', columns='is_member', values='first_name').reset_index()
member_pivot['Total'] = member_pivot['Member'] + member_pivot['Not Member']
member_pivot['Percent Purchase'] = member_pivot['Member'] / member_pivot['Total']
print(member_pivot)

contingency2 = [[200, 50], [250, 75]]
chi22, pval2, froq2, dof2 = chi2_contingency(contingency2)
print(pval2)

everybodycounts = df.groupby(['is_member', 'ab_test_group']).first_name.count().reset_index()
final_member_pivot = everybodycounts.pivot(index='ab_test_group', columns='is_member', values='first_name').reset_index()
final_member_pivot['Total'] = final_member_pivot['Member'] + final_member_pivot['Not Member']
final_member_pivot['Percent Purchase'] = final_member_pivot['Member'] / final_member_pivot['Total']
print(final_member_pivot)

contingency3 = [[200, 2304], [250, 2250]]
chi23, pval3, froq3, dof3 = chi2_contingency(contingency3)
print(pval3)

ax = plt.subplot()
plt.bar(range(len(app_pivot)), height=app_pivot['Percent with Application'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15])
ax.set_yticklabels(['0%', '5%', '10%', '15%'])
plt.title('Percentage of People Who Applied')
plt.show()
plt.savefig('Breakdown of Percentages for Applications.png')

ax2 = plt.subplot()
plt.bar(range(len(member_pivot)), height=member_pivot['Percent Purchase'].values)
ax2.set_xticks(range(len(member_pivot)))
ax2.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax2.set_yticks([0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90])
ax2.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%'])
plt.title('Percentage of those who bought the membership in those who applied ')
plt.show()
plt.savefig('Breakdown of Percentages of Purchases in those who applied.png')

ax3 = plt.subplot()
plt.bar(range(len(final_member_pivot)), height=final_member_pivot['Percent Purchase'].values)
ax3.set_xticks(range(len(final_member_pivot)))
ax3.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax3.set_yticks([0, 0.025, 0.050, 0.075, 0.100])
ax3.set_yticklabels(['0%', '2.5%', '5%', '7.5%', '10%'])
plt.title('Percentages of Purchases among all people')
plt.show()
plt.savefig('Breakdown of Percentages of Purchases among all people.png')
