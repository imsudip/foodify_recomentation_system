from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from word2vec_rec import get_recs

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET"])
def hello():
    return HELLO_HTML


HELLO_HTML = """
     <html><body>
         <h1>Welcome to my api: Whatscooking!</h1>
         <p>Please add some ingredients to the url to receive recipe recommendations.
            You can do this by appending "/recipe?ingredients= Pasta Tomato ..." to the current url.
         <br>Click <a href="/recipe?ingredients=pasta,tomato,onion">here</a> for an example when using the ingredients: pasta, tomato and onion.
     </body></html>
     """


@app.route('/recipe', methods=["GET"])
def recommend_recipe():
    ingredients = request.args.get('ingredients')
    limit = request.args.get('limit')
    if limit is None:
        limit = 10
    else:
        limit = int(limit)
    recipe = get_recs(ingredients, limit)

    response = []
    count = 0
    for index, row in recipe.iterrows():
        response.append({
            'title': str(row['title']),
            'score': str(row['score']),
            'ingredients': str(row['ingredients']),
            'recipe_id': str(row['recipe_id'])
        })
        count += 1
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


# http://127.0.0.1:5000/recipe?ingredients=pasta

# use ipconfig getifaddr en0 in terminal (ipconfig if you are on windows, ip a if on linux)
# to find intenal (LAN) IP address. Then on any devide on network you can use server.
