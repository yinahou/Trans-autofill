import os
import json
from tqdm import tqdm
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models 

def is_japanese(text):
    """
    Check if the text contains Japanese characters.
    This function looks for Kana characters which are unique to Japanese.
    """
    for char in text:
        if '\u3040' <= char <= '\u30ff':  # Range for Hiragana and Katakana
            return True
    return False

def translate_japanese(source_text):
    secret_id=''
    secret_key=''
    try:
        # Set up credentials
        cred = credential.Credential(secret_id, secret_key) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        # Set up client profile
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

        # Prepare the request
        req = models.TextTranslateRequest()
        req.SourceText = source_text
        req.Source = 'jp'
        req.Target = 'zh'
        req.ProjectId = 0
        
        # Send the request and print the response
        resp = client.TextTranslate(req) 
        return resp.TargetText

    except TencentCloudSDKException as err: 
        print(err)
        return str(err)

def process_and_save_files(directory, start_line=0):
    """
    Process all .txt files in the given directory, translate the Japanese text,
    and save the translations in new files.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            translated_file_path = os.path.join(directory, f"translated_{filename}")

            with open(file_path, 'r', encoding='UTF-16') as file:
                total_lines = sum(1 for line in file)

            with open(file_path, 'r', encoding='UTF-16') as file, \
                 open(translated_file_path, 'a', encoding='UTF-16') as translated_file:
                line_number=0
                for line in tqdm(file, total=total_lines, desc=f"Processing {filename}", leave=False):
                    line_number += 1
                    if line_number < start_line:
                        continue
                    translated_line = translate_japanese(line.strip()) if is_japanese(line) else line.strip()
                    translated_file.write(translated_line + '\n')
                
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory, filename)
#             translated_file_path = os.path.join(directory, f"translated_{filename}")

#             with open(file_path, 'r', encoding='UTF-16') as file, \
#                  open(translated_file_path, 'a', encoding='UTF-16') as translated_file:
#                 for line_number, line in enumerate(file, start=1):
#                     if line_number < start_line:
#                         continue
#                     translated_line = translate_japanese(line.strip()) if is_japanese(line) else line.strip()
#                     translated_file.write(translated_line + '\n')

# Replace 'your_directory_path' with the path to the directory containing the .txt files
directory_path = './data'
start_from_line = 0  # Replace with the line number from which you want to start processing

# Calling the function to process and save files in the specified directory
process_and_save_files(directory_path, start_from_line)