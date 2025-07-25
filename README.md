# LLM-Corrector
This project automates the process of grading subjective student answers by leveraging a Large Language Model (LLM) – specifically OpenAI's GPT-4. It compares student responses against a predefined answer key and assigns scores, streamlining the evaluation process for educators.

Features
Batch Processing: Reads multiple student answer sheets from a specified directory.

Data Integration: Merges student responses with a blueprint containing questions, correct answers, and maximum marks.

LLM-Powered Grading: Utilizes OpenAI's GPT-4 (or a similar model) to evaluate student answers based on the provided correct answer and assign a score for each question.

Structured Output: Generates a summary DataFrame showing each student's total marks obtained and total maximum marks.

Dynamic Data Handling: Uses Pandas for efficient data loading, manipulation, and merging of answer sheets.

How It Works
Blueprint Loading: The system first loads a questionAndAnswers.txt file, which serves as the blueprint, containing the question number (Qno), question description, the correct answer, and the maximum marks for each question.

Student Answer Sheet Loading: It then iterates through all .txt files in the data/Students Answersheet/ directory. Each file is expected to contain a student's responses, including their USN and name (extracted from the filename).

Data Merging: Student answers are merged with the question blueprint based on the question number (Qno).

LLM Evaluation: For each question, a detailed prompt is constructed including the question, correct answer, student's answer, and maximum marks. This prompt is sent to the OpenAI GPT-4 model.

The LLM is instructed to return only the obtained score for each question in a specific format (e.g., X/Y or just X).

The raw response from the LLM is parsed to extract numerical scores.

Score Aggregation: The individual question scores obtained from the LLM are added to the merged DataFrame.

Final Summary: The scores are aggregated by student (USN and name) to provide a final summary of total marks obtained against total maximum marks for their entire paper.

Setup and Installation
Prerequisites
Python 3.8+

An OpenAI API Key.

Familiarity with the command line/terminal.

1. Project Structure
Ensure your project directory is organized as follows:

.
├── grade_answers.py             # Your main Python script
├── .env                         # Stores your API keys (create this file)
└── data/
    ├── questionAndAnswers.txt   # Blueprint file
    └── Students Answersheet/
        ├── <USN>_<StudentName>.txt
        ├── <USN>_<StudentName>.txt
        └── ...
2. Create data Directory and Files
data/questionAndAnswers.txt:
This file should be a pipe-separated (|) CSV file with the following columns: Qno, Question Description, Answer, Max Marks.
Example questionAndAnswers.txt:

Qno|Question Description|Answer|Max Marks
1|What is the capital of France?|Paris|5
2|Explain the concept of photosynthesis.|Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with chlorophyll.|10
data/Students Answersheet/<USN>_<StudentName>.txt:
Each student's answer sheet should be a pipe-separated (|) CSV file containing Qno and Answer columns. The filename format is crucial for extracting USN and student name.
Example 1MS18CS001_Alice.txt:

Qno|Answer
1|Paris
2|It's how plants make food using sun.
Example 1MS18CS002_Bob.txt:

Qno|Answer
1|London
2|Photosynthesis is a process used by plants to convert light energy into chemical energy that can later be released to fuel the organisms' activities.
3. Create .env File
In the root of your project directory, create a file named .env and add your API keys:

OPENAI_API_KEY="sk-YOUR_OPENAI_API_KEY_HERE"
# HF_TOKEN="hf_YOUR_HUGGINGFACE_TOKEN_HERE" # (Optional: included in code but not used for this functionality)
Important: Replace "sk-YOUR_OPENAI_API_KEY_HERE" with your actual OpenAI API key. Do not share your API key publicly.

4. Install Dependencies
It's highly recommended to use a virtual environment to manage dependencies.

Bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Now, install the required Python packages:

Bash

pip install pandas python-dotenv openai
5. Verify OpenAI API Version
The script uses features of a modern OpenAI Python library. You can check your installed version:

Bash

python -c "import openai; print(openai.__version__)"
If it's an older version (e.g., 0.28.x), you might consider upgrading: pip install --upgrade openai.

Running the Grader
Activate your virtual environment (if not already active).

Run the Python script:

Bash

python grade_answers.py # Or whatever you named your script
The script will:

Load the blueprint and student answer sheets.

Print the loaded DataFrames for verification.

Call the OpenAI API for each student's paper to generate scores.

Print the raw response from OpenAI.

Print the parsed scores.

Finally, print the final_df with Marks Obtained and the grouped_df showing total marks for each student.

Important Considerations and Limitations
OpenAI API Usage and Cost: Each call to the OpenAI API incurs a cost. Be mindful of the number of student papers and questions, as this can lead to significant API usage.

Rate Limits: The OpenAI API has rate limits. If you process a very large number of answers, you might hit these limits, leading to errors. Implementing a delay or retry mechanism might be necessary for large datasets.

LLM Accuracy and Bias: The accuracy of grading heavily depends on the LLM's understanding and its inherent biases. Reviewing the graded papers manually is still recommended for critical assessments.

Prompt Engineering: The current prompt is designed to extract scores. Experimenting with different prompt structures can significantly influence the grading quality and consistency of the LLM's output.

Output Format Consistency: The parsing of LLM output (re.findall(r'\d+/\d+', res_from_openai)) relies on the LLM consistently returning scores in "Obtained/Max" format. Inconsistent LLM output will lead to parsing errors.

Internet Connection: An active internet connection is required to communicate with the OpenAI API.

HF_TOKEN: The script loads HF_TOKEN from .env, but it is not utilized in the provided code logic. It might be a remnant from a previous iteration or intended for future integration with Hugging Face models.

Future Enhancements
Error Handling for LLM Responses: Implement more robust error handling for unexpected LLM responses (e.g., not returning scores in the expected format, API errors).

Rate Limit Management: Add exponential backoff or a queuing system for OpenAI API calls to handle rate limits gracefully.

Configurable LLM Model: Allow users to easily switch between different OpenAI models (e.g., gpt-3.5-turbo, gpt-4o) or even integrate other LLMs (e.g., Hugging Face models, local LLMs).

Detailed Feedback: Modify the LLM prompt to request not just scores, but also brief explanations for the score, and then parse this feedback for educators.

Output to Excel/PDF: Save the final graded results into a more user-friendly format like an Excel spreadsheet or PDF report.

Caching: Implement caching for LLM responses to avoid re-grading the same answers if the script is run multiple times.

User Interface: Develop a more interactive GUI to upload files, configure settings, and view results.

Handling Diverse Question Types: Extend the system to better handle different question types (e.g., multiple choice, true/false, fill-in-the-blanks) alongside subjective answers.
