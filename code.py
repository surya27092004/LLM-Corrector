import pandas as pd

# Load the CSV file with question, answer key, and marks
file_path = r"data\questionAndAnswers.txt"
df = pd.read_csv(file_path,delimiter="|")
question_answer_blueprint_df = pd.read_csv(file_path,delimiter="|")

# Example of how your DataFrame looks
print(df)




import os
import pandas as pd

# Directory path where the files are located
student_score_answersheet_file_path = r"data/Students Answersheet/"

# List to store DataFrames
df_student_all_lst = []

# Loop through all files in the directory
for filename in os.listdir(student_score_answersheet_file_path):
    # Check if the file is a CSV file
    if filename.endswith(".txt"):
        file_path = os.path.join(student_score_answersheet_file_path, filename)
        
        # Read the CSV file into a DataFrame
        df_student = pd.read_csv(file_path,delimiter="|")
        
        # Add a new column for the filename
        df_student['Filename'] = filename
        
        # Append the DataFrame to the list
        df_student_all_lst.append(df_student)

# Optionally, concatenate all DataFrames into a single DataFrame
final_student_df = pd.concat(df_student_all_lst, ignore_index=True)

# Display the final concatenated DataFrame
print(final_student_df)
final_student_df['usn_id'] = final_student_df['Filename'].apply(lambda x: x.split('_')[0])
final_student_df['student_name'] = final_student_df['Filename'].apply(lambda x: x.split('_')[1].replace('.txt', ''))

final_student_df





#New enhancement
final_df = pd.merge(question_answer_blueprint_df, final_student_df, on='Qno', how='inner', suffixes=('_blueprint', '_studnet_response'))

#final_df = final_df.drop(columns=['Qno_studnet_response', 'score_df2'])

final_df





import os
from dotenv import load_dotenv
load_dotenv()

os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
os.environ["OPENAI_API_KEYKEN"]=os.getenv("OPENAI_API_KEY")




import openai
print(openai._version_) 








def generate_scores_for_paper(df):
    """
    Evaluates a student's entire paper based on the correct answers using GPT-4.

    Args:
        df (pd.DataFrame): DataFrame containing questions, correct answers, and max marks and studnet answer or response to each question.

    Returns:
        list: A list of scores for each question.
    """
    # Construct the questions, answers, and student answers into a formatted string
    questions_and_answers = []
    for i, row in df.iterrows():
        question = row['Question Description']
        correct_answer = row['Answer_blueprint']
        student_answer = row['Answer_studnet_response']
        max_marks = row['Max Marks']
        
        # Format the data into a structured string
        questions_and_answers.append(f"""
        Question: {question}
        Correct Answer: {correct_answer}
        Student's Answer: {student_answer}
        Max Marks: {max_marks}
        """)

    # Join all the question-answer pairs into one string
    full_prompt = "\n".join(questions_and_answers) + """
    Based on the student's answers, assign a score out of the maximum marks for each question, and return the scores only. No explanations required.
    """

    try:
        # Call GPT-4 to evaluate the answers for all questions
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or "gpt-3.5-turbo" depending on your choice
            messages=[{
                "role": "system", "content": "You are an assistant helping grade answers."
            }, {
                "role": "user", "content": full_prompt
            }],
            max_tokens=100,  # Adjust token limit as needed based on the number of questions
            temperature=0.7  # Adjust the creativity factor
        )

        # Extract the response (which should contain the scores for each question)
        scores = response['choices'][0]['message']['content'].strip()

        return scores

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        print(f"Error with OpenAI API: {e}")
        return "Error evaluating the paper."

    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {e}")
        return "Unexpected error occurred during evaluation."











res=generate_scores_for_paper(final_df)





res_raw





type(res_raw)
print(res_raw)





import re
res = [int(match.split('/')[0]) for match in re.findall(r'\d+/\d+', res_raw)]




res




final_df["Marks Obtained"]=res
final_df['Marks Obtained'] = pd.to_numeric(final_df['Marks Obtained'], errors='coerce')

final_df






# Group by 'usn_id' and 'student_name', and then aggregate
grouped_df = final_df.groupby(['usn_id', 'student_name']).agg(
    total_marks_obtained=('Marks Obtained', 'sum'),
    total_max_marks=('Max Marks', 'sum')
).reset_index()





grouped_df