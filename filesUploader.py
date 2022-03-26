import os
import time
import dropbox
from tqdm import tqdm
from simple_chalk import chalk
from dropbox import DropboxOAuth2FlowNoRedirect


class TransferData:
    def __init__(self) -> None:
        transferData = TransferData.token()

        try:
            file1 = input("Enter your folder path : ")
            file2 = input("\nEnter path where you want to save in Dropbox ( default : / ) : ")
        except KeyboardInterrupt:
            TransferData.error(1)
        except:
            TransferData.error(2)
        else:
            pass

        TransferData.upload_file(file1, file2)

    def token():
        try:
            token = open("token.txt", "r")
        except FileNotFoundError:
            token = open("token.txt", "w")
            TransferData.accessToken()
            print("Try again by typing 'Python uploadFiles.py'")
            TransferData.recallApp()
        except:
            TransferData.error(2)
        else:
            pass

        checkToken = token.read()

        if checkToken == "":
            access_token = "none"
            TransferData.accessToken()
        else:
            access_token = checkToken

        return access_token

    def upload_file(file_from, file_to):
        dbx = dropbox.Dropbox(TransferData.token())
        print("\nUploading your files in", "'"+file_from+"'", "folder ...")

        # enumerate local files recursively
        for root, dirs, files in os.walk(file_from):

            for filename in files:
                # construct the full local path
                local_path = os.path.join(root, filename)

                # construct the full Dropbox path
                relative_path = os.path.relpath(local_path, file_from)
                dropbox_path = os.path.join(file_to, relative_path)
                # upload the file
                with open(local_path, "rb") as f:
                    dbx.files_upload(
                        f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite
                    )
                    print("\n" + chalk.blue("Uploading :"), f.name)
                    for i in tqdm(range(7), desc="Uploading... ", ncols=74):
                        time.sleep(0.1)
                    print(chalk.green("Uploaded :"), f.name)

        print(
            "\n" + chalk.green("Successfully Uploaded your files to"),
            chalk.blue.bold("Dropbox"),
            ".",
        )

    def error(code) -> int:
        if code == 1:
            print("\n" + chalk.yellow("User exited!"))
            os._exit(0)
        elif code == 2:
            print("\n" + chalk.red("SomeThing Went Wrong?"))
            os._exit(1)
        else:
            code = 2

    def copyright():
        app = "Cloud Storage"
        copyRight = app + " Copyright © " + str(time.localtime().tm_year) + " Junaid"

        # Giving a line for Credits
        print("\n")
        # Credits
        print("This app is made by Junaid.")
        print(chalk.bgWhite.black(copyRight))

    def accessToken():
        # On Start
        TransferData.clear()

        # This function will make token send to token function.

        APP_KEY = "ponj4byl3ufl7su"
        APP_SECRET = "bpenulwuui2c65k"

        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

        authorize_url = auth_flow.start()

        print("\n1. Go to: " + authorize_url)
        print('2. Click "Allow" (you might have to log in first).')
        print("3. Copy the authorization code.\n")

        try:
            auth_code = input("Enter the authorization code here: ").strip()
        except KeyboardInterrupt:
            TransferData.error(1)
        except:
            TransferData.error(2)
        else:
            pass

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print("Error: %s" % (e,))
            exit(1)

        dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)
        account = dbx.users_get_current_account()

        print(chalk.green("Successfully Login!"), "\n")
        print(chalk.bold.blue("Welcome " + account.name.given_name))

        token = open("token.txt", "w")
        token.write(oauth_result.access_token)

    def clear():
        # for windows
        if os.name == "nt":
            os.system("cls")

        # for mac and linux(if, os.name is 'posix')
        else:
            os.system("clear")

    def recallApp():
        os.system("python uploadFiles.py")
