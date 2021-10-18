## Segmentation with Inter-means Algorithm

## Dependencies
import cv2 as cv
import sys

## Load Image

def load_image(image_name):
  image_file_path = "./Original Images/" + image_name
  image = cv.imread(image_file_path)
  if image is None:
      sys.exit("Could not read the image.")
  return image

## Convert to Gray Scale

def convert_to_gray_scale(rgb_image):
  r, g, b = rgb_image[:,:,0], rgb_image[:,:,1], rgb_image[:,:,2]
  gray_image = 0.2989 * r + 0.5870 * g + 0.1140 * b
  return gray_image

## Get Mean Value

def get_average_intensity(image_array):
  sum = 0
  count = 0

  for pixel in image_array:
      sum += pixel
      count += 1

  return sum/count

## Partition By Threshold

def partition_by_threshold(image_array, init_threshold):
  part_1 = []
  part_2 = []

  for pixel in image_array:
      if (pixel <= init_threshold):
        part_1.append(pixel)
      else:
        part_2.append(pixel)

  return part_1, part_2

## Apply Inter-mean Algorithm

def apply_inter_mean(image_name):
  image = load_image(image_name)
  # print("Original Image : ")
  # cv2_imshow(image)

  gray_scaled_image = convert_to_gray_scale(image)
  # print("\nGray Scaled Image : ")
  # cv2_imshow(gray_scaled_image)

  image_array = [i for element in gray_scaled_image for i in element]  # flattern image to array

  init_threshold = get_average_intensity(image_array)
  print("\nInitial Threshold : ", init_threshold)

  count = 1
  threshold_array = [init_threshold]

  while (True):

    part_1, part_2 = partition_by_threshold(image_array, threshold_array[-1])
    # print(len(part_1), len(part_2))

    part_1_avg = get_average_intensity(part_1)
    part_2_avg = get_average_intensity(part_2)
    # print(part_1_avg, part_2_avg)

    new_threshold = 1/2 * (part_1_avg + part_2_avg)
    print("New Threshold After Iteration ", count, " : ", new_threshold)
    
    if (new_threshold == threshold_array[-1]):
      print("Converged!")
      print("Final Treshold : ", new_threshold)
      break

    elif (new_threshold in threshold_array[:-1]):
      print("Bouncing...")
      break

    threshold_array.append(new_threshold)

    count += 1

  return gray_scaled_image, new_threshold

## Segmentation

def segmentate_image(image, threshold):
  final_image = image.copy()
  rows_count = len(image)
  columns_count = len(image[0])
  for i in range(rows_count):
    for j in range(columns_count):
      if (image[i,j] <= threshold):
        final_image[i,j] = 0
      else:
        final_image[i,j] = 255
  return final_image

## Get Segmented Image

image_name = "yellow_cabs.JPEG"
gray_image, threshold = apply_inter_mean(image_name)
new_image = segmentate_image(gray_image, threshold)
# print("\nFinal Segmented Image : ")
# cv2_imshow(new_image)
cv.imwrite("./Segmented Images/Segmented_" + image_name, new_image)