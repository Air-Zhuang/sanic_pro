from app import app

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=8000,debug=app.config['DEBUG'],workers=2)
    app.run(host='0.0.0.0',port=8000,debug=app.config['DEBUG'])