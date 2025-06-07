import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns



roles_df = pd.read_csv("Roles_Salaries.csv")
departments_df = pd.read_csv("Departments_roles_n_percentage_employeess.csv")

Faker.seed(0)
random.seed(0)
fake = Faker()
 
country_of_birth = { 'USA': 0.60, 'India': 0.14, 'China': 0.12,'Mexico': 0.04,'Canada': 0.03, 'Philippines': 0.03, 'Taiwan': 0.02, 'South Korea': 0.02
}

locale_map = {
    'USA': 'en_US', 'India': 'en_IN', 'China': 'zh_CN', 'Mexico': 'es_MX', 'Canada': 'en_CA', 'Philippines': 'en_PH', 'Taiwan': 'zh_TW', 'South Korea': 'ko_KR'
}

genders = ['female', 'male', 'nonbinary']
gender_weights = [0.49, 0.49, 0.02]

def rand_birthdate():
    age = random.randint(20, 65)
    return datetime.today() - timedelta(days=age * 365)
  
def rand_hiredate(birthdate):
    min_hire = birthdate + timedelta(days=365 * 20)
    company_start = datetime(2010, 1, 1)
    latest_hire = datetime(2024, 12, 31)
    min_hire = max(min_hire, company_start)
    if min_hire > latest_hire:
        return latest_hire  
    return fake.date_between_dates(date_start=min_hire, date_end=latest_hire)

departments_df["weight"] = departments_df["% of employees"].str.replace('%', '').astype(float) / 100
dept_names = departments_df["Department"].tolist()
dept_weights = departments_df["weight"].tolist()


roles_df["Lower"] = roles_df["Lower"].str.replace("[$,]", "", regex=True).astype(float)
roles_df["Upper"] = roles_df["Upper"].str.replace("[$,]", "", regex=True).astype(float)

roles_list = {}
for _, row in roles_df.iterrows():
    dept = row["Department"]
    if dept not in roles_list:
        roles_list[dept] = []
    roles_list[dept].append({
        "role": row["Role"],
        "salary_range": (row["Lower"], row["Upper"])
    })


# Generate 10,000  employees
employees = []

for _ in range(10000):
    country = random.choices(list(country_of_birth.keys()), weights=list(country_of_birth.values()), k=1)[0]
    namef= Faker(locale_map[country])
    birthdate = rand_birthdate()
    hiredate = rand_hiredate(birthdate)
    department = random.choices(dept_names, weights=dept_weights, k=1)[0]
    role_info = random.choice(roles_list[department])
    role = role_info["role"]
    salary = random.randint(int(role_info["salary_range"][0]), int(role_info["salary_range"][1]))
    employee_id = fake.unique.random_int(min=100000000, max=999999999)
    name = namef.name()
    phone = fake.phone_number()
    email = fake.email()
    gender = random.choices(genders, weights=gender_weights, k=1)[0]
    ssid = fake.ssn()

    employees.append({
        "employeeID": employee_id,
        "CountryOfBirth": country,
        "name": name,
        "phone": phone,
        "email": email,
        "gender": gender,
        "birthdate": birthdate.date(),
        "hiredate": hiredate,
        "department": department,
        "role": role,
        "salary": salary,
        "SSID": ssid
    })

emp_df = pd.DataFrame(employees)
emp_df.to_csv("emp_df.csv", index=False)
emp_df.head(10)

print("\nemp_df:")
print("\n\nOutput emp_df.describe(include=’all’)")
print(emp_df.describe(include='all'))
print("\n\nOutput emp_df.head(10):")
#print(emp_df.head(10))
#print(emp_df.head(10).to_string(index=False))
#tryied to better alignment 
print(f"{'employeeID':<12} {'Country':<12} {'name':<25} {'phone':<24} {'email':<30} {'gender':<10} {'birthdate':<12} {'hiredate':<12} {'department':<20} {'role':<35} {'salary':<8} {'SSID':<11}")

for _, row in emp_df.head(10).iterrows():
    print(f"{row['employeeID']:<12} {row['CountryOfBirth']:<12} {row['name']:<25} {row['phone']:<24} {row['email']:<30} {row['gender']:<10} {str(row['birthdate']):<12} {str(row['hiredate']):<12} {row['department']:<20} {row['role']:<35} {row['salary']:<8} {row['SSID']:<11}")

print("\nTotal Payroll:", emp_df["salary"].sum())


def add_value_labels(ax):
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)



#3a. bar chart displaying counts of each CountryOfBirth
fig, ax = plt.subplots(figsize=(8, 5))
emp_df["CountryOfBirth"].value_counts().sort_values(ascending=False).plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("counts of each CountryOfBirth")
ax.set_xlabel("Country")
ax.set_ylabel("Count")
add_value_labels(ax)
plt.tight_layout()
plt.show()

#3b.bar chart displaying counts for each Department
fig, ax = plt.subplots(figsize=(10, 5))
emp_df["department"].value_counts().sort_values(ascending=False).plot(kind='bar', color='lightgreen', ax=ax)
ax.set_title("counts for each Department")
ax.set_xlabel("Department")
ax.set_ylabel("Count")
add_value_labels(ax)
plt.tight_layout()
plt.show()


# 3C 
# # Step 3C: Extract day of week from hiredate
emp_df["hire_dayofweek"] = pd.to_datetime(emp_df["hiredate"]).dt.day_name()
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hire_counts = emp_df["hire_dayofweek"].value_counts().reindex(ordered_days)
fig, ax = plt.subplots(figsize=(10, 5))
hire_counts.plot(kind='bar', color='salmon', ax=ax)
ax.set_title("Employees Hired by Day of the Week")
ax.set_xlabel("Day of the Week")
ax.set_ylabel("Number of Hires")
add_value_labels(ax)
plt.tight_layout()
plt.show()


#3D KDE
plt.figure(figsize=(10, 5))
sns.kdeplot(emp_df["salary"], fill=True, color='purple')
plt.title("KDE Plot of Employee Salaries")
plt.xlabel("Salary")
plt.ylabel("Density")
plt.tight_layout()
plt.show()

#3E
birth_years = pd.to_datetime(emp_df["birthdate"]).dt.year
birth_year_counts = birth_years.value_counts().sort_index()

# Plot
plt.figure(figsize=(10, 5))
birth_year_counts.plot(kind='line', marker='o', color='teal')
plt.title("Number of Employees by Birth Year")
plt.xlabel("Birth Year")
plt.ylabel("Employees")
plt.grid(True)
plt.tight_layout()
plt.show()

#3F
plt.figure(figsize=(12, 6))
for dept in emp_df["department"].unique():
    sns.kdeplot(
        data=emp_df[emp_df["department"] == dept],
        x="salary",
        label=dept,
        fill=True,
        alpha=0.3
    )
plt.title("Salary Distribution by Department")
plt.xlabel("Salary")
plt.ylabel("Density")
plt.legend(title="Department", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


