import os
from flask import Blueprint, render_template
from flask_login import login_required, current_user

usr = Blueprint('usr', __name__)


# Auto
@usr.route('/')
@login_required
def home():
    imgFilePath_Price = os.path.join('static', 'priceGraphs/ETHUSDT_LongTerm_PriceGraph.png')
    imgFilePath_SentimentGraph = os.path.join('static', 'sentimentGraphs/ADA_LongTerm_SentimentGraph.png')
    imgFilePath_wordcloudImg = os.path.join('static', 'wordClouds/ADA_wordcloud.png')
    imgFilePath_LSTM_resultsImg = os.path.join('static', 'LSTM_Model_Results/ADAUSDT_LSTM_modelPredictionsResults_onDaysPrecedingTrainingData.png')
    imgFilePath_LSTM_results_onTrainingData_img = os.path.join('static', 'LSTM_Model_Results/ADAUSDT_LSTM_modelPredictionsResults.png')
    return render_template("view_cryptocurrency_data.html", user=current_user, price_graph=imgFilePath_Price,
                           sentiment_graph=imgFilePath_SentimentGraph,
                           wordcloud_img=imgFilePath_wordcloudImg,
                           LSTM_results_img=imgFilePath_LSTM_resultsImg,
                           LSTM_results_onTrainingData_img=imgFilePath_LSTM_results_onTrainingData_img)


@usr.route('/ada')
@login_required
def view_ada():
    imgFilePath_Price = os.path.join('static', 'priceGraphs/ADAUSDT_LongTerm_PriceGraph.png')
    imgFilePath_SentimentGraph = os.path.join('static', 'sentimentGraphs/ADA_LongTerm_SentimentGraph.png')
    imgFilePath_wordcloudImg = os.path.join('static', 'wordClouds/ADA_wordcloud.png')
    imgFilePath_LSTM_resultsImg = os.path.join('static', 'LSTM_Model_Results/ADAUSDT_LSTM_modelPredictionsResults_onDaysPrecedingTrainingData.png')
    imgFilePath_LSTM_results_onTrainingData_img = os.path.join('static', 'LSTM_Model_Results/ADAUSDT_LSTM_modelPredictionsResults.png')
    return render_template("view_cryptocurrency_data.html", user=current_user, price_graph=imgFilePath_Price,
                           sentiment_graph=imgFilePath_SentimentGraph,
                           wordcloud_img=imgFilePath_wordcloudImg,
                           LSTM_results_img=imgFilePath_LSTM_resultsImg,
                           LSTM_results_onTrainingData_img=imgFilePath_LSTM_results_onTrainingData_img)


@usr.route('/eth')
@login_required
def view_eth():
    imgFilePath_Price = os.path.join('static', 'priceGraphs/ETHUSDT_LongTerm_PriceGraph.png')
    imgFilePath_SentimentGraph = os.path.join('static', 'sentimentGraphs/ETH_LongTerm_SentimentGraph.png')
    imgFilePath_wordcloudImg = os.path.join('static', 'wordClouds/ETH_wordcloud.png')
    imgFilePath_LSTM_resultsImg = os.path.join('static', 'LSTM_Model_Results/ETHUSDT_LSTM_modelPredictionsResults_onDaysPrecedingTrainingData.png')
    imgFilePath_LSTM_results_onTrainingData_img = os.path.join('static', 'LSTM_Model_Results/ETHUSDT_LSTM_modelPredictionsResults.png')
    return render_template("view_cryptocurrency_data.html", user=current_user, price_graph=imgFilePath_Price,
                           sentiment_graph=imgFilePath_SentimentGraph,
                           wordcloud_img=imgFilePath_wordcloudImg,
                           LSTM_results_img=imgFilePath_LSTM_resultsImg,
                           LSTM_results_onTrainingData_img=imgFilePath_LSTM_results_onTrainingData_img)


@usr.route('/btc')
@login_required
def view_btc():
    imgFilePath_Price = os.path.join('static', 'priceGraphs/BTCUSDT_LongTerm_PriceGraph.png')
    imgFilePath_SentimentGraph = os.path.join('static', 'sentimentGraphs/BTC_LongTerm_SentimentGraph.png')
    imgFilePath_wordcloudImg = os.path.join('static', 'wordClouds/BTC_wordcloud.png')
    imgFilePath_LSTM_resultsImg = os.path.join('static', 'LSTM_Model_Results/BTCUSDT_LSTM_modelPredictionsResults_onDaysPrecedingTrainingData.png')
    imgFilePath_LSTM_results_onTrainingData_img = os.path.join('static', 'LSTM_Model_Results/BTCUSDT_LSTM_modelPredictionsResults.png')
    return render_template("view_cryptocurrency_data.html", user=current_user, price_graph=imgFilePath_Price,
                           sentiment_graph=imgFilePath_SentimentGraph,
                           wordcloud_img=imgFilePath_wordcloudImg,
                           LSTM_results_img=imgFilePath_LSTM_resultsImg,
                           LSTM_results_onTrainingData_img=imgFilePath_LSTM_results_onTrainingData_img)






    '''@auth.route("/view")
    def view():
        return render_template("view.html", values=users.query.all())

    @auth.route("/user", methods=["POST", "GET"])
    def user():
        email = None
        if "userName" in session:
            userName = session["userName"]

            if request.method == "POST":
                email = request.form["email"]
                found_user = users.query.filter_by(name=userName).first()
                found_user.email = email
                session["email"] = email
                db.session.commit()
                flash("Email was saved!")
            else:
                if "email" in session:
                    email = session["email"]

            # PEOPLE_FOLDER = os.path.join('static', 'people_photo')
            imgFilePath = os.path.join('static', 'ETHUSDT_LongTerm_PriceGraph.png')
            # plot_url = get_eth_usd_graph()

            return render_template("user.html", userName=userName, email=email, plot_url=imgFilePath)
        else:
            flash("You are not logged in!")
            return redirect(url_for("login"))'''