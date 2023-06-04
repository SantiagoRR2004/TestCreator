import os
import json
import random

numOfQuestions = 30  ## Cambiar el número de preguntas aquí

def make_test(number=1):
    for i in range(number):
        questions = []
        for unit in range(1, 14):
            with open(f"Unit{unit}.json", "r", encoding='utf-8') as file:
                questionsData = json.load(file)
                available_questions = questionsData["questions"]
                
                ## Verificar si hay suficientes preguntas en la unidad
                if not available_questions:
                    continue
                
                ## Seleccionar preguntas sin repetir
                selected_questions = random.sample(available_questions, min(len(available_questions), numOfQuestions))
                
                for question in selected_questions:
                    if question not in questions:
                        questions.append(question)
                    if len(questions) == numOfQuestions:
                        break

        fileOutName = f"./ExamenTest1.html"

        ## Verificar la existencia del archivo y actualizar el nombre si es necesario
        fileIndex = 2
        while os.path.exists(fileOutName):
            fileOutName = f"./ExamenTest{fileIndex}.html"
            fileIndex += 1

        html_head = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Empresas</title>
            <style>
                .question {
                    margin-bottom: 20px;
                }
                .question p {
                    font-weight: bold;
                    font-size: 20px;
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
                    
                    // Mostrar las respuestas después de enviar el formulario
                    var correctAnswers = document.getElementsByClassName("correct-answer");
                    for (var i = 0; i < correctAnswers.length; i++) {
                        correctAnswers[i].style.display = "block";
                    }
                    
                    // Bloquear las opciones después de enviar el formulario
                    var options = document.getElementsByTagName("input");
                    for (var i = 0; i < options.length; i++) {
                        options[i].classList.add("answered");
                    }
                    
                    // Calcular puntuación total
                    var score = calculateScore(answers);
                    var scoreDisplay = document.getElementById("scoreDisplay");
                    scoreDisplay.innerHTML = "Puntuación total: " + score;
                    
                    return false;
                }
                
                function calculateScore(answers) {
                    var correctCount = 0;
                    for (var i = 0; i < answers.length; i++) {
                        var questionIndex = i;
                        var correctOptionInput = document.getElementsByName("correct_" + questionIndex)[0];
                        var correctOption = correctOptionInput.value;
                        if (answers[i] === correctOption) {
                            correctCount++;
                        }
                    }
                    var totalOptions = answers.length;
                    var score = (correctCount / totalOptions) * 100;
                    return score.toFixed(2) + "%";
                }
            </script>
        </head>
        <body>
            <form id="testForm" onsubmit="return submitForm()">
        """

        html_tail = '''
                <input type="submit" value="Enviar respuestas">
            </form>
            <p id="scoreDisplay"></p>
        </body>
        </html>
        '''

        fileOut = open(fileOutName, "w", encoding='utf-8')
        fileOut.write(html_head)

        for i, question in enumerate(questions[:numOfQuestions]):
            question_number = i + 1  ## Incrementar el número de pregunta
            
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
                <p>{question_number}: {question_text}</p>  <!-- Mostrar el número de pregunta -->
                <ul>
                    {option_html}
                </ul>
                {correct_html}
                {correct_hidden_input}
            </div>
            """)

        fileOut.write(html_tail)
        fileOut.close()


make_test(10) ## Número de exámenes se que quiere generar
