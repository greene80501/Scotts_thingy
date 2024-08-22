import pygame
import pandas as pd
from datetime import datetime
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128,128,128)
BUTTON_COLOR = (0, 128, 255)
FONT_COLOR = (255, 255, 255)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 70  # Increased height for thicker buttons
BUTTON_MARGIN = 20
FONT_SIZE = 24
INPUT_BOX_WIDTH = 300
INPUT_BOX_HEIGHT = 50
font = pygame.font.SysFont("Arial", 36)
# Setup the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Student Pass System")

# Load the CSV into a DataFrame
df = pd.read_csv("Student_list.csv")
student_gone = {}

def draw_button(text, x, y):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, FONT_COLOR)
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(text_surface, (x + (BUTTON_WIDTH - text_surface.get_width()) // 2, y + (BUTTON_HEIGHT - text_surface.get_height()) // 2))
    return button_rect

def draw_input_box(x, y, text):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, FONT_COLOR)
    input_box_rect = pygame.Rect(x, y, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, input_box_rect)
    pygame.draw.rect(screen, BLACK, input_box_rect, 2)
    screen.blit(text_surface, (x + 10, y + (INPUT_BOX_HEIGHT - text_surface.get_height()) // 2))
    return input_box_rect

def idToBarcodeConverter(idNumber):
    idNumber = int(idNumber)
    output = bin(idNumber)[2:]
    return output

def print_pass(student_id, student_name):
    now = datetime.now()
    hours = now.hour
    minutes = now.minute
    if hours > 12:
        hours -= 12
    return f"Pass for: Mr. Scoπ, Room: 219\nStudent Name: {student_name}\nTime Printed: {hours}:{minutes:02d}"

def draw_home_button():
    return draw_button("Home", 25, 25)

def save_to_spreadsheet():
    global df
    df.to_csv("Student_list.csv", index=False)

def type_menu():
    running = True
    while running:
        screen.fill(BLACK)

        button1 = draw_button("Get Pass", WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, WINDOW_HEIGHT // 2 - BUTTON_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN)
        button2 = draw_button("Return to class", WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, WINDOW_HEIGHT // 2 - BUTTON_HEIGHT // 2)
        home_button = draw_home_button()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_spreadsheet()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button1.collidepoint(pos):
                    lev_class()
                elif button2.collidepoint(pos):
                    return_class()
                elif home_button.collidepoint(pos):
                    main()

def lev_class():
    global student_gone
    input_box = pygame.Rect(WINDOW_WIDTH // 2 - INPUT_BOX_WIDTH // 2, WINDOW_HEIGHT // 2 - INPUT_BOX_HEIGHT // 2, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    error_message = ""  # Variable to store error messages
    font = pygame.font.Font(None, FONT_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_spreadsheet()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if home_button.collidepoint(pos):
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(text) != 6:
                            error_message = "Invalid PIN length! Must be 6 digits."
                        elif text not in df['ID'].astype(str).values:
                            error_message = "PIN not found in the list!"
                        elif int(text) in student_gone:
                            error_message = "This student is currently out."
                        else:
                            running = False  # Exit the loop if the PIN is valid
                            student_id = int(text)
                            student_info = df[df['ID'] == student_id]
                            student_name = f"{student_info[' First Name'].values[0]} {student_info[' Last Name'].values[0]}"
                            start_time = datetime.now()
                            barcode = idToBarcodeConverter(student_id)
                            print(print_pass(student_id, student_name))
                            
                            # Update the student_gone dictionary
                            student_gone[student_id] = {
                                'name': student_name,
                                'start_time': start_time
                            }
                            print(f"Student left the class at: {start_time.hour}:{start_time.minute}")
                            print(student_gone)
                            draw_pass(student_id, student_name, barcode)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        # Display the error message
        if error_message:
            error_surface = font.render(error_message, True, pygame.Color('red'))
            screen.blit(error_surface, (input_box.x, input_box.y + INPUT_BOX_HEIGHT + 10))
        home_button = draw_home_button()

        pygame.display.flip()

def return_class():
    global student_gone
    input_box = pygame.Rect(WINDOW_WIDTH // 2 - INPUT_BOX_WIDTH // 2, WINDOW_HEIGHT // 2 - INPUT_BOX_HEIGHT // 2, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    error_message = ""  # Variable to store error messages
    font = pygame.font.Font(None, FONT_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_spreadsheet()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if home_button.collidepoint(pos):
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        student_id = int(text)
                        if len(text) != 6:
                            error_message = "Invalid PIN length! Must be 6 digits."
                        elif text not in df['ID'].astype(str).values:
                            error_message = "PIN not found in the list!"
                        elif student_id not in student_gone:
                            error_message = "Student is not currently out."
                        else:
                            running = False  # Exit the loop if the PIN is valid
                            end_time = datetime.now()
                            start_time = student_gone[student_id]['start_time']
                            time_gone = end_time - start_time

                            total_minutes_out = time_gone.total_seconds() / 60
                            existing_minutes_out = df.loc[df['ID'] == student_id, ' total minutes out'].values[0]
                            new_total_minutes_out = existing_minutes_out + total_minutes_out
                            df.loc[df['ID'] == student_id, ' total minutes out'] = new_total_minutes_out
                            save_to_spreadsheet()
                            print(f"Time gone: {new_total_minutes_out:.2f} minutes")

                            student_gone.pop(student_id)
                            main()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        # Display the error message
        if error_message:
            error_surface = font.render(error_message, True, pygame.Color('red'))
            screen.blit(error_surface, (input_box.x, input_box.y + INPUT_BOX_HEIGHT + 10))
        home_button = draw_home_button()

        pygame.display.flip()




def main():
    running = True
    while running:
        screen.fill(BLACK)

        button1 = draw_button("Use Pin", WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, WINDOW_HEIGHT // 2 - BUTTON_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN)
        button2 = draw_button("Use Bar Code", WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, WINDOW_HEIGHT // 2 - BUTTON_HEIGHT // 2)
        button3 = draw_button("Exit", WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, WINDOW_HEIGHT // 2 - BUTTON_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_spreadsheet()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button1.collidepoint(pos):
                    type_menu()
                elif button2.collidepoint(pos):
                    scan_code()
                elif button3.collidepoint(pos):
                    save_to_spreadsheet()
                    pygame.quit()
                    sys.exit()

screen_x_center = WINDOW_WIDTH / 2
screen_y_center = WINDOW_HEIGHT/ 2
waiting = True
def scan_code():
    global waiting  # Ensure that you are modifying the global 'waiting' variable
    screen.fill(BLACK)

    font = pygame.font.SysFont("Arial", 36)
    text_1 = font.render("Scaning.", True, WHITE)
    text_2 = font.render("Scaning..", True, WHITE)
    text_3 = font.render("Scaning...", True, WHITE)
    home_button = draw_home_button()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_spreadsheet()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if home_button.collidepoint(pos):
                    main()

        # Clear the screen each frame
        screen.fill(BLACK)

        if waiting:
            # Display the text with dots incrementally
            home_button = draw_home_button()
            screen.blit(text_1, (screen_x_center - text_1.get_width() // 2, screen_y_center - text_1.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(250)  # Wait 500 ms
            
            screen.fill(BLACK)
            home_button = draw_home_button()
            screen.blit(text_2, (screen_x_center - text_2.get_width() // 2, screen_y_center - text_2.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(250)  # Wait 500 ms
            
            screen.fill(BLACK)
            home_button = draw_home_button()
            screen.blit(text_3, (screen_x_center - text_3.get_width() // 2, screen_y_center - text_3.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(250)  # Wait 500 ms
            
        else:
            # If waiting is False, exit the loop or perform other actions
            break
def draw_code(idNumber):
    
    barcode = idToBarcodeConverter(idNumber)
    x = WINDOW_WIDTH // 2 - 125
    y = WINDOW_HEIGHT // 2
    for bit in barcode:
        pygame.draw.line(screen, BLACK if bit == '1' else WHITE, (x, y), (x, y + 100), 1)
        x += 5
runing = True
def draw_pass(student_id, student_name, barcode):
    screen.fill(BLACK)
    
    pass_info = print_pass(student_id, student_name)
    print(student_id, student_name)
    lines = pass_info.split('\n')
    pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH / 4 , WINDOW_HEIGHT/ 8 ,WINDOW_WIDTH/ 2.3 ,WINDOW_HEIGHT/1.25))
    y = 100
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (300, y))
        y += 50
    
    while runing == True:
        draw_code(student_id)
        button1 = draw_button("Home", 25, 25)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_spreadsheet()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button1.collidepoint(pos):
                    main()

if __name__ == "__main__":
    main()