from flask import Flask, render_template, request

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

  bg_colors = {"81a": "#FF6600",  "85a": "#FFFF00", "87a": "#9900FF", "90a": "#FF0000", "93a": "#00CC00", "97a": "#FF00FF"}

  text_colors = dict((item, "#FFFFFF") for item in bg_colors)
  text_colors["85a"] = "#000000"

  weight = int(weight)
  
  if weight_type == "lb":
    weight *= .453

  bushing_pairs = []

  columns = [("Soft", -5), ("Medium", 0), ("Hard", 5)]

  for column in columns:
    bushing_pairs.append([[weight_to_duro(weight + column[1], boardside=False), weight_to_duro(weight + column[1], boardside=True)], column[0]])

  return render_template("main.html", show_bushings=True, invalid=False, bushing_pairs=bushing_pairs, bg_colors=bg_colors, weight = request.values['weight'], weight_type = request.values['weight_type'], text_colors=text_colors)

def weight_to_duro(weight, boardside=True):
  """ Takes a weight in KG and returns an appropriate duro bushing """
  bushings = [81, 85, 87, 90, 93, 97]

  if not boardside:
    weight -= 5

  approx_duro = ( (weight - 30) / 4.0) + 79

  duro = min(bushings, key=lambda x:abs(x-approx_duro))

  return str(duro) + 'a'

def run_app():
  app.run()

if __name__ == '__main__':
  run_app()
