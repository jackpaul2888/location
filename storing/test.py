import sqlite3
import random

# Connect to your SQLite database
db_path = '/home/mundax/SQLite/My_Database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clear all existing values from the 'location' table
cursor.execute('DELETE FROM location')

# Function to generate random object coordinates
def generate_object_coordinates(num_objects):
    return [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(num_objects)]

# Insert 100 rows into the 'location' table with the specified rules
for group in range(17):  # 0-16 creates 100 rows (6 cameras per group)
    # Common GPS coordinates for the 6 cameras in this group
    gps_latitude = random.uniform(-90.0, 90.0)
    gps_longitude = random.uniform(-180.0, 180.0)

    # Assign object coordinates for the first camera
    obj_coordinates = generate_object_coordinates(3)  # Three objects for the first camera

    # Insert data for each of the 6 cameras in the group
    for camera_offset in range(6):
        camera_id = camera_offset + 1  # Camera IDs from 1 to 6

        # Get the object coordinates for this camera
        if camera_id == 1:  # First camera
            obj1_x, obj1_y = obj_coordinates[0]
            obj2_x, obj2_y = obj_coordinates[1]
            obj3_x, obj3_y = obj_coordinates[2]
            class_obj_1 = random.randint(1, 3)
            class_obj_2 = random.randint(1, 3)
            class_obj_3 = random.randint(1, 3)
        elif camera_id in (2, 3):  # Cameras that share objects with camera 1
            obj1_x, obj1_y = obj_coordinates[0]  # Object from camera 1
            obj2_x, obj2_y = obj_coordinates[1]  # Object from camera 1
            obj3_x, obj3_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            class_obj_1, class_obj_2 = random.randint(1, 3), random.randint(1, 3)
            class_obj_3 = random.randint(1, 3)
        elif camera_id == 4:  # Camera that shares objects with camera 2
            obj1_x, obj1_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            obj2_x, obj2_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            obj3_x, obj3_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            class_obj_1, class_obj_2, class_obj_3 = random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)
        else:  # Camera 5 and 6
            obj1_x, obj1_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            obj2_x, obj2_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            obj3_x, obj3_y = random.uniform(-100, 100), random.uniform(-100, 100)  # New object
            class_obj_1, class_obj_2, class_obj_3 = random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)

        # Random angles
        angle_1 = random.uniform(0, 360)
        angle_2 = random.uniform(0, 360)
        angle_3 = random.uniform(0, 360)

        # Insert values into the location table
        cursor.execute('''
            INSERT INTO location (
                camera_id, gps_latitude, gps_longitude,
                angle_1, angle_2, angle_3,
                obj1_x, obj1_y,
                obj2_x, obj2_y,
                obj3_x, obj3_y,
                class_obj1, class_obj2, class_obj3,
                obj1_latitude, obj1_longitude,
                obj2_latitude, obj2_longitude,
                obj3_latitude, obj3_longitude
            ) VALUES (?, ?, ?,
                      ?, ?, ?,
                      ?, ?, 
                      ?, ?, 
                      ?, ?, 
                      ?, ?, ?,
                      NULL, NULL,
                      NULL, NULL,
                      NULL, NULL)
        ''', (camera_id, gps_latitude, gps_longitude,
              angle_1, angle_2, angle_3,
              obj1_x, obj1_y,
              obj2_x, obj2_y,
              obj3_x, obj3_y,
              class_obj_1, class_obj_2, class_obj_3))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Inserted 100 rows into the location table with specified rules.")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# import sqlite3

# # Connect to your SQLite database
# db_path = '/home/mundax/SQLite/My_Database.db'
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Clear all values from the 'location' table
# cursor.execute('DELETE FROM location')

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# print("All values have been cleared from the 'location' table.")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
