import face_recognition
import cv2
import numpy as np
import time
import function.Face_DataBase as Face_DataBase
import function.no_match_face as no_match_face
import function.user_interact as user_interact


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

run_once_true = 0
run_once_false = 0
start_time = time.time()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(Face_DataBase.known_face_encodings, face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(Face_DataBase.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            # # If a match was found in known_face_encodings, just use the first one.








            # Check if any face in the frame matches a known face
            matches = [True if distance < 0.6 else False for distance in face_distances]
            if True in matches:
                # Get the index of the best match
                best_match_index = matches.index(True)
                name = Face_DataBase.known_face_names[best_match_index]
    
                # Perform actions if it's the first time the face is detected or after 1 minute
                if run_once_true == 0 or time.time() - start_time >= 60:
                    # Speak a welcome message and the name of the person
                    user_interact.convert_to_audio("Welcome")
                    user_interact.convert_to_audio(name)
                    # Reset the welcome message timer
                    start_time = time.time()
                    # Set the run_once flag to avoid repeating the welcome message
                    run_once_true = 1
            else:
                # Reset the run_once flag if no match was found
                run_once_true = 0
                

            if False in matches:
                if run_once_false ==0:
                    no_match_face.main()       
                    run_once_false =1

                

                
                    







# Or instead, use the known face with the smallest distance to the new face
            #face_distances = face_recognition.face_distance(Face_DataBase.known_face_encodings, face_encoding)
            #best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = Face_DataBase.known_face_names[best_match_index]

            
            
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

