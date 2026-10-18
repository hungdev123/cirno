import pygame, cv2, os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init() 

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Very scary jumpscare")
font = pygame.font.SysFont(None, 100)
counter = 10
text_content = "Jumpscare in: " + str(counter)

COUNTDOWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(COUNTDOWN_EVENT, 1000)

VIDEO_PATH = resource_path("cirno.mp4")
MUSIC_PATH = resource_path("music.mp3")

video_capture = None
state = "COUNTDOWN"

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == COUNTDOWN_EVENT:
            if counter > 0:
                counter -= 1
                text_content = "Jumpscare in: " + str(counter)
            else:
                pygame.time.set_timer(COUNTDOWN_EVENT, 0)
                state = "PLAY_VIDEO"
                video_capture = cv2.VideoCapture(VIDEO_PATH)

                pygame.mixer.music.load(MUSIC_PATH)
                pygame.mixer.music.play(loops=-1)

    screen.fill((255, 255, 255))

    if state == "COUNTDOWN":
        text_surface = font.render(text_content, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    elif state == "PLAY_VIDEO" and video_capture is not None:
        success, frame = video_capture.read()

        if not success:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = video_capture.read()
            
        
        if success:
            video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            scale = min(SCREEN_WIDTH / video_width, SCREEN_HEIGHT / video_height)
            new_width = int(video_width * scale)
            new_height = int(video_height * scale)
            
            x_offset = (SCREEN_WIDTH - new_width) // 2
            y_offset = (SCREEN_HEIGHT - new_height) // 2

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (new_width, new_height)) # Resize theo kích thước mới
            frame = frame.swapaxes(0, 1)
            video_surface = pygame.surfarray.make_surface(frame)
            
            screen.blit(video_surface, (x_offset, y_offset))
            
            clock.tick(30) 
        else:
            video_capture.release()
            running = False

    pygame.display.flip()
    if state == "COUNTDOWN":
        clock.tick(60)

pygame.quit()