import os
import subprocess


pc_player_folder = r"C:\Users\username\Documents\My Games\Terraria\Players"  # player PC folder - replace with path to player folder
android_player_folder = "/sdcard/Android/data/com.and.games505.TerrariaPaid/Players" # android player folder
pc_world_folder = r"C:\Users\username\Documents\My Games\Terraria\Worlds"  # worlds PC folder - replace with path to worlds folder
android_world_folder = "/sdcard/Android/data/com.and.games505.TerrariaPaid/Worlds" # android worlds folder

adb_path = r"C:\Users\usernamw\AppData\Local\Programs\Python\Python313\Lib\site-packages\adbutils\binaries\adb.exe" # path to adb exe

def adb_pull(android_path: str, pc_path: str):
    try:
        subprocess.check_call([adb_path, "pull", android_path, pc_path])
        print(f"Pulled {os.path.basename(android_path)} from Android to PC \n")
    except subprocess.CalledProcessError:
        print(f"Failed to pull {os.path.basename(android_path)} \n")

def adb_push(pc_path:str, android_path:str):
    try:
        subprocess.check_call([adb_path, "push", pc_path, android_path])
        print(f"Pushed {os.path.basename(pc_path)} from PC to Android \n")
    except subprocess.CalledProcessError:
        print(f"Failed to push {os.path.basename(pc_path)} \n")


def getFileList(type:str, device:str):

    if type == "player":

        playersList = []
        playersListRaw = []
        
        if device == "android":
            try:
                playersListRaw = (subprocess.check_output([adb_path, "shell", "ls", android_player_folder], text=True)).strip().split("\n")
            except:
                print("error no mobile files found")
                return
            
        elif device == "pc":
            try:
                playersListRaw = list(file.name for file in os.scandir(pc_player_folder) if file.is_file())
            except:
                print("error no pc files found")
                return 

        for i in playersListRaw:
            if i[-4:] == ".plr": 
                playersList.append(i)

        return playersList
    
    if type == "world":
        
        worldsList = []
        worldsListRaw = []
        
        if device == "android":
            try:
                worldsListRaw = (subprocess.check_output([adb_path, "shell", "ls", android_world_folder], text=True)).strip().split("\n") 
            except:
                print("error no mobile files found")
                return

        elif device == "pc":
            try: 
                worldsListRaw = list(file.name for file in os.scandir(pc_world_folder) if file.is_file())
            except:
                print("error no pc files found")
                return 

        for i in worldsListRaw:
            if i[-4:] == ".wld":
                worldsList.append(i)
        
        return worldsList


def fetch(targetData:str, androidFolder:str, pcFolder:str, type:str):

        transferring = True  

        # set file paths
        android_file = f"{androidFolder}/{targetData}"
        pc_file = os.path.join(pcFolder, targetData)

        # loop until either confirmed or denied
        while transferring:

            confirmFetch = input("confirm fetch of " + targetData + " [y/n] ").lower()

            if confirmFetch == "y":
                transferring = False
                os.system('cls')
                print(f"Fetching {type} from Android...")
                adb_pull(android_file, pc_file)
                main()

            elif confirmFetch == "n":
                transferring = False
                os.system("cls")
                print("Abandoning... \n\n")
                main()

            
def commit(targetData:str, pcFolder:str, androidFolder:str, type:str):
    
    transferring = True

    pc_file = os.path.join(pcFolder, targetData)
    android_file = f"{androidFolder}/{targetData}"

    while transferring:

        confirmFetch = input("confirm committing of " + targetData + " [y/n] ").lower()

        if confirmFetch == "y":
            transferring = False
            os.system('cls')
            print(f"Committing {type} to Android...")
            adb_push(pc_file, android_file)
            main()

        elif confirmFetch == "n":
            transferring = False
            os.system("cls")
            print("Abandoning... \n\n")
            main()


def displayFiles(index: int, operation: str, type: str):

    fileList = None

    if operation == "fetch":
        
        if type == "world":

            print("Mobile Worlds:\n")
            
            fileList = getFileList(type, device="android")

        elif type == "player":

            print("Mobile Players:\n")
            
            fileList = getFileList(type, device="android")


    if operation == "commit":
        
        if type == "world":

            print("PC Worlds:\n")
            
            fileList = getFileList(type, device="pc")

        elif type == "player":

            print("PC Players:\n")
            
            fileList = getFileList(type, device="pc")
    
    if fileList != None:

        totalPages = len(fileList)//10

        targetDataIndex = printList(fileList, index, operation, totalPages, type)
        
        targetData = fileList[targetDataIndex]

        if operation == "fetch":
            if type == "world":
                fetch(targetData, android_world_folder, pc_world_folder, type)

            elif type == "player":
                fetch(targetData, android_player_folder, pc_player_folder, type)

        elif operation == "commit":
            if type == "world":
                commit(targetData, pc_world_folder, android_world_folder, type)

            elif type == "player":
                commit(targetData, pc_player_folder, android_player_folder, type)
    else:
        return 

def printList(fileList:list, index:int, operation:str, totalPages:int, type:str) -> int:

    #prints files 
    for i in range(len(fileList[index: index+min(10, len(fileList) - index)])):
        print(f"[{i}] " + f"{fileList[i+index]}")
    
    pageN = index//10
    backArrow = ""
    forwardArrow = ""

    if totalPages > 0:
        if pageN < totalPages:
            forwardArrow = " D>"
        if pageN > 0:
            backArrow = "<A "

    print("============================")
    print(f"{backArrow} page {pageN+1} of {totalPages+1} {forwardArrow}")
    
    userInpt = ""

    ran = False
    
    while ran == False: 

        userInpt = input(f"\n{type} to {operation}: ").strip().lower()

        if userInpt == 'a' and backArrow == "<A ":
            print("\n")
            ran = True
            return printList(fileList, index - 10, operation, totalPages,type)

        elif userInpt == 'd' and forwardArrow == " D>":
            print("\n")
            ran = True
            return printList(fileList, index + 10, operation, totalPages, type)

        else:
            try:
                targetDataIndex = int(userInpt) + index
                ran = True
            except ValueError:
                print("Please enter a valid number. ")
                continue

            if (targetDataIndex > len(fileList)-1):
                print("Please enter a valid number. ")
                continue
            
        return targetDataIndex


def main():
    
    fetchOrCommit = input("[F]etch\n[C]ommit\n[E]xit\n").lower()

    if fetchOrCommit == "e":
        return
    
    wOrP = input("\n[W]orlds\n[P]layers\n").lower()
    
    if fetchOrCommit == 'f':
        if wOrP == 'w':
            os.system('cls')
            displayFiles(0, "fetch", "world")

        elif wOrP == 'p':
            os.system('cls')
            displayFiles(0, "fetch", "player")


    elif fetchOrCommit == "c":
        if wOrP == 'w':
            os.system('cls')
            displayFiles(0, "commit", "world")

        elif wOrP == 'p':
            os.system('cls')
            displayFiles(0, "commit", "player")


    else:
        os.system('cls')
        main()
                
            
if __name__ == "__main__":
    main() 
