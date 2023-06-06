from random import randint
import json
import copy

def questionGenerator(numOfQuestions = 30):
    questionsOfEachUnit = {key: 0 for key in range(1, 14)}
    questions = []

    for i in range(numOfQuestions):
        x = randint(1, 13)
        questionsOfEachUnit[x] += 1

    for unit in questionsOfEachUnit.keys():
        with open("Unit"+str(unit)+".json", "r") as file:
            questionsData = json.load(file)
            numOfQuestionsInUnit = len(questionsData["questions"])

            enoughQuestions = (questionsOfEachUnit[unit] <= numOfQuestionsInUnit)
            print(enoughQuestions)

            while questionsOfEachUnit[unit] > 0:
                x = randint(0, numOfQuestionsInUnit-1)
                questionAdded = copy.deepcopy(questionsData)
                questionAdded = questionAdded["questions"][x]
                questionAdded["question"] = "Tema "+str(unit)+": "+questionAdded["question"]

                if enoughQuestions and questionAdded not in questions:
                    questions.append(questionAdded)
                    questionsOfEachUnit[unit] -= 1

                elif not enoughQuestions:
                    questions.append(questionAdded)
                    questionsOfEachUnit[unit] -= 1

    return questions



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

numOfQuestions = 30

questions = questionGenerator(numOfQuestions)

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






