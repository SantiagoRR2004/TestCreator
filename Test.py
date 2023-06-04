from random import randint
import json

questionsOfEachUnit = {key: 0 for key in range(1, 14)}
numOfQuestions= 30
questions = []

for i in range(numOfQuestions):
    x = randint(1, 13)
    questionsOfEachUnit[x] += 1

for unit in questionsOfEachUnit.keys():
    with open("Unit"+str(unit)+".json", "r") as file:
        questionsData = json.load(file)
        numOfQuestionsInUnit = len(questionsData["questions"])
        for i in range(questionsOfEachUnit[unit]):
            x = randint(0, numOfQuestionsInUnit-1)
            questions.append(questionsData["questions"][x])


fileOutName = "./ExamenTest.html"

html_head = """
<html>
<head>
    <title>Empresas</title>
</head>
</body>
"""

html_tail='''
</body>
</hmtl>
'''


fileOut = open(fileOutName, "w")
fileOut.write(html_head)

for question in questions:
    question_text = question["question"]
    options = question["options"]
    option_html = ""
    for i, option in enumerate(options):
        option_letter = chr(ord("A") + i)  # Convert index to letter
        option_html += f"<li>{option_letter}) {option}</li>"
    correct_html = "Correct:" + chr(ord("A") + question["correct_option"])
    fileOut.write(f"""
    <div>
        <p>{question_text}</p>
        <ul>
            {option_html}
        </ul>
        <p>{correct_html}</p>
    </div>
    """)

fileOut.write(html_tail)
fileOut.close()






