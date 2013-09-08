from flask import Flask, render_template, request
import unittest
import doctest

class BushingPair(object):
  """An object to represent a pair of bushings"""
  def __init__(self, weight, label):
    super(BushingPair, self).__init__()
    self.weight = weight
    self.boardside = weight_to_duro(self.weight, boardside=True)
    self.roadside = weight_to_duro(self.weight, boardside=False)
    self.label = label
    self.bushings = [self.roadside, self.boardside]

  def compare_pairs(self, other):
    """
    Returns true if self and other have the same duro bushings
    >>> a = BushingPair(70, "TestA")
    >>> b = BushingPair(67, "TestB")
    >>> a.compare_pairs(b)
    True

    >>> a = BushingPair(70, "TestA")
    >>> b = BushingPair(90, "TestB")
    >>> a.compare_pairs(b)
    False
    """
    return (self.boardside == other.boardside and self.roadside == other.roadside)

app = Flask(__name__)

@app.route('/')
def main():
  return render_template("main.html", show_bushings=False, invalid=False)

@app.route('/query', methods=['GET'])
def query():
  weight = request.values['weight']
  weight_type = request.values['weight_type']

  if not weight.isdigit():
    return render_template("main.html", show_bushings=False, invalid=True)

  bg_colors = {"78a": "#0000FF","81a": "#FF6600",  "85a": "#FFFF00", "87a": "#9900FF", "90a": "#FF0000", "93a": "#00CC00", "97a": "#FF00FF"}

  text_colors = dict((item, "#FFFFFF") for item in bg_colors)
  text_colors["85a"] = "#000000"

  weight = int(weight)
  
  if weight_type == "lb":
    weight *= .453

  bushing_pairs = []

  offset = 5

  min_duro = sorted(bg_colors)[0]
  max_duro = sorted(bg_colors)[-1]

  columns = [("Soft", -1), ("Medium", 0), ("Hard", 1)]

  for column in columns:
    bushing_pairs.append(BushingPair(weight + column[1] * offset, column[0]))

  items_to_test = [0, 2]

  for item in items_to_test:
    i = 1
    while bushing_pairs[item].compare_pairs(bushing_pairs[1]) and bushing_pairs[item].roadside != min_duro and bushing_pairs[item].boardside != max_duro:
      bushing_pairs[item] = BushingPair(weight + (offset + i) * columns[item][1], columns[item][0])
      i += 2

  return render_template("main.html", show_bushings=True, invalid=False, bushing_pairs=bushing_pairs, bg_colors=bg_colors, weight = int(request.values['weight']), weight_type = weight_type, text_colors=text_colors)


def weight_to_duro(weight, boardside=True):
  """ 
  Takes a weight in KG and returns an appropriate duro bushing. 

  >>> weight_to_duro(75)
  '90a'

  >>> weight_to_duro(75, boardside=False)
  '87a'

  >>> weight_to_duro(300)
  '97a'

  >>> weight_to_duro(20)
  '78a'
  """

  bushings = [78, 81, 85, 87, 90, 93, 97]

  if not boardside:
    weight -= 5

  weight -= 40
  if weight < 0:
    weight = 0
  approx_duro = ((weight) ** 0.66 ) + 79

  duro = min(bushings, key=lambda x:abs(x-approx_duro))

  return str(duro) + 'a'

def run_app():
  app.run(debug=True)

if __name__ == '__main__':
  doctest.testmod()
  run_app()