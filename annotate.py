import cv2
import os
import csv

def on_mouse(event, x, y, flags, params):
    global drawing, bbox, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        bbox = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img_copy = img.copy()
        draw_accepted_boxes(img_copy, accepted_boxes)
        draw_key_commands(img_copy)
        cv2.rectangle(img_copy, bbox[0], (x, y), (0, 255, 0), 2)
        cv2.imshow('image', img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bbox.append((x, y))
        cv2.rectangle(img_copy, bbox[0], (x, y), (0, 255, 0), 2)
        cv2.imshow('image', img_copy)

def draw_accepted_boxes(img, boxes):
    for box in boxes:
        cv2.rectangle(img, box[0], box[1], (0, 255, 0), 2)

def draw_key_commands(img):
    key_commands = [
        ('A: Accept the box', (255, 255, 255)),
        ('R: Redraw', (255, 255, 255)),
        ('N: Next image', (255, 255, 255)),
        ('Q: Quit', (255, 255, 255))
    ]

    y_offset = 20
    for command, color in key_commands:
        cv2.putText(img, command, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        y_offset += 30

def prompt_options(options):
    print("\nOptions:")
    for idx, option in enumerate(options):
        print(f"{idx + 1}. {option}")
    choice = int(input("Enter your choice: ")) - 1
    return options[choice]

image_folder = input("Enter the path to the image folder: ")
classes = input("Enter the class labels separated by commas: ").split(',')

drawing = False
bbox = []

results = []

for img_file in os.listdir(image_folder):
    if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        img_path = os.path.join(image_folder, img_file)
        img = cv2.imread(img_path)
        img_copy = img.copy()

        accepted_boxes = []

        while True:
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', on_mouse)
            draw_accepted_boxes(img_copy, accepted_boxes)
            draw_key_commands(img_copy)
            cv2.imshow('image', img_copy)
            key = cv2.waitKey(0)

            if key == ord('r'):  # Redraw
                bbox = []
                img_copy = img.copy()
            elif key == ord('n'):  # Next image
                break
            elif key == ord('a'):  # Accept the box
                if len(bbox) == 2:
                    label = prompt_options(classes)
                    xmin, ymin = bbox[0]
                    xmax, ymax = bbox[1]
                    results.append([img_file, label, xmin, ymin, xmax, ymax])
                    accepted_boxes.append(bbox)
                    bbox = []
                    img_copy = img.copy()
                else:
                    print("Please draw a bounding box first.")
            elif key == ord('q'):  # Quit
                cv2.destroyAllWindows()
                exit()

        cv2.destroyAllWindows()

with open('annotations.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    for result in results:
        writer.writerow(result)

print("Results saved to annotations.csv.")
