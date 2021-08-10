import json

# Open json file and convert into dictionary object
f = open('data.json',)
data = json.load(f)
f.close()

# Find total number of rows and columns
rows = data["venue"]["layout"]["rows"]
columns = data["venue"]["layout"]["columns"]

# Create a matrix of seat initially filled with 0
# 0 indicates that seat is filled
# 1 indicates that seat is empty
seat_matrix = [[0] * columns ] * rows

def fill_seat_matrix():
    # Fill the seat matrix based on data given in json file
    for i in range(rows):
        for j in range(columns):
            seat_key = chr(i + 97) + str(j+1)
            if seat_key in data["seats"] and data["seats"][seat_key]["status"] == "AVAILABLE":
                seat_matrix[i][j] = 1


# Function to determine if we have seats available in a row
# start_seat and and end_seat indicate seat number in the row
def check_seats_availablity(row, start_seat, end_seat):
    seats_found = True
    for j in range(start_seat, end_seat+1):
        if seat_matrix[row][j] == 0:
            seats_found = False
    return seats_found


def find_seats(total_requested_seats):
    i = 0
    seats_found = False

    # Start from first row and check upto last row
    while i < rows and not seats_found:
        # Start from middle of row and expand around i
        middle = columns//2
        # Expected arrangement for 3 seats (middle-1, middle, middle+1)
        # 3//2 = 1, so for 3 seats take 1 seat to left, 1 to right alongwith middle
        # For 5 seats, take 5//2 = 2, 2 seats to left, 2 to right of middle
        # Use same formula to determine position of starting block of seats
        # Start from left of middle seat
        start_seat = middle - (total_requested_seats//2)
        # End at right of middle seat
        end_seat = middle + (total_requested_seats//2)

        # For even number of seats, arrangement would be (middle-1, middle)
        # Removing additional seat (middle+1)
        if total_requested_seats % 2 == 0:
            end_seat -= 1

        # Check if seat is available to the left
        # Keep moving block of seats until enough seats are found
        while not seats_found and start_seat >=0:
            seats_found = check_seats_availablity(i, start_seat, end_seat)
            if not seats_found:
                start_seat -= 1
                end_seat -= 1

        # Check if seat is available towards right
        # Keep moving block of seats until enough seats are found
        while not seats_found and end_seat < columns:
            seats_found = check_seats_availablity(i, start_seat, end_seat)
            if not seats_found:
                start_seat += 1
                end_seat += 1
        i+=1

    return (i, start_seat, end_seat, seats_found)

number_of_requested_seats = input("Enter number of seats required: ")
fill_seat_matrix()
row, start_seat, end_seat, seats_found = find_seats(number_of_requested_seats)

seat_row = chr(row+96)
allotted_seats = []
# Convert seat index to seat numbers in format a6, a7
for i in range(start_seat, end_seat+1):
    allotted_seats.append(seat_row + str(i+1))
print(allotted_seats)
