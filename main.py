import cv2
import moviepy.editor as mp
import numpy as np

class BadApple:
    input_path = r'./BadApple!!.mp4'
    output_movei_path = './result/output_no_audio.mp4'
    output_audmovei_path = './result/output.mp4'
    output_audio_path = './result/audio.mp3'
    
    frameWidth = 640
    frameHeight = 480

    def main(self):
        print('動画編集中...')
        self.make_video()
        print('音楽編集中...')
        self.set_audio()


    def make_video(self):
        # Input the video
        cap = cv2.VideoCapture(self.input_path)

        # Get the frame rate
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Designate the format
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter(self.output_movei_path, fmt, fps, (self.frameWidth, self.frameHeight),0)

        i = 1
        while True:
            # Get the frame info
            ret, img = cap.read()
            
            # Terminate when video are end
            if ret == False:
                break
                
            # Force quit when press key q 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
            
            # Resize
            img = cv2.resize(img, (self.frameWidth, self.frameHeight))
            
            # Convert to grayscale
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Binarize process
            img_bin = img_gray.copy()
            img_bin[img_gray < 128] = 0
            img_bin[img_gray >= 128] = 255
            
            # Convert image to letter-image
            img_letter = self.image2letter(np.array(img_bin))
            
            # Show the image
            cv2.imshow('Bad Apple!!', img_letter)
            
            # Output the image info
            #print('ret: ', ret, '\tFrame: ', str(i))
            #i += 1
            
            # Write the image
            writer.write(img_letter)
            
        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        
    
    def set_audio(self):
        # Extract audio from input video
        clip_input = mp.VideoFileClip(self.input_path)
        clip_input.audio.write_audiofile(self.output_audio_path)

        # Add audio to output video
        output_movie = mp.VideoFileClip(self.output_movei_path)
        clip_output = output_movie.set_audio(mp.AudioFileClip(self.output_audio_path))
        clip_output.write_videofile(self.output_audmovei_path)


    def image2letter(self, array):
        letter_array = array.copy()
        letter_array[:] = 255
        
        for i in range(int(self.frameHeight/10)):
            for j in range(int(self.frameWidth/10)):
                x = i * 10 + 9
                y = j * 10
                
                if array[x,y] == 0:
                    cv2.putText(letter_array,
                    text='B',
                    org=(y, x),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_AA)
                
                elif array[x,y] == 255:
                    cv2.putText(letter_array,
                    text='W',
                    org=(y, x),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_AA)
                
                else:
                    continue
                 
        return letter_array
    
    
if __name__ == "__main__":
    BadApple().main()