import boto3
import json
import cv2
import io

def numpy_to_binary(arr):
	"""
	Transfrom numpy array (image) to blob

	ArgumentsL
	arr -- input data - numpy array

	Returns:
	output -- transformed numpy array to blob
	"""
    
    is_success, buffer = cv2.imencode(".jpg", arr)
    io_buf = io.BytesIO(buffer)
    output = io_buf.read()
    return output


def detect_faces(image):
	"""
	Calls AWS Rekognition face detection on image. 
	Detect bounding box, landmarks, emotions, beard, status of eyes,
	 						and some more features.

	Arguments:
	image -- numpy image from the camera or local folder

	Returns:
	response -- json with coordinates of faces and all features extracted 
	"""

	client = boto3.client('rekognition', region_name = 'eu-central-1')

	response = client.detect_faces(
		Image = {'Bytes': numpy_to_binary(image)},
		Attributes = ['ALL'])


	#for faceDetail in response['FaceDetails']:
	#	print('Here are the other attributes: ')
	#	print(json.dumps(faceDetail, indent = 4, sort_keys = True))

	return response

def draw_bounding_box(image, box):
	"""
	Draw rectangle bounding box of the face on the image

	Arguments:
	image -- numpy image from the camera or local folder
	box -- dictionary with coordinates for bounding box

	Returns:
	image -- initial image with green bounding box on the face 
	"""

	left = int(image.shape[1] * box['Left'])
	top = int(image.shape[0] * box['Top'])
	right = int((image.shape[1] * box['Width']) + left)
	bottom = int((image.shape[0] * box['Height']) + top)

	#print(left, top, right, bottom)
	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

	return image

def draw_landmarks(image, landmarks):
	"""
	Draw face landmarks on face on image

	Arguments:
	image -- numpy image from the camera or local folder
	landmarks -- dictionaty with coordinates for landmarks on face

	Returns:
	image -- initial image with red dots for every landmark
	"""

	for landmark in landmarks:
		x = int(image.shape[1] * landmark['X'])
		y = int(image.shape[0] * landmark['Y'])
		cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

	return image 

def write_age(image, agerange, box):
	"""
	Write the age range of the face in the bounding box

	ArgumentsL
	image -- numpy image from the camera or local folder
	agerange -- dictionary with age range
	box -- dictionary with coordinates for bounding box

	Returns:
	image -- image with blue text ilustrating the age range. 
				The age range is written above the bounding box
	"""

	pos = (int(image.shape[1] * box['Left']), int(image.shape[0] * box['Top']))
	
	cv2.putText(image, str(agerange['Low']) + '-' + str(agerange['High']), pos,
		cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

	return image

def main():
	
	cam = cv2.VideoCapture(0)

	while True:

		ret, frame = cam.read()		

		faces = detect_faces(frame)
		#print("Faces detected: " + str(len(faces['FaceDetails'])))

		for faceDetail in faces['FaceDetails']:
			frame = draw_bounding_box(frame, faceDetail['BoundingBox'])
			frame = draw_landmarks(frame, faceDetail['Landmarks'])
			frame = write_age(frame, faceDetail['AgeRange'], faceDetail['BoundingBox'])

		cv2.imshow('output', frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	cam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()