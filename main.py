from copy import deepcopy
import pygame
import random
from genome import Genome
import numpy as np
# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [1000, 250]
screen = pygame.display.set_mode(size)

title = "jump"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

class obj :
    def __init__(self) :
        self.survive = True
        self.fitness = 0
        self.level = 0
        self.x = 0
        self.y = 0
        self.move = 0
        self.jump_state = False
        self.jump_down = False
    
    def put_img(self, addr) :
        if addr[-3:] == "png" :
            self.img = pygame.image.load(addr).convert_alpha()
        else :
            self.img = pygame.image.load(addr)
            self.ss_sx, self.ss_sy = self.jumper.get_size()

    def change_size(self, sx, sy) :
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self) :
        screen.blit(self.img, (self.x, self.y))

def crash(a, b) :
    if (a.x - b.sx <= b.x) and (b.x <= a.x+a.sx) :
        if (a.y - b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else :
            return False
    else :
        return False

def actions(outputs) :
    max_index = np.argmax(outputs)
    if max_index == 0 :
        res = "stop"
    elif max_index == 1 :
        res = "sit"
    elif max_index == 2 :
        res = "jump"

    return res
    
m_list = []
wall_list = []

black = (0, 0, 0)
white = (255, 255, 255)
k = 0

score = 0

N_POPULATION = 100
N_BEST = 10
PROB_MUTATION = 0.1

JUMP_POWER = 200



genomes = [Genome() for _ in range(N_POPULATION)]
best_genomes = None
n_generated = 0

jumper = deepcopy(obj())
jumper.put_img("C:/project/딥러닝/python/점프게임/temp/jumper.png")
jumper.change_size(40, 40)
jumper.x = 100
jumper.y = size[1] - jumper.sy

jumper_list = []

generated = 0
_time = 0

# 4. 메인 이벤트
SB = 0
while SB == 0 :
    # 4-1. FPS 설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            SB = 1

    keys = pygame.key.get_pressed()

    
    # 4-3. 입력, 시간에 따른 변화
    if len(jumper_list) == 0 :
        jumper_list = [deepcopy(obj()) for _ in range(N_POPULATION)]
        for i in range(N_POPULATION) :
            jumper_list[i].put_img("C:/project/딥러닝/python/점프게임/temp/jumper.png")
            jumper_list[i].change_size(40, 40)
            jumper_list[i].x = 100
            jumper_list[i].y = size[1] - jumper_list[i].sy
    
    surviver_numbers = 0
    for jumper in jumper_list :
        if jumper.survive == True :
           surviver_numbers += 1
           
    if surviver_numbers > 0:
        _time += 1
        
        if _time % 100 == 0 :
            wall = obj()
            wall.put_img("C:/project/딥러닝/python/점프게임/temp/wall.png")
            level = random.randrange(1,5)
            wall.level = level
            if level == 1 :
                wall.change_size(20, 60)
                wall.x = size[0]
                wall.y = size[1] - wall.sy
            elif level == 2 :
                wall.change_size(20, 80)
                wall.x = size[0]
                wall.y = size[1] - wall.sy
            elif level == 3 :
                wall.change_size(20, 40)
                wall.x = size[0]
                wall.y = size[1] - wall.sy - 30
            elif level == 4 :
                wall.change_size(20, 150)
                wall.x = size[0]
                wall.y = size[1] - wall.sy - 30
            elif level == 5 :
                wall.change_size(20, 200)
                wall.x = size[0]
                wall.y = size[1] - wall.sy - 30

            wall.move = 5
            wall_list.append(wall)
        
        d_list = []
        
        for i in range(len(wall_list)) :
            wall = wall_list[i]
            wall.x -= wall.move
            if wall.x <= 0 :
                d_list.append(i)
        
        for d in d_list:
            score += 1
            del wall_list[d]
            for i in range(N_POPULATION) :
                if jumper_list[i].survive == True :
                    genomes[i].fitness += 1

        for i in range(len(wall_list)) :
            wall = wall_list[i]
            for j in range(len(jumper_list)) :
                if crash(wall, jumper_list[j]) == True :
                    jumper_list[j].survive = False
                    genomes[j].fitness -= 5            
        

        if len(wall_list) != 0 :
            level = wall_list[0].level * 0.25
            wall_position = 1 - wall_list[0].x * 0.001
        else :
            level = 0
            wall_position = 0
        
        inputs = np.array([level, wall_position])

        for i in range(N_POPULATION) :
            outputs = genomes[i].forward(inputs)
            action = actions(outputs)

            if jumper_list[i].survive == True :
                if jumper_list[i].jump_state == False : 
                    if action == "stop" :
                        jumper_list[i].change_size(40, 20) 
                        jumper_list[i].y = size[1] - jumper_list[i].sy
                    
                    if action == "sit" :
                        jumper_list[i].change_size(40, 40)
                        jumper_list[i].y = size[1] - jumper_list[i].sy

                if action == "jump" : 
                    jumper_list[i].jump_state = True

                if jumper_list[i].jump_state == True and jumper_list[i].jump_down == False:
                    jumper_list[i].y -= 8
                    if jumper_list[i].y < size[1] - JUMP_POWER  :
                        jumper_list[i].jump_down = True
                
                if jumper_list[i].jump_state == True and jumper_list[i].jump_down == True :
                    jumper_list[i].y += 8
                    if jumper_list[i].y >= size[1] - jumper_list[i].sy :
                        jumper_list[i].jump_state = False
                        jumper_list[i].jump_down = False
    else :
        # generate
        score = 0
        wall_list = []
        genomes.sort(key=lambda x: x.fitness, reverse=True)
        best_genomes = deepcopy(genomes[:N_BEST])
        print("best fitness : {}".format(best_genomes[0].fitness))
        
        for i in range(N_POPULATION - N_BEST):
            new_genome = deepcopy(best_genomes[0])
            a_genome = random.choice(best_genomes)
            b_genome = random.choice(best_genomes)

            cut = random.randint(0, new_genome.w1.shape[1])
            j = random.randint(0, len(new_genome.w1)-1)
            new_genome.w1[j, :cut] = a_genome.w1[j, :cut]
            new_genome.w1[j, cut:] = b_genome.w1[j, cut:]

            cut = random.randint(0, new_genome.w2.shape[1])
            j = random.randint(0, len(new_genome.w2)-1)
            new_genome.w2[j, :cut] = a_genome.w2[j, :cut]
            new_genome.w2[j, cut:] = b_genome.w2[j, cut:]

            cut = random.randint(0, new_genome.w3.shape[1])
            j = random.randint(0, len(new_genome.w3)-1)
            new_genome.w3[j, :cut] = a_genome.w3[j, :cut]
            new_genome.w3[j, cut:] = b_genome.w3[j, cut:]

            cut = random.randint(0, new_genome.w4.shape[1])
            j = random.randint(0, len(new_genome.w4)-1)
            new_genome.w4[j, :cut] = a_genome.w4[j, :cut]
            new_genome.w4[j, cut:] = b_genome.w4[j, cut:]
            
            cut = random.randint(0, new_genome.w5.shape[1])
            j = random.randint(0, len(new_genome.w5)-1)
            new_genome.w5[j, :cut] = a_genome.w5[j, :cut]
            new_genome.w5[j, cut:] = b_genome.w5[j, cut:]

            best_genomes.append(new_genome)
        
        genomes = []
        for i in range(int(N_POPULATION / (N_BEST * 10))) :
            for bg in best_genomes:
                new_genome = deepcopy(bg)

                mean = 20
                stddev = 10

                if random.uniform(0, 1) < PROB_MUTATION:
                    new_genome.w1 += new_genome.w1 * np.random.normal(mean, stddev, size=(2, 10)) / 100 * np.random.randint(-1, 2, (2, 10))
                if random.uniform(0, 1) < PROB_MUTATION:
                    new_genome.w2 += new_genome.w2 * np.random.normal(mean, stddev, size=(10, 10)) / 100 * np.random.randint(-1, 2, (10, 10))
                if random.uniform(0, 1) < PROB_MUTATION:
                    new_genome.w3 += new_genome.w3 * np.random.normal(mean, stddev, size=(10, 10)) / 100 * np.random.randint(-1, 2, (10, 10))
                if random.uniform(0, 1) < PROB_MUTATION:
                    new_genome.w4 += new_genome.w4 * np.random.normal(mean, stddev, size=(10, 10)) / 100 * np.random.randint(-1, 2, (10, 10))
                if random.uniform(0, 1) < PROB_MUTATION:
                    new_genome.w5 += new_genome.w5 * np.random.normal(mean, stddev, size=(10, 3)) / 100 * np.random.randint(-1, 2, (10, 3))

                genomes.append(new_genome)

        n_generated += 1

        for i in range(N_POPULATION) :
            jumper_list[i].survive = True
        
        

    # 4-4. 그리기
    screen.fill(black)

    for jumper in jumper_list :
        if jumper.survive == True :
            jumper.show()
    
    for wall in wall_list :
        if surviver_numbers > 0:
            wall.show()

    font = pygame.font.Font("C:/Windows/Fonts/AGENCYR.TTF", 20)
    text = font.render("scored : {}  /  surviver : {}  /  Generated : {}".format(score, surviver_numbers, n_generated), True, (255, 255, 0))
    screen.blit(text, (10, 5))

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()