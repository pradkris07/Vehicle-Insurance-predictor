from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from src.configuration.googledrive_connection import googleClient
from io import StringIO, BytesIO
from typing import Union,List
import os,sys
from src.logger import logging
#from mypy_boto3_s3.service_resource import Bucket
from src.exception import MyException
#from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
import pickle


class DriveStorageService:
    """
    A class for interacting with Google Drive storage, providing methods for file management, 
    data uploads, and data retrieval in Google Drive folders.
    """

    def __init__(self):
        """
        Initializes the SimpleStorageService instance with S3 resource and client
        from the S3Client class.
        """
        s3_client = googleClient()
        self.creds = s3_client.creds
        self.service = build("drive", "v3", credentials=self.creds)
        self.file_id = 0
        self.destination_path = "./temp.pkl"

    def s3_key_path_available(self, bucket_name, s3_key) -> bool:
        """
        Checks if a specified S3 key path (file path) is available in the specified bucket.

        Args:
            bucket_name (str): Name of the S3 bucket.
            s3_key (str): Key path of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            #file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            file_objects = self.get_file_object(s3_key, bucket_name)
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Reads the specified S3 object with optional decoding and formatting.

        Args:
            object_name (str): The S3 object name.
            decode (bool): Whether to decode the object content as a string.
            make_readable (bool): Whether to convert content to StringIO for DataFrame usage.

        Returns:
            Union[StringIO, str]: The content of the object, as a StringIO or decoded string.
        """
        # logging.info("Entered the read_object method of SimpleStorageService class")
        try:
            # Read and decode the object content if decode=True
            #func = (
            #    lambda: object_name.get()["Body"].read().decode()
            #    if decode else object_name.get()["Body"].read()
            #)
            func = (lambda: object_name.read().decode() if decode else object_name.read())
            # Convert to StringIO if make_readable=True
            conv_func = lambda: StringIO(func()) if make_readable else func()
            # logging.info("Exited the read_object method of SimpleStorageService class")
            return conv_func()
        except Exception as e:
            raise MyException(e, sys) from e

    def get_bucket(self, bucket_name: str):
        """
        Retrieves the S3 bucket object based on the provided bucket name.

        Args:
            bucket_name (str): The name of the S3 bucket.

        Returns:
            Bucket: S3 bucket object.
        """
        logging.info("Entered the get_bucket method of GoogleStorageService class")
        try:
            page_token = None

            while True:
              # Call the Drive v3 API
              results = (
                  self.service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken = page_token).execute()
              )
              items = results.get("files", [])
              for item in items:
                #print(item)
                if item['name'] == bucket_name:
                    folderid = item['id']
              
              if page_token is None:
                break
        except HttpError as error:
            raise MyException(error, sys) from error
              #print(f"An error occurred: {error}")
        except Exception as e:
            raise MyException(e, sys) from e
  
        return folderid
      

    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        """
        Retrieves the file object(s) from the specified bucket based on the filename.

        Args:
            filename (str): The name of the file to retrieve.
            bucket_name (str): The name of the S3 bucket.

        Returns:
            Union[List[object], object]: The S3 file object or list of file objects.
        """
        logging.info("Entered the get_file_object method of SimpleStorageService class")
        try:
            bucket = self.get_bucket(bucket_name)
            #file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            try:
                page_token = None
                folders = []
                
                while True:
                  # Call the Drive v3 API
                  response = (self.service.files().list(q = "'" + bucket + "' in parents",
                                       spaces="drive",fields="nextPageToken, files(id, name)",pageToken=page_token).execute())
      
                  items = response.get("files", [])
                  for item in items:
                    #print(item)
                    if item['name'] == filename:
                        folders.append(item['name'])
                        self.file_id = item['id']
                  
                  if page_token is None:
                    break
            except HttpError as error:
                raise MyException(error, sys) from error
                #print(f"An error occurred: {error}")
            except Exception as e:
                raise MyException(e, sys) from e
      

            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(folders)
            logging.info("Exited the get_file_object method of SimpleStorageService class")
            return file_objs
        except Exception as e:
            raise MyException(e, sys) from e

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        """
        Loads a serialized model from the specified S3 bucket.

        Args:
            model_name (str): Name of the model file in the bucket.
            bucket_name (str): Name of the S3 bucket.
            model_dir (str): Directory path within the bucket.

        Returns:
            object: The deserialized model object.
        """
        try:
            model_file = model_dir + "/" + model_name if model_dir else model_name
            file_object = self.get_file_object(model_name, bucket_name)
            self.download_file(self.file_id)
            #model_obj = self.read_object(file_object, decode=False)
            logging.info("Going to load the pickle file.")
            with open(self.destination_path,'rb') as f:
                model = pickle.load(f)
            #model = pickle.load(file_object.getvalue())
            #model = pickle.loads(databytes)
            logging.info("Production model loaded from S3 bucket.")
            return model
        except Exception as e:
            raise MyException(e, sys) from e
            
    def download_file(self, real_file_id):
    
        """Downloads a file
               Args: real_file_id: ID of the file to download
               Returns : IO object with location.
        """
        try:
        # create drive api client
            request = self.service.files().get_media(fileId=real_file_id)
            downloaded_file = BytesIO()
            downloader = MediaIoBaseDownload(downloaded_file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

        except HttpError as error:
            raise MyException(error, sys) from error
            downloaded_file = None
        
        with open(self.destination_path, 'wb') as f:
            f.write(downloaded_file.getvalue())
            

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a folder in the specified S3 bucket.

        Args:
            folder_name (str): Name of the folder to create.
            bucket_name (str): Name of the S3 bucket.
        """
        logging.info("Entered the create_folder method of SimpleStorageService class")
        try:
            # Create a folder on Drive, returns the newely created folders ID
            body = {'name': folderName,'mimeType': "application/vnd.google-apps.folder"}
            bucket = self.get_bucket(bucket_name)
            if bucket:
                body['parents'] = [bucket]
            if self.get_bucket(folderName) is None:
                root_folder = service.files().create(body = body).execute() 
            else:
                print("Folder already exists with id " + getFolders())
                root_folder = "Folder already exists"
        except Exception as e:
            raise MyException(e, sys) from e
    
        logging.info("Exited the create_folder method of SimpleStorageService class")

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        """
        Uploads a local file to the specified S3 bucket with an optional file deletion.

        Args:
            from_filename (str): Path of the local file.
            to_filename (str): Target file path in the bucket.
            bucket_name (str): Name of the S3 bucket.
            remove (bool): If True, deletes the local file after upload.
        """
        logging.info("Entered the upload_file method of SimpleStorageService class")
        page_token = None
        namelist = []
        try:
            logging.info(f"Uploading {from_filename} to {to_filename} in {bucket_name}")
            try:
                folder_id = self.get_bucket(bucket_name)
                # create drive api client
                while True:
                    #query = f"name='{to_filename}' in parents"
                    results = (self.service.files().list(q="'" + folder_id + "' in parents", spaces="drive", fields="nextPageToken, files(id, name)",pageToken=page_token).execute())
                    items = results.get('files', [])
                    logging.info(f"Getting file names {items}")
                    idlist = [n['id'] for n in items if n['name'] == to_filename]
                    if idlist:
                        # File found, get its ID and update
                        existing_file_id = idlist[0]
                        # Example: Update content (replace 'your_new_content.txt' with your file path)
                        media = MediaFileUpload(from_filename, mimetype="application/octet-stream", resumable=True)
                        #media_body = {'name': file_name}
                        file = self.service.files().update(fileId=existing_file_id,media_body=media,fields='id, name').execute()
                    else:
                        file_metadata = {"name": to_filename, "parents": [folder_id]}
                        media = MediaFileUpload(from_filename, mimetype="application/octet-stream", resumable=True)
                        # pylint: disable=maybe-no-member
                        file = (self.service.files().create(body=file_metadata, media_body=media, fields="id").execute())
                    if page_token is None:
                        break
                return file.get("id")

            except HttpError as error:
               raise MyException(error, sys) from error
               return None
            #self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            logging.info(f"Uploaded {from_filename} to {to_filename} in {bucket_name}")

            # Delete the local file if remove is True
            if remove:
                os.remove(from_filename)
                logging.info(f"Removed local file {from_filename} after upload")
            logging.info("Exited the upload_file method of SimpleStorageService class")
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        """
        Uploads a DataFrame as a CSV file to the specified S3 bucket.

        Args:
            data_frame (DataFrame): DataFrame to be uploaded.
            local_filename (str): Temporary local filename for the DataFrame.
            bucket_filename (str): Target filename in the bucket.
            bucket_name (str): Name of the S3 bucket.
        """
        logging.info("Entered the upload_df_as_csv method of SimpleStorageService class")
        try:
            # Save DataFrame to CSV locally and then upload it
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
            logging.info("Exited the upload_df_as_csv method of SimpleStorageService class")
        except Exception as e:
            raise MyException(e, sys) from e

    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Converts an S3 object to a DataFrame.

        Args:
            object_ (object): The S3 object.

        Returns:
            DataFrame: DataFrame created from the object content.
        """
        logging.info("Entered the get_df_from_object method of SimpleStorageService class")
        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logging.info("Exited the get_df_from_object method of SimpleStorageService class")
            return df
        except Exception as e:
            raise MyException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Reads a CSV file from the specified S3 bucket and converts it to a DataFrame.

        Args:
            filename (str): The name of the file in the bucket.
            bucket_name (str): The name of the S3 bucket.

        Returns:
            DataFrame: DataFrame created from the CSV file.
        """
        logging.info("Entered the read_csv method of SimpleStorageService class")
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            logging.info("Exited the read_csv method of SimpleStorageService class")
            return df
        except Exception as e:
            raise MyException(e, sys) from e