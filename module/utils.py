from django.conf import settings
from datetime import datetime
from supabase import create_client

# Supabase client initialization
supabase_url = settings.SUPABASE_URL
supabase_key = settings.SUPABASE_KEY
supabase = create_client(supabase_url, supabase_key)

class ImageUploader:

    @staticmethod
    def is_image_file(filename):
        image_extensions = ['image/jpg', 'image/jpeg', 'image/png', 'image/bmp', 'image/gif']
        
        if filename not in image_extensions:
            return {"err_code": 1, "message": "File is not valid"}
        else: 
            return {"err_code": 0, "message": "File is valid"}
        
    @staticmethod
    def upload_image_to_supabase(image, bucket_name):
        try:
            content_type = image.content_type
            file_validation = ImageUploader.is_image_file(content_type)

            if file_validation["err_code"] == 0:
                try:
                    supabase.storage.get_bucket(bucket_name)
                except Exception as e:
                    error = e.args[0]["error"]
                    if "Bucket not found" in error:
                        supabase.storage.create_bucket(bucket_name, options={
                            "public": True, 
                            "allowed_mime_types": ["image/png"],
                            # "file_size_limit": 1024
                        })
    
                current_time_integer = int(datetime.now().timestamp())
                image_name = str(current_time_integer)
                response = supabase.storage.from_(bucket_name).upload(image_name, image.file.read(), file_options={"content-type": "image/png"})
                image_url = supabase.storage.from_(bucket_name).get_public_url(image_name)

                if response.status_code == 200:
                    return {"err_code": 0, "message": "Avatar upload successful", "image_url": image_url, "image_name": image_name}
                else:
                    return {"err_code": 1, "message": "Avatar upload failed"}
            
            else:
                return {"err_code": file_validation["err_code"], "message": file_validation["message"]}
            
        except Exception as e:
            return {"err_code": 2, "message": str(e)}
    
    @staticmethod
    def delete_old_image(bucket_name, image_name):
        res = supabase.storage.from_(bucket_name).remove(image_name)





    
