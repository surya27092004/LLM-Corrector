import os
import pandas as pd

data_dir = 'data'
blueprint_path = os.path.join(data_dir, 'questionAndAnswers.txt')
students_dir = os.path.join(data_dir, 'Students Answersheet')

os.makedirs(students_dir, exist_ok=True)

# Create sample blueprint file if missing
def ensure_sample_blueprint():
    if not os.path.exists(blueprint_path):
        with open(blueprint_path, 'w', encoding='utf-8') as f:
            f.write('Qno|Question Description|Answer_blueprint|Max Marks\n')
            f.write('1|What is the capital of France?|Paris|2\n')
            f.write('2|What is 2+2?|4|1\n')

def ensure_sample_student():
    sample_student_file = os.path.join(students_dir, '1234_John.txt')
    if not os.path.exists(sample_student_file):
        with open(sample_student_file, 'w', encoding='utf-8') as f:
            f.write('Qno|Answer_studnet_response\n')
            f.write('1|Paris\n')
            f.write('2|4\n')

def load_blueprint():
    return pd.read_csv(blueprint_path, delimiter='|')

def load_all_students():
    student_dfs = []
    for filename in os.listdir(students_dir):
        if filename.endswith('.txt'):
            try:
                df = pd.read_csv(os.path.join(students_dir, filename), delimiter='|')
                df['Filename'] = filename
                student_dfs.append(df)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    if not student_dfs:
        return pd.DataFrame()
    all_students_df = pd.concat(student_dfs, ignore_index=True)
    all_students_df['usn_id'] = all_students_df['Filename'].apply(lambda x: x.split('_')[0])
    all_students_df['student_name'] = all_students_df['Filename'].apply(lambda x: x.split('_')[1].replace('.txt', ''))
    return all_students_df

def merge_and_score(blueprint_df, students_df):
    if 'Qno' not in blueprint_df.columns or 'Qno' not in students_df.columns:
        print("'Qno' column missing in one of the DataFrames.")
        return pd.DataFrame()
    merged_df = pd.merge(blueprint_df, students_df, on='Qno', how='inner', suffixes=('_blueprint', '_studnet_response'))
    def score_row(row):
        return int(row['Answer_blueprint'].strip().lower() == str(row['Answer_studnet_response']).strip().lower()) * int(row['Max Marks'])
    merged_df['Marks Obtained'] = merged_df.apply(score_row, axis=1)
    return merged_df

def group_results(merged_df):
    grouped = merged_df.groupby(['usn_id', 'student_name']).agg(
        total_marks_obtained=('Marks Obtained', 'sum'),
        total_max_marks=('Max Marks', 'sum')
    ).reset_index()
    return grouped

def add_new_question():
    blueprint_df = load_blueprint()
    try:
        qno = int(blueprint_df['Qno'].max()) + 1 if not blueprint_df.empty else 1
    except:
        qno = 1
    qdesc = input('Enter question description: ')
    ans = input('Enter answer key: ')
    marks = input('Enter max marks: ')
    with open(blueprint_path, 'a', encoding='utf-8') as f:
        f.write(f'{qno}|{qdesc}|{ans}|{marks}\n')
    print('Question added.')

def add_new_student():
    usn = input('Enter student USN: ')
    name = input('Enter student name: ')
    blueprint_df = load_blueprint()
    answers = []
    for _, row in blueprint_df.iterrows():
        ans = input(f"Answer for Q{row['Qno']} ({row['Question Description']}): ")
        answers.append((row['Qno'], ans))
    filename = f'{usn}_{name}.txt'
    filepath = os.path.join(students_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('Qno|Answer_studnet_response\n')
        for qno, ans in answers:
            f.write(f'{qno}|{ans}\n')
    print('Student answersheet added.')

def view_results():
    students_df = load_all_students()
    if students_df.empty:
        print('No student data.')
        return
    blueprint_df = load_blueprint()
    merged_df = merge_and_score(blueprint_df, students_df)
    grouped = group_results(merged_df)
    print('\nGrouped Results:')
    print(grouped)
    print('\nDetailed Results:')
    print(merged_df)

def view_student_result():
    students_df = load_all_students()
    if students_df.empty:
        print('No student data.')
        return
    usn = input('Enter student USN: ')
    name = input('Enter student name: ')
    blueprint_df = load_blueprint()
    merged_df = merge_and_score(blueprint_df, students_df)
    student_df = merged_df[(merged_df['usn_id'] == usn) & (merged_df['student_name'].str.lower() == name.lower())]
    if student_df.empty:
        print('No data for this student.')
        return
    print(f"\nResults for {usn} {name}:")
    print(student_df)
    total = student_df['Marks Obtained'].sum()
    max_total = student_df['Max Marks'].sum()
    print(f"Total: {total} / {max_total}")

def main_menu():
    ensure_sample_blueprint()
    ensure_sample_student()
    while True:
        print("\n--- Interactive Grading System ---")
        print("1. Grade all students and view results")
        print("2. View result for a specific student")
        print("3. Add a new question")
        print("4. Add a new student answer sheet")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            view_results()
        elif choice == '2':
            view_student_result()
        elif choice == '3':
            add_new_question()
        elif choice == '4':
            add_new_student()
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Try again.')

if __name__ == '__main__':
    main_menu()
