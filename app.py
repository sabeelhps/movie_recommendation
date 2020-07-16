from flask import Flask,render_template,redirect,request

import predict_movies


app=Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/submit",methods=[ "POST" ])
def submit_movie_name():
    if request.method == "POST":

        movie_name=request.form['movie_name']

        predictions=predict_movies.predictMovies(movie_name)
        predictions=predictions[:6]
        # for i in range(6):
        #     print(predictions[i][0])

    return render_template("index.html",movie_list=predictions,movie_name=movie_name)


if __name__=="__main__":
    app.run(debug=True)
