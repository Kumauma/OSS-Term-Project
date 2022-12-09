import turtle, random, time, math

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=80):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        
        turtle.register_shape("img\professor.gif")
        turtle.register_shape("img\student.gif")

        # Initialize 'runner' and 'chaser'
        self.runner.shape('img\student.gif')
        self.runner.penup()

        self.chaser.shape('img\professor.gif')
        self.chaser.penup()

        # Instantiate an another turtles for drawing
        self.drawer1 = turtle.RawTurtle(canvas)
        self.drawer1.hideturtle()
        self.drawer1.penup()
        
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup()
        
        self.drawer3 = turtle.RawTurtle(canvas)
        self.drawer3.hideturtle()
        self.drawer3.penup()
        self.drawer3.speed(10)
        self.drawer3.pensize(10)
        self.drawer3.pencolor("#9a6b4b")
        
        self.drawer4 = turtle.RawTurtle(canvas)
        self.drawer4.hideturtle()
        self.drawer4.penup()
        
        self.drawer5 = turtle.RawTurtle(canvas)
        self.drawer5.hideturtle()
        self.drawer5.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, ai_timer_msec=100):
        time.sleep(1)
        turtle.bgcolor("#b5d692")
        self.drawer3.penup()
        self.drawer3.setpos(-350,-350)
        self.drawer3.pendown()
        self.drawer3.forward(750)
        self.drawer3.left(90)
        self.drawer3.forward(700)
        self.drawer3.left(90)
        self.drawer3.forward(750)
        self.drawer3.left(90)
        self.drawer3.forward(700)
        
        self.drawer4.undo()
        self.drawer4.penup()
        self.drawer4.setpos(25, 300)
        self.drawer4.write('Welcome to the Student hunting Game!!!', align='center', font=("Consolas", 20))
        time.sleep(1)
        self.drawer4.setpos(25, 260)
        self.drawer4.write('Rule1. You can hunt the student by moving the professor with an arrow.', align='center', font=("Consolas", 13))
        time.sleep(1)
        self.drawer4.setpos(25, 220)
        self.drawer4.write('Rule2. After 60 seconds, it\'s game over.', align='center', font=("Consolas", 13))
        time.sleep(1)
        self.drawer4.setpos(25, 180)
        self.drawer4.write('Rule3. If you go out of the fence, it\'s game over.', align='center', font=("Consolas", 13))
        time.sleep(1)
        self.drawer4.setpos(25, 140)
        self.drawer4.write('The game will start in 5 seconds...', align='center', font=("Consolas", 13))
        time.sleep(5)
        self.drawer4.clear()
        
        self.runner.setpos(random.randint(-300, 350), random.randint(-300, 300))
        self.runner.showturtle()
        self.runner.setheading(random.randint(0, 360))
        self.runner.speed(10)
        self.chaser.setpos(25, 0)
        self.chaser.showturtle()
        
        self.start_time = time.time()
        self.ai_timer_msec = ai_timer_msec
        self.score = 0
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        curr_time = time.time() - self.start_time
        self.drawer1.undo()
        self.drawer1.penup()
        self.drawer1.setpos(-310, 270)
        self.drawer1.write(f'Time: {math.trunc(curr_time)}/60', align="left", font=("Consolas", 12))
        
        if self.is_catched():
            self.score += 1
            self.runner.hideturtle()
            self.runner = RandomMover(canvas)
            self.runner.shape('img\student.gif')
            self.runner.penup()
            self.runner.setpos(random.randint(-300, 350), random.randint(-300, 300))
            self.runner.showturtle()
            self.runner.setheading(random.randint(0, 360))
            
        self.drawer2.undo()
        self.drawer2.penup()
        self.drawer2.setpos(200, 270)
        self.drawer2.write(f'Hunted Students: {self.score}', font=("Consolas", 12))
        if chaser.xcor() < -350 or chaser.xcor() > 400:
            self.chaser.hideturtle()
            self.runner.hideturtle()
            self.drawer5.undo()
            self.drawer5.penup()
            self.drawer5.setpos(25, 0)
            self.drawer5.write('You broke the Rule3. Game Over!', align='center', font=("Consolas", 20))
        elif chaser.ycor() < -350 or chaser.ycor() > 350:
            self.chaser.hideturtle()
            self.runner.hideturtle()
            self.drawer5.undo()
            self.drawer5.penup()
            self.drawer5.setpos(25, 0)
            self.drawer5.write('You broke the Rule3. Game Over!', align='center', font=("Consolas", 20))
        elif math.trunc(curr_time) <= 60:
            self.canvas.ontimer(self.step, self.ai_timer_msec)
        else:
            self.chaser.hideturtle()
            self.runner.hideturtle()
            self.drawer5.undo()
            self.drawer5.penup()
            self.drawer5.setpos(25, 0)
            self.drawer5.write(f'Time\'s Up! You hunted {self.score} students!', align='center', font=("Consolas", 20))

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=23):
        super().__init__(canvas)
        self.hideturtle()
        self.step_move = step_move

        # Register event handlers
        canvas.onkeypress(lambda: self.goto(self.xcor(), self.ycor() + self.step_move), 'Up')
        canvas.onkeypress(lambda: self.goto(self.xcor(), self.ycor() - self.step_move), 'Down')
        canvas.onkeypress(lambda: self.goto(self.xcor() - self.step_move, self.ycor()), 'Left')
        canvas.onkeypress(lambda: self.goto(self.xcor() + self.step_move, self.ycor()), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=50, step_turn=30):
        super().__init__(canvas)
        self.hideturtle()
        self.step_move = step_move
        self.step_turn = step_turn
        self.speed(10)
        
    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if self.xcor() < -320 or self.xcor() > 370:
            self.right(180)
            self.forward(100)
        elif self.ycor() < -320 or self.ycor() > 320:
            self.right(180)
            self.forward(100)
        elif mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
            self.forward(self.step_move)
        elif mode == 2:
            self.right(self.step_turn)
            self.forward(self.step_move)

if __name__ == '__main__':
    canvas = turtle.Screen()
    canvas.title("Student Hunting Game")
    runner = RandomMover(canvas)
    chaser = ManualMover(canvas)

    game = RunawayGame(canvas, runner, chaser)
    game.start()
    canvas.mainloop()
