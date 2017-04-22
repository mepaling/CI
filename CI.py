# coding: utf-8
# pylint: skip-file

"""
By 105522056 王建舜
"""
"""
Reference
http://effbot.org/tkinterbook/canvas.htm
http://stackoverflow.com/questions/17985216/draw-circle-in-tkinter-python
http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_oval.html
http://stackoverflow.com/questions/23690993/how-do-we-delete-a-shape-thats-already-been-created-in-tkinter-canvas
http://stackoverflow.com/questions/9776718/how-do-i-stop-tkinter-after-function
http://www.chebucto.ns.ca/Science/AIMET/archive/ddj/fuzzy_logic_in_C/
"""

import Tkinter as tk
from functions import *
from FuzzySystem import *

# base settings
canvas_width = 600
canvas_height = 600
ratio = 9
offset = point(150, 500)
rotate = point(1, -1)
speed = 10

# Open two files
file_4D = open("train4D.txt", 'w')
file_6D = open("train6D.txt", 'w')

# calculate the value after zoomed
def zoom(value, method):
    if method is "x":
        return value*ratio*rotate.x+offset.x
    elif method is "y":
        return value*ratio*rotate.y+offset.y
    else:
        return None

# draw a circle to the canvas
def draw_circle(canvas, x, y, r=1, outline="red", width=3):
    return canvas.create_oval(zoom((x-r), "x"), zoom((y-r), "y"),
                              zoom((x+r), "x"), zoom((y+r), "y"), outline=outline, width=width)

# draw the border (line) to the canvas
def draw_border(canvas, line, fill="black"):
    return canvas.create_line(zoom(line.point1.x, "x"), zoom(line.point1.y, "y"),
                              zoom(line.point2.x, "x"), zoom(line.point2.y, "y"), fill=fill)

# draw the car image on the canvas
def draw_car_image(canvas, car, car_last_point=None):
    car.canvas_car = draw_circle(canvas, car.x, car.y, car.r)
    car_point = point(car.x, car.y)
    if car_last_point is None:
        car.veraxis = line(car.x, car.y, x2=car.x, y2=car.y+car.r*1.5)
        car.horaxis = line(car.x-car.r*1.5, car.y, x2=car.x+car.r*1.5, y2=car.y)
    else: 
        slope = get_slope(car_point, car_last_point)
        try:
            ver_slope = (-1) / slope

            if -270.0 <= car.phi and car.phi <= -100:
                next_point_ver = (point_distance(car_point, slope, car.r*1.5))[1]
            else:
                next_point_ver = (point_distance(car_point, slope, car.r*1.5))[0]
            #print next_point_ver
            if isnan(next_point_ver.y):
                next_point_ver.y = car_point.y + car.r*1.5
            next_point_hor_0 = (point_distance(car_point, ver_slope, car.r*1.5))[0]
            next_point_hor_1 = (point_distance(car_point, ver_slope, car.r*1.5))[1]
            car.veraxis = line(car.x, car.y, x2=next_point_ver.x, y2=next_point_ver.y)
            car.horaxis = line(next_point_hor_0.x, next_point_hor_0.y, x2=next_point_hor_1.x, y2=next_point_hor_1.y)
        except ZeroDivisionError:
            car.veraxis = line(car.x, car.y, x2=car.x, y2=car.y+car.r*1.5)
            car.horaxis = line(car.x-car.r*1.5, car.y, x2=car.x+car.r*1.5, y2=car.y)
    car.canvas_horaxis = draw_border(canvas, car.horaxis, "red")
    car.canvas_veraxis = draw_border(canvas, car.veraxis, "red")


# remove the car image on the canvas
def remove_car_image(canvas, car):
    canvas.delete(car.canvas_car)
    canvas.delete(car.canvas_horaxis)
    canvas.delete(car.canvas_veraxis)
# calculate sensor's value
def calculate_sensor(car):
    min_sf = float('inf')
    min_sl = float('inf')
    min_sr = float('inf')
    car_point = point(car.x, car.y)
    count = len(border_arr)
    # has -3 in set_sensor_val
    for ele in border_arr:
        if count is 1:
            break
        else:
            count -= 1
        # the intersection point of front sensor line and wall 
        point_f_border = point_intersection_between_lines(ele, car.sfl)
        if point_f_border is not None and (between_ab(point_f_border.x, ele.xmin, ele.xmax) and between_ab(point_f_border.y, ele.ymin, ele.ymax)):
            dis_f_border = dis_p1_p2(car_point, point_f_border)
            min_sf = min(min_sf, dis_f_border)

        point_l_border = point_intersection_between_lines(ele, car.sll)
        if point_l_border is not None and (between_ab(point_l_border.x, ele.xmin, ele.xmax) and between_ab(point_l_border.y, ele.ymin, ele.ymax)):
            dis_l_border = dis_p1_p2(car_point, point_l_border)
            min_sl = min(min_sl, dis_l_border)
        
        point_r_border = point_intersection_between_lines(ele, car.srl)
        if point_r_border is not None and (between_ab(point_r_border.x, ele.xmin, ele.xmax) and between_ab(point_r_border.y, ele.ymin, ele.ymax)):
            dis_r_border = dis_p1_p2(car_point, point_r_border)
            min_sr = min(min_sr, dis_r_border)
        #print (min_sf)
        #min_sf = min(min_sf, dis_between_point_line_theta(car_point, ele, car.phi))
        #min_sl = min(min_sl, dis_between_point_line_theta(car_point, ele, car.phi + 45))
        #min_sr = min(min_sr, dis_between_point_line_theta(car_point, ele, car.phi - 45))
    #print car_point
    #print str(min_sf) + " " + str(min_sl) + " " + str(min_sr)
    
    #print str(min_sf) + " " + str(min_sr) + " " + str(min_sl)
    car.set_sensor_val(min_sf, min_sl, min_sr)
    return car

# moving function
def moving():
    car_last_point = point(car.x, car.y)
    # Calculate theta then set car's new position and update sensor's data
    theta = fs.fuzzy_main(car.sf, car.sl, car.sr)
    #theta = 40
    car.set_pos_theta(theta)
    calculate_sensor(car)

    #print car
    print(str(car) + " theta:" + str(theta) + "\n")
    file_4D.write(car.print_car_4D(theta) + "\n")
    file_6D.write(car.print_car_6D(theta) + "\n")
    
    # Delete the car image then redraw it
    remove_car_image(canvas, car)
    draw_circle(canvas, car_last_point.x, car_last_point.y, 0.5, "blue", 1)
    draw_car_image(canvas, car, car_last_point)

    # Check if the car is reach goal
    if not (car.y > goal.y):
        # if not, keep on moving!
        canvas.after(int(1000 / speed), moving)

"""Main"""

# Create Tk window and canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)

# Create border and draw
border_arr = [line(-6, 0, x2=-6, y2=22), line(-6, 22, x2=18, y2=22), line(18, 22, x2=18, y2=50), 
              line(6, 0, x2=6, y2=10), line(6, 10, x2=30, y2=10), line(30, 10, x2=30, y2=50),
              line(18, 50, x2=30, y2=50), line(-10, 0, x2=20, y2=0)]
for ele in border_arr:
    draw_border(canvas, ele)

# Create car and draw
car = car(0, 0, 90, 3)
calculate_sensor(car)
#print car
print(str(car) + " theta:" + str(0) + "\n")
file_4D.write(car.print_car_4D() + "\n")
file_6D.write(car.print_car_6D() + "\n")
draw_car_image(canvas, car)

# Create a FuzzySystem insatnce
fs = FuzzySystem()

# Create goal and draw
goal = point(24, 37)
draw_circle(canvas, goal.x, goal.y)

# Bind moving function
canvas.after(0, moving)


# Create Window!
canvas.pack()
root.wm_title("105522056 王建舜 HW1")
root.mainloop()
