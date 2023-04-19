import csv
import cv2
import os

def draw_bounding_boxes(image, bounding_boxes):
    for box in bounding_boxes:
        class_label, xmin, ymin, xmax, ymax = box
        if class_label == "Solar Panels":
            color = (0, 255, 0)
        elif class_label == "Body":
            color = (0, 0, 255)
        elif class_label == "Large Antenna":
            color = (255, 0, 0)
        elif class_label == "Small Antenna":
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)

    return image

def main():
    images = {}
    csv_path = "annotations_test.csv"
    images_folder = "Test"

    with open(csv_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            filename, class_label, xmin, ymin, xmax, ymax = row
            xmin, ymin, xmax, ymax = map(int, (xmin, ymin, xmax, ymax))

            if filename not in images:
                images[filename] = []

            images[filename].append((class_label, xmin, ymin, xmax, ymax))

    for image_name, bounding_boxes in images.items():
        image = cv2.imread(os.path.join(images_folder, image_name))
        image_with_boxes = draw_bounding_boxes(image, bounding_boxes)
        cv2.imwrite(os.path.join(images_folder, f'bbox_{image_name}'), image_with_boxes)

if __name__ == "__main__":
    main()
