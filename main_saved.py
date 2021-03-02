from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colordetector import ColorDetector

import imutils as imutils
import keyboard
import mouse
import numpy as np
from PIL import ImageGrab
import cv2
import playsound
import time

animals = []


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def process_img(image):
    final = apply_brightness_contrast(image, 12, 50)

    sd = ShapeDetector()
    cd = ColorDetector()
    # convert to gray
    # processed_img = imutils.resize(image, width=1500)
    # ratio = image.shape[0]/float(processed_img.shape[0])
    processed_img = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.equalizeHist(processed_img)
    # processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

    # cv2.imshow("Image", processed_img)
    # cv2.waitKey(0)

    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1=100, threshold2=200)
    # cv2.imshow("Image", processed_img)
    # cv2.waitKey(0)
    #
    # kernel = np.ones((7, 7), np.uint8)
    # processed_img = cv2.dilate(processed_img, kernel, iterations=1)
    # processed_img = cv2.erode(processed_img, kernel, iterations=1)
    #

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(processed_img.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    game_board = []
    x_coordinates = []
    y_coordinates = []
    lowestY = 999999
    # for c in cnts:
    #     # compute the center of the contour
    #     M = cv2.moments(c)
    #     if M["m00"] == 0:
    #         M["m00"] = 1
    #     cX = int(M["m10"] / M["m00"])
    #     cY = int(M["m01"] / M["m00"])
    #
    #     shape = sd.detect(c)
    #     if shape == "hexagon":
    #         print(str(cX) + ", " + str(cY))
    #         # draw the contour and center of the shape on the image
    #         color = cd.determine_color(image, c)
    #         cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    #         cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    #         cv2.putText(image, color, (cX - 20, cY - 20),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #         if cY < lowestY:
    #             lowestY = cY
    #             game_board.append([color])
    #             x_coordinates.append([cX])
    #             y_coordinates.append(cY)
    #
    #         else:
    #             for i in range(0, len(y_coordinates)):
    #                 if cY == y_coordinates[i]:
    #                     x_coordinates[i].append(cX)
    #                     game_board[i].append(color)
    # for i in range(0, len(x_coordinates)):
    #     swapped = True
    #     while swapped:
    #         swapped = False
    #         for j in range(len(x_coordinates[i]) - 1):
    #             if x_coordinates[i][j] > x_coordinates[i][j + 1]:
    #                 # Swap the elements
    #                 x_coordinates[i][j], x_coordinates[i][j + 1] = x_coordinates[i][j + 1], x_coordinates[i][j]
    #                 game_board[i][j], game_board[i][j + 1] = game_board[i][j + 1], game_board[i][j]
    #                 # Set the flag to True so we'll loop again
    #                 swapped = True
    # game_board = game_board[::-1]
    # x_coordinates = x_coordinates[::-1]
    # y_coordinates = y_coordinates[::-1]

    # solve_game(game_board, x_coordinates, y_coordinates)
    # show the image
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)

    cv2.imwrite("./Gray_Image.jpg", image)

    return image, cnts


def change_state(color):
    if color == "black":
        color = "white"
    else:
        color = "black"
    return color


def move(game_board, x, y):
    # print("X: " + str(x) + ", Y: " + str(y))
    # change self
    game_board[x][y] = change_state(game_board[x][y])

    # left and right
    if y > 0:  # if column greater than 0
        game_board[x][y - 1] = change_state(game_board[x][y - 1])  # color to the left is changed
    if y < len(game_board[x]) - 1:  # if column less than row length
        game_board[x][y + 1] = change_state(game_board[x][y + 1])  # color to the right is changed

    # top and bottom
    # if not last row
    if x < len(game_board) - 1:
        # if row below is bigger
        if len(game_board[x]) < len(game_board[x + 1]):
            game_board[x + 1][y] = change_state(game_board[x + 1][y])  # change left state
            game_board[x + 1][y + 1] = change_state(game_board[x + 1][y + 1])  # change right state

        # row below is smaller
        else:
            if y != len(game_board[x]) - 1:  # if not last col
                game_board[x + 1][y] = change_state(game_board[x + 1][y])  # change right state
            if y != 0:  # if not first col
                game_board[x + 1][y - 1] = change_state(game_board[x + 1][y - 1])  # change left state

    # if not first row
    if x != 0:
        # if row above is bigger
        # print(game_board)
        # print(len(game_board[x]))
        # print(len(game_board[x - 1]))
        if len(game_board[x]) < len(game_board[x - 1]):
            game_board[x - 1][y] = change_state(game_board[x - 1][y])  # change left state
            game_board[x - 1][y + 1] = change_state(game_board[x - 1][y + 1])  # change right state

        # row above is smaller
        else:
            # print("THIS " + str(y) + "LENGTH " + str(len(game_board[x]) - 1))
            if y != len(game_board[x]) - 1:  # if not last col
                game_board[x - 1][y] = change_state(game_board[x - 1][y])  # change right state
            if y != 0:  # if not first col
                game_board[x - 1][y - 1] = change_state(game_board[x - 1][y - 1])  # change left state
    # print(game_board)
    return game_board


# top and bottom


def start_game(image, cnts):
    game_board = []
    x_coordinates = []
    y_coordinates = []
    lowestY = 999999
    sd = ShapeDetector()
    cd = ColorDetector()

    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] == 0:
            M["m00"] = 1
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        shape = sd.detect(c)
        if shape == "hexagon":
            # print(str(cX) + ", " + str(cY))
            # draw the contour and center of the shape on the image
            color = cd.determine_color(image, c)
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, color, (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            if cY < lowestY:
                lowestY = cY
                game_board.append([color])
                x_coordinates.append([cX])
                y_coordinates.append(cY)

            else:
                for i in range(0, len(y_coordinates)):
                    if cY == y_coordinates[i]:
                        x_coordinates[i].append(cX)
                        game_board[i].append(color)
    if len(game_board) == 0:
        return
    for i in range(0, len(x_coordinates)):
        swapped = True
        while swapped:
            swapped = False
            for j in range(len(x_coordinates[i]) - 1):
                if x_coordinates[i][j] > x_coordinates[i][j + 1]:
                    # Swap the elements
                    x_coordinates[i][j], x_coordinates[i][j + 1] = x_coordinates[i][j + 1], x_coordinates[i][j]
                    game_board[i][j], game_board[i][j + 1] = game_board[i][j + 1], game_board[i][j]
                    # Set the flag to True so we'll loop again
                    swapped = True
    game_board = game_board[::-1]
    x_coordinates = x_coordinates[::-1]
    y_coordinates = y_coordinates[::-1]
    solve_game(game_board, x_coordinates, y_coordinates)


# TODO: Create a more efficient algorithm
def solving_down(game_board, row, color):
    instructions = []
    i = 0
    # if (row == 0) or (len(game_board[row]) < len(game_board[row + 1])):  # if row below is smaller
    if row < 3:
        # print(row)
        # print(game_board)
        while i < len(game_board[row]):
            tile = game_board[row][i]
            if tile == color:
                if i < len(game_board[row]) - 1 and game_board[row][i + 1] == color:
                    instructions.append(i + 1)
                    i += 2
                else:
                    x = i
                    if x + 1 <= len(game_board[row]) / 2:
                        while x > -1:
                            instructions.append(x)
                            x -= 1
                    else:

                        while x < len(game_board[row]):
                            x += 1
                            instructions.append(x)

                    i += 1
            else:
                i += 1
        return row + 1, instructions
    else:
        counter = 0
        for tile in game_board[row]:
            if tile == color:
                counter += 1
        if counter % 2 == 0:
            while i < len(game_board[row]):
                tile = game_board[row][i]
                if tile == color:
                    if i < len(game_board[row]) - 1 and game_board[row][i + 1] == color:
                        instructions.append(i)
                        i += 2
                    else:
                        x = i - 1
                        while x > -1:
                            instructions.append(x)
                            x -= 1
                        i += 1
                else:
                    i += 1
            return row + 1, instructions
        else:
            if row == 3:
                x = len(game_board[3]) - 1
                while x > - 1:
                    instructions.append(x)
                    x -= 1
                return row, instructions

            if row == 4:
                x = len(game_board[1]) - 1
                while x > -1:
                    instructions.append(x)
                    x -= 1
                return row - 3, instructions

            if row == 5:
                x = len(game_board[2]) - 1
                while x > -1:
                    instructions.append(x)
                    x -= 1
                return row - 3, instructions
    # print(instructions)
    return instructions


# executes instructions one row at a time
def execute_instructions(instructions, row, x_coords, y_coords, game_board):
    y = y_coords[row]
    for instruction in instructions:
        x = x_coords[row][instruction]
        mouse.move(x, y, absolute=True, duration=0.25)
        game_board = move(game_board, row, instruction)
        mouse.click()
    return game_board


def test_instructions(instructions, row, game_board):
    for instruction in instructions:
        game_board = move(game_board=game_board, x=row, y=instruction)
    return game_board


def solve_game(game_board, x_coords, y_coords):
    # test for black
    # temp_game_board = game_board
    # row = 0
    # maxiter = 0
    # black_counter = 0
    # black_all_instructions = []
    # while row < 6:
    #     row, instructions = solving_down(game_board=temp_game_board, row=row, color="black")
    #     temp_game_board = test_instructions(instructions=instructions, row=row, game_board=temp_game_board)
    #     black_counter += len(instructions)
    #     if maxiter == 30:
    #         break
    #     else:
    #         maxiter += 1
    #     black_all_instructions.append((row, instructions))
    #
    # # test for white
    # temp_game_board = game_board
    # row = 0
    # maxiter = 0
    # white_counter = 0
    # white_all_instructions = []
    # while row < 6:
    #     row, instructions = solving_down(game_board=temp_game_board, row=row, color="white")
    #     temp_game_board = test_instructions(instructions=instructions, row=row, game_board=temp_game_board)
    #     white_counter += len(instructions)
    #     if maxiter == 30:
    #         break
    #     else:
    #         maxiter += 1
    #     white_all_instructions.append((row, instructions))
    #
    # print("White: " + str(white_counter) + ", Black: " + str(black_counter))

    # test for black
    row = 0
    maxiter = 0
    while row < 6:
        row, instructions = solving_down(game_board=game_board, row=row, color="black")
        game_board = execute_instructions(instructions, row, x_coords, y_coords, game_board)
        # print(row)
        # print(instructions)
        if maxiter == 30:
            break
        else:
            maxiter += 1

    # if white_counter < black_counter:
    #     for row, instructions in white_all_instructions:
    #         execute_instructions(instructions, row, x_coords, y_coords)
    # else:
    #     for row, instructions in black_all_instructions:
    #         execute_instructions(instructions, row, x_coords, y_coords)


def press_next(image, cnts):
    sd = ShapeDetector()
    cd = ColorDetector()

    pressed = False

    for c in cnts:
        M = cv2.moments(c)
        if M["m00"] == 0:
            M["m00"] = 1
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        shape = sd.detect(c)
        if shape == "rectangle":
            print(str(cX) + ", " + str(cY))
            mouse.move(cX, cY, absolute=True, duration=0.05)
            mouse.click()
            pressed = True


def screen_grab():
    screengrab = ImageGrab.grab()
    screengrab_raw = np.array(screengrab, dtype='uint8') \
        .reshape((screengrab.size[1], screengrab.size[0], 3))

    image, cnts = process_img(screengrab_raw)
    return image, cnts


limit = 0
keyboard.wait('`')
while True:
    # try:  # used try so that if user pressed other than the given key error will not be shown
    try:
        image, cnts = screen_grab()
        start_game(image, cnts)
    except:
        print()
        # playsound.playsound('Card Shuffle sound effect.mp3')

    time.sleep(0.1)
    try:
        image, cnts = screen_grab()
        start_game(image, cnts)
    except:
        print()
        # playsound.playsound('Card Shuffle sound effect.mp3')
    time.sleep(0.1)
    try:
        image, cnts = screen_grab()
        start_game(image, cnts)
    except:
        print()
        # playsound.playsound('Card Shuffle sound effect.mp3')
    time.sleep(0.1)
    try:
        image, cnts = screen_grab()
        start_game(image, cnts)
    except:
        # playsound.playsound('Card Shuffle sound effect.mp3')
        time.sleep(0.3)
    time.sleep(0.1)
    try:
        image, cnts = screen_grab()
        start_game(image, cnts)
    except:
        playsound.playsound('Wrong Buzzer Sound effect.mp3')
        print("Hexagon")
        keyboard.wait('`')
    time.sleep(0.5)

    press_flag = False
    try:
        image, cnts = screen_grab()
        press_next(image, cnts)
        press_flag = True
    except:
        playsound.playsound('Card Shuffle sound effect.mp3')
        time.sleep(0.25)

    if not press_flag:
        time.sleep(0.25)
        try:
            image, cnts = screen_grab()
            press_next(image, cnts)
            press_flag = True
        except:
            print("PressNext")
    if not press_flag:
        time.sleep(0.25)
        try:
            image, cnts = screen_grab()
            press_next(image, cnts)
            press_flag = True
        except:
            playsound.playsound('Wrong Buzzer Sound effect.mp3')
            print("PressNext")
            keyboard.wait('`')


    time.sleep(0.5)

    if limit > 49:
        limit = 0
        playsound.playsound('Sparkle-sound-effect.mp3')
        keyboard.wait('`')
    else:
        limit += 1
    # except:
    #     print("ERROR")
    #     # break  # if user pressed a key other than the given key the loop will break
