import os
import json
import random

numOfQuestions = 30  ## Cambiar el número de preguntas aquí
questionsPerTopic = {
    1: 5,
    2: 4,
    3: 4,
    4: 2,
    5: 1,
    6: 2,
    7: 1,
    8: 1,
    9: 1,
    10: 2,
    11: 2,
    12: 3,
    13: 2
} ## Elegimos cuántas preguntas de cada tema queremos

def generate_questions(number=1):
    questions = []
    while len(questions) < number:
        for unit in range(1, 14):
            filename = f"Unit{unit}.json"
            if not os.path.exists(filename):
                continue

            with open(filename, "r", encoding='utf-8') as file:
                questionsData = json.load(file)
                available_questions = questionsData["questions"]

                ## Verificar si hay suficientes preguntas en la unidad
                if not available_questions:
                    continue

                if unit in questionsPerTopic:
                    selected_questions = random.sample(available_questions, min(len(available_questions), questionsPerTopic[unit]))
                    for question in selected_questions:
                        question["unit"] = unit
                        if question not in questions:
                            questions.append(question)
                        if len(questions) == number:
                            break
                if len(questions) == number:
                    break
            if len(questions) == number:
                break
    return questions

def create_html_page(questions, index):
    fileOutName = f"./ExamenTest{index}.html"

    html_head = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Empresas</title>
        <style>
            body {font-family: Arial, sans-serif; 
                }
                .question {
                    margin-bottom: 19px;
                }
                .question p {
                    font-weight: bold;
                    font-size: 19px;
                }
                .question span {
                    font-size: 17px;
                    font-style: italic;
                }
                .question li {
                    font-size: 18px;
                    list-style-type: none;
                }
                .correct-answer {
                    display: none;
                    font-weight: bold;
                    font-size: 16px;
                }
                .answered {
                    pointer-events: none;
                }
            
        </style>
        <script>
            function submitForm() {
                var form = document.getElementById("testForm");
                var answers = [];
                var questions = document.getElementsByClassName("question");
                
                for (var i = 0; i < questions.length; i++) {
                    var question = questions[i];
                    var inputs = question.getElementsByTagName("input");
                    var answer = null;
                    
                    for (var j = 0; j < inputs.length; j++) {
                        if (inputs[j].checked) {
                            answer = inputs[j].value;
                            break;
                        }
                    }
                    
                    answers.push(answer);
                }

                var correctAnswers = document.getElementsByClassName("correct-answer");
                
                for (var i = 0; i < correctAnswers.length; i++) {
                    correctAnswers[i].style.display = "block";
                }

                var options = document.getElementsByTagName("input");
                
                for (var i = 0; i < options.length; i++) {
                    options[i].classList.add("answered");
                }

                var scores = calculateScore(answers);
                var scoreDisplay = document.getElementById("scoreDisplay");
                
                scoreDisplay.innerHTML = "Preguntas acertadas: " + scores.correctGlobal + "<br>Preguntas falladas: " + scores.incorrectGlobal + "<br>Puntuación total: " + scores.totalScore + "/10";

                form.elements["submitButton"].disabled = true;

                return false;
            }

            function calculateScore(answers) {
                var correctGlobal = 0;
                var incorrectGlobal = 0;
                var unanswered = 0;

                for (var i = 0; i < answers.length; i++) {
                    var questionIndex = i;
                    var correctOptionInput = document.getElementsByName("correct_" + questionIndex)[0];
                    var correctOption = correctOptionInput.value;

                    if (answers[i] === correctOption) {
                        correctGlobal++;
                    } else if (answers[i] !== null) {
                        incorrectGlobal++;
                    } else {
                        unanswered++;
                    }
                }

                var totalOptions = answers.length;
                var totalCorrect = correctGlobal - Math.floor(incorrectGlobal / 3);  // Restar respuestas correctas por cada tres respuestas incorrectas
                var score = (totalCorrect / totalOptions) * 10;  // Calcular la puntuación como un porcentaje

                if (score < 0) {
                    score = 0;
                }

                var result = {
                    totalScore: score.toFixed(2),
                    correctGlobal: correctGlobal,
                    incorrectGlobal: incorrectGlobal,
                    unanswered: unanswered
                };

                return result;
            }

        </script>
    </head>
    <body>
        <form id="testForm" onsubmit="return submitForm()">
    """

    html_tail = '''
            <input id="submitButton" type="submit" value="Enviar respuestas">
        </form>
        <p id="scoreDisplay"></p>
    </body>
    </html>
    '''

    fileOut = open(fileOutName, "w", encoding='utf-8')
    fileOut.write(html_head)

    for i, question in enumerate(questions[:numOfQuestions]):
        question_number = i + 1  ## Incrementar el número de pregunta
        unit = question["unit"]
        question_text = question["question"]
        options = question["options"]
        correct_option = question["correct_option"]
        option_html = ""
        for j, option in enumerate(options):
            option_letter = chr(ord("A") + j)  ## Convertir el índice en una letra
            option_html += f'<li><input type="radio" name="question_{i}" value="{option_letter}"> {option_letter}) {option}</li>'

        correct_html = f'<p class="correct-answer">Respuesta correcta: {chr(ord("A") + correct_option)}</p>'
        correct_hidden_input = f'<input type="hidden" name="correct_{i}" value="{chr(ord("A") + correct_option)}">'

        fileOut.write(f"""
        <div class="question">
            <p>{question_number}: {question_text} <span>[Tema {unit}]</span></p>  <!-- Mostrar el número de pregunta y el tema -->
            <ul>
                {option_html}
            </ul>
            {correct_html}
            {correct_hidden_input}
        </div>
        """)

    fileOut.write(html_tail)
    fileOut.close()

for i in range(1, 11): # Hacer 10 exámenes
    questions = generate_questions(numOfQuestions)
    create_html_page(questions, i)
