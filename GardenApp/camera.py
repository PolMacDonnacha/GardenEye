import utility
import os
import threading
from picamera import PiCamera
from time import sleep
import cv2
from datetime import datetime, timedelta

camera = PiCamera()
videoFormat = ".mov"
timelapseDirectory = "/home/pi/Pictures/Timelapse/"
allTimelapsePhotos = '/home/pi/Pictures/Timelapse/*.jpg'
liveImageLocation = "/home/pi/Pictures/Live/LiveImage.jpg"
lock = threading.Lock()
camera.annotate_text_size = 30
camera.resolution = (1920, 1080)


def stopTimelapse(timelapseTime,fps): #previous third parameter photoCount
    try:
        timelapseVideo = f"/home/pi/Videos/{timelapseTime}{videoFormat}"
        images = [img for img in sorted(os.listdir(timelapseDirectory)) if img.endswith("jpg")]
        
        frame = cv2.imread(os.path.join(timelapseDirectory,images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(timelapseVideo, 0, fps,(width, height))
        
        for image in images:
            video.write(cv2.imread(os.path.join(timelapseDirectory,image)))
        cv2.destroyAllWindows()
        video.release()
        # The next line converts all timelapse images into a video
        # ffmpeg is an audio and video converter
        # -s denotes the size of the images 1024x768
        # -pattern_type specifies how the system will read the input files, the glob option selects all files in a specified file format, in this case .jpg
        # -i is input and this specifies where the input files will come from, in this case, from the folder where all timelapse images are stored

        #os.system(f'ffmpeg -f image2 -framerate {fps} -loglevel 0 -s 1920x1080 -pattern_type glob -i "/home/pi/Pictures/Timelapse/[0-{photoCount}].jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p {timelapseVideo}')
        #print('Finished ffmpeg command')
        os.environ['TimelapseKeepAlive'] = 'True'
        os.environ['TimelapseRunning'] = 'False'
        sleep(4)
        lock.acquire()
        utility.pushToStorage(f'/Timelapses/{timelapseTime}{videoFormat}', timelapseVideo)
        utility.updateDb('/control/', {'timelapseSwitch':0})
        lock.release()
        utility.deleteFiles("/home/pi/Videos/")
        utility.deleteFiles(allTimelapsePhotos)
        
    except Exception as e:
        print(f'Timelapse stopping catch block reached: {e}\n')
        errorMessage = f"stopTimelapse Function Error: {e}"
        utility.appendToLog("error",errorMessage)
    
def startTimelapse(length,fps, interval):
    os.environ['TimelapseKeepAlive'] = 'True'
    os.environ['TimelapseRunning'] = 'True'
    try:
        currentTime = datetime.now()
        endTime = currentTime + timedelta(minutes=length)
        photosToTake = int((length*60)/interval) #number of photos to take
        estimatedStorageRequired = photosToTake * 1.1
        print(f"Estimated storage required: {estimatedStorageRequired}MB")
        print(f"Number of photos to take = {photosToTake}\n")
        pictureCount = utility.countFiles(timelapseDirectory)
        print(f'Number of photos: {pictureCount}\n')
        if pictureCount > 0:
            utility.deleteFiles(allTimelapsePhotos)
        updatedPictureCount = utility.countFiles(timelapseDirectory)
        print(f'Number of photos left: {updatedPictureCount}\n')
        
        startTime = utility.getTime()
        print(f'Starting timelapse at {startTime}\n')
        count = 0
        while datetime.now() < endTime:
            megabytesAvailable = utility.getAvailableSpace()
            print(f'Storage space left: {megabytesAvailable}MB\n')
            if os.environ['TimelapseKeepAlive'] == 'False' or megabytesAvailable <= estimatedStorageRequired:
                print('Timelapse loop breaking\n')
                break
            while float(os.environ['light']) < 40:
                print(f"Light level too low: {os.environ['light']}\n")
                sleep(3)
            count += 1
            lock.acquire()
            print(f'{count} out of {photosToTake} photos taken\n')
            camera.annotate_text = utility.getEnvStats()
            camera.capture(f'{timelapseDirectory}{utility.getTime()}.jpg')
            lock.release()
            sleep(interval)
        print('Timelapse photos completed\n')
       # if count < photosToTake:# If the timelapse is started early
       #     photosToTake = count
        stopTimelapse(startTime,fps)
    except Exception as e:
        print(f'Timelapse catch block reached: {e}\n')
        errorMessage = f"Timelapse Function Error: {e}"
        utility.appendToLog("error",errorMessage)

def liveViewCapture():
    try:
        print("Live view starting\n")
        while True:
            print('Taking live view photo\n')
            lock.acquire()
            camera.annotate_text = ''
            camera.capture(f'{liveImageLocation}')
            utility.pushToStorage('liveImage.jpg',liveImageLocation)
            lock.release()
            sleep(3)
    except Exception as e:
        print(f'Live view catch block reached: {e}\n')
        errorMessage = f"Live view Function Error: {e}"
        utility.appendToLog("error",errorMessage)
        liveThread = threading.Thread(target=liveViewCapture,args=())#Restart the live view of plants
        liveThread.start()