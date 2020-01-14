import pygame
import socket
from _thread import *

pygame.init()
screen = pygame.display.set_mode([400, 400])
pygame.display.set_caption('Rotating image example')
clock = pygame.time.Clock()

img = pygame.image.load('images/wheel.png').convert()

# If multiple listeners, uncomment lines below

# def threaded(c):
#     while True:
#         try:
#             data = c.recv(1024)
#             print(c.getpeername(), ': ', str(data)[2:-1])
#             # print(type(data))
#             angle = int(str(data)[2:-1])
#             rotator(angle)
#             #print(angle)
#         except Exception as e:
#             print("Exception at server (Rotator): ", e)
#             c.close()


def rotator(degree):
    img_rect = img.get_rect(center=screen.get_rect().center)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # rotate image
    rot_img = pygame.transform.rotate(img, degree)
    img_rect = rot_img.get_rect(center=img_rect.center)

    # copy image to screen
    screen.fill((255, 255, 255))
    screen.blit(rot_img, img_rect)
    pygame.display.flip()

    clock.tick(60)
    degree += 1


### SERVER CODE
host = "127.0.0.1"
port = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("Socket binded to post", port)
s.listen(5)
print("Socket is listening")

# If multiple listeners, add while True:
c, addr = s.accept()
print('Connected to :', addr[0], ':', addr[1])
while True:
    try:
        data = c.recv(1024)
        print(c.getpeername(), ': ', str(data)[2:-1])
        # print(type(data))
        #print(type(int(data.decode())))
        angle = float(data.decode())
        rotator(angle)
        if not data:
            break
        #print(angle)
    except ConnectionResetError:
        print("Closing connection at rotator")
        s.close()
        break
    except ValueError:
        print("here")
        continue
    #start_new_thread(threaded, (c,))


pygame.quit()
