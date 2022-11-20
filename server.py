import socket
import random
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_Address= "127.0.0.1"
port= 8000
server.bind((ip_Address, port))
server.listen()
clients = []
nicknames = []
questions = [
     " What is the Italian word for PIE? \n a.Mozarella\n b.Pasty\n c.Patty\n d.Pizza",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit\n b.Celsius\n c.Rankine\n d.Kelvin",
     " Which sea creature has three hearts? \n a.Dolphin\n b.Octopus\n c.Walrus\n d.Seal",
     " Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary\n b.Jack\n c.Johnny\n d.Mukesh",
     " How many bones does an adult human have? \n a.206\n b.208\n c.201\n d.196",
     " How many wonders are there in the world? \n a.7\n b.8\n c.10\n d.4",
     " What element does not exist? \n a.Xf\n b.Re\n c.Si\n d.Pa",
     " How many states are there in India? \n a.24\n b.29\n c.30\n d.31",
     " Who invented the telephone? \n a.A.G Bell\n b.John Wick\n c.Thomas Edison\n d.G Marconi",
     " Who is Loki? \n a.God of Thunder\n b.God of Dwarves\n c.God of Mischief\n d.God of Gods",
     " Who was the first Indian female astronaut ? \n a.Sunita Williams\n b.Kalpana Chawla\n c.None of them\n d.Both of them ",
     " What is the smallest continent? \n a.Asia\n b.Antarctic\n c.Africa\n d.Australia",
     " The beaver is the national embelem of which country? \n a.Zimbabwe\n b.Iceland\n c.Argentina\n d.Canada",
     " How many players are on the field in baseball? \n a.6\n b.7\n c.9\n d.8",
     " Hg stands for? \n a.Mercury\n b.Hulgerium\n c.Argenine\n d.Halfnium",
     " Who gifted the Statue of Libery to the US? \n a.Brazil\n b.France\n c.Wales\n d.Germany",
     " Which planet is closest to the sun? \n a.Mercury\n b.Pluto\n c.Earth\n d.Venus"
]

answers = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b', 'a']

def getRandomQuestionAnswer(conn):
    random_index =  random.randint(0, len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode("utf-8"))
    return random_index, random_question, random_answer

def removeQuestion(i):
    questions.pop(i)
    answers.pop(i)
def remove(connection, nickname):
    if connection in clients:
        clients.remove(connection) 
    if nickname in nicknames:
        nicknames.remove(nickname)
def clientThread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!\n".encode("utf-8"))
    conn.send("You will recieve a question, the answer to that question must be one of a, b, c or d\n".encode("utf-8"))
    conn.send("Good Luck! \n\n".encode("utf-8"))
    index, ques, ans =getRandomQuestionAnswer(conn)

    while(True):
        try:
            msg = conn.recv(2048).decode("utf-8")
            if msg:
                if msg.lower() == ans:
                  score += 1
                  conn.send(f"Yayayay you got the answer correct! Your score is {score}\n\n".encode("utf-8"))  
                else:
                    conn.send("You got it wrong. Better luck next time!\n".encode("utf-8"))
                removeQuestion(index)
                index, ques, ans = getRandomQuestionAnswer(conn)
            else:
                remove(conn, nickname)
        except:
            continue
while(True):
    connection, address = server.accept()
    connection.send("NICKNAME".encode("utf-8"))
    nickname = connection.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    print(nickname + " connected!")
    clients.append(connection)
    newThread = Thread(target=clientThread, args=(connection,nickname))
    newThread.start()
