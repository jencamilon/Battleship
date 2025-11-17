def ship_type(ship):
  '''to be implemented according to specification'''

  return ship[0] if ship [0] in ["destroyer", "carrier"] else None

 # Source: https://chatgpt.com for shortening the code instead of using if and else
  
def ship_from_input(type_inp, rotation_inp, anchor_inp):
  '''to be implemented according to specification'''

  N, M = map(int, anchor_inp.split())
  
  if type_inp == "D":
    destroyer_rotation = {
      "0": {(N,M), (N,M+1)},
      "90": {(N,M), (N+1,M)},
      "180": {(N,M), (N,M-1)},
      "270": {(N,M), (N-1,M)},
    }

    return("destroyer", destroyer_rotation.get(rotation_inp, set()), set())

  elif type_inp == "C":
    carrier_rotation ={
      "0": {(N,M), (N+1,M), (N+2,M), (N,M+1)},
      "90": {(N,M), (N,M-1), (N,M-2), (N+1,M)},
      "180": {(N,M), (N-1,M), (N-2,M), (N,M-1)},
      "270": {(N,M), (N,M+1), (N,M+2), (N-1,M)},
    }
  
    return("carrier", carrier_rotation.get(rotation_inp, set()), set())

  return None
  

def ok_to_place_ship_at(ship, fleet):
  '''to be implemented according to specification'''

  new_ship_positions = set(ship[1])
    
  for row, column in new_ship_positions:
    if not (0 <= row <= 9 and 0 <= column <= 9):
      return False
    
  for existing_ship in fleet:
    occupied_positions = set(existing_ship[1])
    adjacent_positions = occupied_positions.copy()
        
    for row, column in occupied_positions:
      adjacent_positions.update({
        (row-1, column), (row+1, column), (row, column-1), (row, column+1)
      })
        
    if new_ship_positions & adjacent_positions:
      return False
    
  return True


def is_sunk(ship):
  '''to be implemented according to specification
  
  Hint (not following it will not affect your mark): how to check if a carrier is sunk?

  One idea is to implement a pair of functions: 
  - a function that computes the long side of the carrier as a set of squares
  - a function that computes the short side of the carrier

  It remains to check if either of the sides is (fully) covered by hit squares
  '''

  type_inp = ship[0]
  occupied_squares = ship[1]
  hit_squares = ship[2]

  if type_inp == "destroyer":
    return occupied_squares.issubset(hit_squares)

  elif type_inp == "carrier":
    rows = {}
    columns = {}

    for row, col in occupied_squares:
      rows.setdefault(row, set()).add((row, col))
      columns.setdefault(col, set()).add((row, col))

    long_side = next((squares for squares in rows.values() if len(squares) == 3), None)
    if not long_side:
      long_side = next((squares for squares in columns.values() if len(squares) == 3), None)

    short_side = next((squares for squares in rows.values() if len(squares) == 2), None)
    if not short_side:
      short_side = next((squares for squares in columns.values() if len(squares) == 2), None)

    if (long_side and long_side.issubset(hit_squares)) or (short_side and short_side.issubset(hit_squares)):
      return True

    return False

  else:
    return False

# Source: https://chatgpt.com for defining if the long side or short side of the carrier is already sunk

def is_water(row, column, fleet):
  '''to be implemented according to specification'''

  for ship in fleet:
    occupied_squares = ship[1]
    hit_squares = ship[2]

    if (row, column) in occupied_squares:
      if is_sunk(ship):
        return True

      elif (row, column) in hit_squares:
        return True

      return False

  return True

def what_hit(row, column, fleet):
  '''to be implemented according to specification'''
  for ship in fleet:
    type_inp, occupied_squares, hit_squares = ship
    if (row, column) in occupied_squares:
      if (row, column) not in hit_squares:
        return ship
  return None


def what_sunk(row, column, fleet):
  '''to be implemented according to specification'''

  for ship in fleet:
    type_inp = ship[0]
    occupied_squares = ship[1]
    hit_squares = ship[2]

    if (row, column) in occupied_squares:
      hit_squares_updated = hit_squares | {(row, column)}

      if hit_squares_updated == occupied_squares:
        return (type_inp, occupied_squares, hit_squares)

  return None

def are_unsunk_left(fleet):
  '''to be implemented according to specification'''

  return any(not is_sunk(ship) for ship in fleet)

  
def update_fleet(row, column, fleet):
  '''to be implemented according to specification'''

  fleet_updated = []

  for ship in fleet:
      type_inp = ship[0]
      occupied_squares = ship[1]
      hit_squares = ship[2]

      if (row, column) in occupied_squares:
        hit_squares_updated = hit_squares.copy()
        hit_squares_updated.add((row, column))

        ship_updated = (type_inp, occupied_squares, hit_squares_updated)
        fleet_updated.append(ship_updated)

      else:
        fleet_updated.append(ship)
    
  return fleet_updated
    


def main():
  '''to be implemented according to specification'''

  fleet = []

  print('''Your turn Player 1. When entering a type of a ship, type "D" for destroyer and "C" for carrier (followed by Enter key).
When entering rotation of a ship, type "0", "90", "180" or "270".
When entering a square, first type row and then column, e.g. "6 3". Both numbers must be between 0 and 9.''')
  print()

  while True:
    ship_type = input('''Player 1, enter the type of the next ship or enter "Q" if you are done specifying the fleet: ''')
    if ship_type == "Q":
      break

    if ship_type not in {"D", "C"}:
      print("Invalid ship type!", end=' ')
      continue
              
    rotation = input("Player 1, enter the rotation of this ship: ")
    if rotation not in {"0", "90", "180", "270"}:
      print("Invalid rotation!", end=' ')
      continue

    while True:
      anchor = input("Player 1, enter the square that the anchor of this ship occupies in the ocean: ")
      try:
        row, column = map(int, anchor.split())
        if 0 <= row <= 9 and 0 <= column <= 9:
          ship = ship_from_input(ship_type, rotation, f"{row} {column}")
          if ship and ok_to_place_ship_at(ship, fleet):
            fleet.append(ship)
            break
          else:
            print("This is not a valid placement.", end=' ')
        else:
          print("This is not a valid placement.", end=' ')
      except ValueError:
        print("This is not a valid placement.", end=' ')


  if len(fleet) == 0:
    print("Game over!")
    return



  print('''\nYour turn Player 2. When entering a square, first type row and then column, e.g. "6 3". Both numbers must be between 0 and 9.''')
  print()
  
  squares_fired = set()

  while True:
    fire = input("Player 2, enter the square in the ocean you fire at: ")
    try:
      row, column = map(int, fire.split()) 
      if 0 <= row <= 9 and 0 <= column <= 9:
        if (row, column) in squares_fired:
          print("Water!")
          continue

        squares_fired.add((row, column))
        result = what_hit(row, column, fleet)
        if result:
          ship_type, occupied_squares, hit_squares = result

          if (row, column) in hit_squares:
            print("Water!")
            continue

          print(f"You hit a {ship_type}!")
          fleet = update_fleet(row, column, fleet)

          for ship in fleet:
            if ship[0] == ship_type and is_sunk(ship):
              print(f"You sunk a {ship_type}!")
              fleet = [s for s in fleet if not is_sunk(s)]
              break

          if not are_unsunk_left(fleet):
            print("Game over!")
            break
        else: 
          print("Water!")
      else:
          print("This is not a valid square.")
    except ValueError:
      print("This is not a valid square.")


if __name__ == "__main__":  main() #DO NOT MODIFY THIS LINE OR MOVE IT FROM THE END OF FILE