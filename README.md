# Faces-Detection-with-AWS-Rekognition
## Moglan Mihai, Machine Learning Engineer
------
Amazon Rekognition Image provides the DetectFaces operation that looks for key facial features such as eyes, nose, and mouth to detect faces in an input image. Amazon Rekognition Image detects the 100 largest faces in an image.

## To detect faces in your image
__1. If you haven't already:__

  * a. Create or update an IAM user with AmazonRekognitionFullAccess and AmazonS3ReadOnlyAccess permissions. For more information, see https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-dg.pdf#page=20&zoom=100,96,202.
  * b. Install and configure the AWS CLI and the AWS SDKs. For more information, see https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-dg.pdf#page=21&zoom=100,96,105.

__2. After you created IAM user and downloaded CSV file with the keys of user, add aws_access_key_id and aws_secret_access_key to Environment variables (on Windows):__
![alt text](https://github.com/yourbeach/Faces-Detection-with-AWS-Rekognition-/blob/main/images/environment%20Variables.png?raw=true)


