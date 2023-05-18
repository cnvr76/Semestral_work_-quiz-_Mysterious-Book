# Mysterious book

## Introduction

Mysterious Book is a fun and interactive way to compete with your friends by answering quick test questions. This game is designed to test your knowledge on various topics and enhance your critical thinking skills while having fun. This project was made by using Python, especially, Pygame library. All the graphics created using Blender and Adobe Photoshop.

## Trailer of the game

```
https://youtu.be/GRPIIHZdac0
```

## Prerequisites

To use the program, you'll need to have Python 3.x installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

## Installation

1. Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/cnvr76/Semestral_work_-quiz-_Mysterious-Book.git
```

2. If you want to run the game directly from compiling the code - install the required packages using the command:

```bash
pip3 install -r requirements.txt
```

3. Download a zip folder from my Google Drive by the link below (it contains used images and videos which are important for the program to work correctly, and, if you don't want to install the requirements, the executable file that you need to move to the project folder):

```bash
https://drive.google.com/file/d/1AjZhg4cK9n1_t_5uASrkLtzmPLn8o2t7/view?usp=share_link
```

## Usage

To start the program, run the following command from the project directory in console (or click on the .exe file):

```bash
python3 main.py
```

## Architecture
The Mysterious book game is built with Python 3 (and Pygame) and utilizes the following files:

+ `main.py`: This is the main module that contains all the working code of the game (with classes, functions, etc) and responsible for it's running

+ `config.py`: This module contains all the basic parameters, uploading videos/images/sounds/fonts and almost all of the variables

+ `input_questions.py`: This is the module that contains 2 lists of questions and answers for the the "input-type" questions

+ `pygamevideo.py`: This is externally downloaded module that contains class for playing videos inside Pygame window

+ `TriviaAPI_questions.py`: This module contains API function responsible for taking questions from large Trivia database (ABCD and True/False)

## Conclusion
Congratulations! Now you understand the Mysterious book's codebase and know how to contribute to the project.
